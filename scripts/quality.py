#!/usr/bin/env python3
"""Judge what a repository publishes as proof, without judging whether it is good.

  check                     — run every repository linked from README.md
  check --repos FILE        — run one owner/repo per line instead
  check --aggregate FILE    — run rows of a data/games.json-style dump (no manual reading)
  check ... --band MIN MAX  — star window for --aggregate
  check ... --sample N      — deterministic random subset of the matching rows

Per repository it costs three requests: `GET /repos/{owner}/{repo}`, the README, and the
recursive git tree. Responses are cached under scripts/.quality-cache so a re-run is free;
--refresh re-reads. The fourth request (releases) fires only when no build file was found.

Four evidence classes, each either present in the repository or not:

  E1 match      byte-for-byte / matching ROM / a hash / a decompilation percentage
  E2 compat     a compatibility or progress table with a denominator
  E3 repro      a build system or CI, so the reader can reproduce it
  E4 boundary   an explicit "ships no game files, bring your own copy"

verdict: exclude (no source code, no README, archived) / eligible (E1 or E2) /
conditional (E3 or E4 only) / watch (nothing checkable published).
GITHUB_TOKEN (or GH_TOKEN) enables parallel requests; anonymous runs serialise and sleep.
"""
import argparse
import datetime
import hashlib
import json
import os
import random
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
README = ROOT / "README.md"
CACHE = HERE / ".quality-cache"
SLUG = re.compile(r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
PROXY = os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")

SOURCE_EXT = {".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".rs", ".go", ".py", ".java", ".kt",
              ".cs", ".js", ".ts", ".m", ".mm", ".swift", ".lua", ".rb", ".zig", ".d", ".nim",
              ".v", ".vala", ".pl", ".asm", ".s", ".S", ".glsl", ".hlsl", ".sh", ".bat"}
BUILD_FILES = {"cmakelists.txt", "makefile", "gnumakefile", "meson.build", "cargo.toml",
               "package.json", "sconstruct", "build.zig", "configure.ac", "configure",
               "autogen.sh", "bootstrap.sh", "build.gradle", "gemfile", "setup.py", "pyproject.toml",
               "default.nix", "flake.nix", "dockerfile", "build.bazel", "workspace.bazel"}

RE_MATCH = re.compile(r"byte[\s-]?for[\s-]?byte|byte[\s-]?matching|matching bytes|matches? bytes|"
                      r"exact (?:match|reconstruction)|bit[\s-]?exact|(?:md5|sha[\s-]?(?:1|256|512))\b|"
                      r"non_matchings|decomp(?:ilation|pressed)? (?:percentage|progress|coverage|complete|ratio)|"
                      r"matching (?:rom|exe|dol|elf|binary|image)|"
                      r"matching decompilation|completely matching|fully matching|1:1 replica|"
                      r"compares? (?:the )?ram|ram (?:state )?(?:is |was )?compar\w*|"
                      r"compar\w* after (?:each|every) (?:frame|tick)|matches? the origino(?:al|u)|"
                      r"rebuilds? (?:a|the) (?:matching )?rom|playable from start to (?:end|finish)", re.I)
RE_COMPAT = re.compile(r"compat(?:ibility)? (?:table|matrix|list|status|doc)|"
                      r"\b\d+\s*(?:of|/)\s*\d+\b[^.\n]{0,60}\b(?:support|play|title|work)\w*\b|"
                      r"\b\d+\s+(?:supported|playable|working)\b", re.I)
RE_BOUNDARY = re.compile(r"no game (?:files|assets|content)|does not (?:include|ship|contain) any|"
                         r"bring your own|own (?:legally )?(?:obtained|licensed)? ?(?:copy|installation|"
                         r"disc|dump|rom)|baserom|requires? the original|must (?:provide|supply)|"
                         r"not (?:included|shipped)", re.I)
RE_PROGRESS = re.compile(r"\b(?:wip|work[- ]in[- ]progress|incomplete|not yet (?:complete|working)|"
                         r"playable|boot(?:s)? into|crash(?:es)?|unsupported)\b", re.I)
RE_NOISE = re.compile(r"^(?:\[?!\[|<img\b|\[[^\]]*\]:\s*\S)")
COMPAT_NAME = re.compile(r"compat|matrix|status|progress|checklist|support", re.I)

FLAG_LABEL = {"shell": "no source files in tree", "noreadme": "README unreadable",
              "archived": "archived", "nostars": "★ without forks or watchers",
              "emptydesc": "no description and no README claims"}


def gh(repo, path="", raw=False, timeout=25):
    cmd = ["curl", "-s", "--max-time", str(timeout)]
    if PROXY:
        cmd += ["-x", PROXY]
    if TOKEN:
        cmd += ["-H", f"Authorization: Bearer {TOKEN}"]
    if raw:
        cmd += ["-H", "Accept: application/vnd.github.raw"]
    out = subprocess.run(cmd + [f"https://api.github.com/repos/{repo}{path}"],
                         capture_output=True, text=True, check=False).stdout
    if raw:
        return out
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {}


def cache_path(repo):
    return CACHE / (repo.replace("/", "__") + ".json")


def fetch(repo, refresh=False):
    if not refresh:
        p = cache_path(repo)
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
    meta = gh(repo)
    if not meta.get("full_name"):
        return {}
    branch = meta.get("default_branch") or "HEAD"
    readme = gh(repo, "/readme", raw=True)
    tree = gh(repo, f"/git/trees/{branch}?recursive=1", timeout=120)
    names = [t.get("path", "") for t in tree.get("tree", [])] if tree.get("tree") else []
    status = "full" if names and not tree.get("truncated") else ("truncated" if names else "unknown")
    if status == "unknown":  # big repo or a slow answer: root listing plus the language bytes
        top = gh(repo, f"/git/trees/{branch}", timeout=45)
        names = [t.get("path", "") for t in top.get("tree", [])] if top.get("tree") else []
        status = "partial" if names else "none"
    langs = gh(repo, "/languages", timeout=45) if status != "full" else {}
    rec = {"repo": repo, "meta": {k: meta.get(k) for k in
           ("stargazers_count", "forks_count", "subscribers_count", "language", "size",
            "archived", "pushed_at", "created_at", "description", "license")},
           "readme_len": len(readme), "names": names, "tree_status": status,
           "tree_truncated": bool(tree.get("truncated")), "langs": langs,
           "readme_head": [line for line in readme.splitlines() if line.strip()][:400],
           "fetched": datetime.date.today().isoformat()}
    if not rec["tree_truncated"] and len(names) < 5000:
        rec["readme_snips"] = ""  # quotes come from readme_head, kept small on purpose
    CACHE.mkdir(parents=True, exist_ok=True)
    p = cache_path(repo)
    p.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
    if not names:  # the tree call may have failed while the rest worked
        rec["names"] = []
    return rec


def sentence(text, rx):
    for line in text.splitlines():
        s = line.strip()
        if not s or RE_NOISE.match(s):
            continue
        if rx.search(s):
            return re.sub(r"\s+", " ", s)[:200]
    return ""


def analyse(repo, refresh=False):
    rec = fetch(repo, refresh)
    if not rec:
        return {"repo": repo, "verdict": "dead", "flags": ["404"], "quote": "", "e": "",
                "stars": 0, "forks": 0, "watchers": 0, "pushed": "", "src": 0, "files": 0}
    m = rec["meta"]
    names = rec["names"]
    status = rec.get("tree_status", "full")
    langs = rec.get("langs") or {}
    low = [n.lower() for n in names]
    src = sum(1 for n in names if os.path.splitext(n)[1].lower() in SOURCE_EXT)
    has_ci = any(n.startswith(".github/workflows/") or n == ".github" for n in low)
    has_build = any(os.path.basename(n) in BUILD_FILES or n.endswith((".sln", ".vcxproj", ".xcodeproj"))
                    for n in low)
    compat_file = any(COMPAT_NAME.search(os.path.basename(n)) and n.endswith((".md", ".rst", ".txt", ".json"))
                      for n in names)
    text = "\n".join(rec["readme_head"])
    e1 = sentence(text, RE_MATCH)
    e2 = sentence(text, RE_COMPAT) or ("compatibility/progress table ships in the tree"
                                      if compat_file else "")
    e3 = ""
    if has_ci:
        e3 = "CI: " + next((n for n in low if n.startswith(".github/workflows/") or n == ".github"), "")
    elif has_build:
        e3 = "build: " + next((os.path.basename(n) for n in low
                               if os.path.basename(n) in BUILD_FILES
                               or n.endswith((".sln", ".vcxproj"))), "")
    e4 = sentence(text, RE_BOUNDARY)
    if not e3 and status != "full":  # the tree was unreadable, so ask releases instead
        e3 = ("releases: yes" if gh(repo, "/releases?per_page=1") else "")
    prog = sentence(text, RE_PROGRESS)
    flags = []
    if src == 0 and not langs and status in ("none", "full") and (m.get("size") or 0) < 60:
        flags.append("shell")
    if status in ("none", "partial"):
        flags.append("tree-" + status)
    if rec["readme_len"] == 0:
        flags.append("noreadme")
    if m.get("archived"):
        flags.append("archived")
    if (m.get("stargazers_count") or 0) > 30 and not (m.get("forks_count") or 0) and \
       not (m.get("subscribers_count") or 0):
        flags.append("nostars")
    ev = sum(bool(x) for x in (e1, e2, e3, e4))
    if "shell" in flags or "noreadme" in flags or "archived" in flags:
        verdict = "exclude"
    elif e1 or e2:
        verdict = "eligible"
    elif e3 or e4:
        verdict = "conditional"
    else:
        verdict = "watch"
    return {"repo": repo, "stars": m.get("stargazers_count") or 0,
            "forks": m.get("forks_count") or 0, "watchers": m.get("subscribers_count") or 0,
            "pushed": (m.get("pushed_at") or "")[:10], "lang": m.get("language") or "",
            "size_kb": m.get("size") or 0, "src": src, "files": len(names),
            "e": f"E1{'x' if e1 else '-'}E2{'x' if e2 else '-'}E3{'x' if e3 else '-'}E4{'x' if e4 else '-'}",
            "evidence": ev, "quote": (e1 or e2 or e4 or e3 or prog)[:200],
            "flags": flags, "verdict": verdict}


def from_readme(limit=0):
    text = README.read_text(encoding="utf-8")
    out = []
    for s in SLUG.findall(text):
        if s.lower() not in [o.lower() for o in out]:
            out.append(s)
    return out[:limit] if limit else out


def from_file(path, limit=0):
    rows = [l.strip() for l in Path(path).read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")]
    return rows[:limit] if limit else rows


def from_aggregate(path, band=(0, 10 ** 9), sample=0, seed=42):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = d if isinstance(d, list) else d.get("games") or d.get("data") or []
    ours = {s.lower() for s in from_readme()}
    out = []
    for r in rows:
        if r.get("inactive"):
            continue
        m = SLUG.search(r.get("url") or "")
        if not m or m.group(1).lower() in ours:
            continue
        try:
            stars = int(r.get("stars") or 0)
        except (TypeError, ValueError):
            stars = 0
        if band[0] <= stars <= band[1]:
            out.append(m.group(1))
    seen, uniq = set(), []
    for s in out:
        if s.lower() not in seen:
            seen.add(s.lower())
            uniq.append(s)
    if sample:
        uniq = random.Random(seed).sample(uniq, min(sample, len(uniq)))
    return uniq


def report(res, out_path=None):
    from collections import Counter
    c = Counter(r["verdict"] for r in res)
    print("\n".join(f"  {k:12} {v}" for k, v in sorted(c.items(), key=lambda kv: -kv[1])))
    fl = Counter(f for r in res for f in r["flags"])
    if fl:
        print("  flags: " + ", ".join(f"{FLAG_LABEL.get(k, k)}={v}" for k, v in fl.most_common()))
    ev = Counter(r["evidence"] for r in res)
    print("  evidence count histogram: " + ", ".join(f"{k}:{ev[k]}" for k in sorted(ev)))
    print(f"\n  {'repo':44} {'★':>7} {'verdict':12} {'E':16} quote")
    for r in sorted(res, key=lambda x: (x["verdict"], -x["stars"]))[:40]:
        print(f"  {r['repo'][:44]:44} {r['stars']:>7,} {r['verdict']:12} {r['e']:16} {r['quote'][:70]}")
    if out_path:
        cols = ["repo", "verdict", "stars", "forks", "watchers", "pushed", "lang", "size_kb",
                "src", "files", "e", "evidence", "flags", "quote"]
        with open(out_path, "w", newline="", encoding="utf-8") as fh:
            w = csv_writer(fh, cols)
            for r in res:
                w.append(r)
        print(f"\nwrote {out_path}")


def csv_writer(fh, cols):
    import csv

    class W:
        def __init__(self, fh, cols):
            self.w = csv.writer(fh, delimiter="\t")
            self.cols = cols
            self.w.writerow(cols)

        def append(self, r):
            self.w.writerow([r.get(c, "") if not isinstance(r.get(c), list)
                             else "+".join(r[c]) for c in self.cols])

    return W(fh, cols)


def main():
    ap = argparse.ArgumentParser(prog="quality.py", description=__doc__.splitlines()[0])
    ap.add_argument("command", choices=["check"])
    ap.add_argument("--repos", help="file with one owner/repo per line")
    ap.add_argument("--aggregate", help="data/games.json-style dump to sample instead")
    ap.add_argument("--band", default="0:1000000000", help="star window MIN:MAX for --aggregate")
    ap.add_argument("--sample", type=int, default=0)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--refresh", action="store_true", help="ignore the cache")
    ap.add_argument("--out", default="", help="TSV to write")
    ap.add_argument("--workers", type=int, default=4 if TOKEN else 1)
    a = ap.parse_args()
    if a.aggregate:
        lo, hi = (int(x) for x in a.band.split(":"))
        repos = from_aggregate(a.aggregate, (lo, hi), a.sample)
    elif a.repos:
        repos = from_file(a.repos, a.limit)
    else:
        repos = from_readme(a.limit)
    if not TOKEN:
        print("no GITHUB_TOKEN: serialised and throttled", file=sys.stderr)
    print(f"checking {len(repos)} repositories, {len(set(r.lower() for r in repos))} unique"
          f"{' (cached run, 0 requests)' if all(cache_path(r).exists() for r in repos) else ''}")
    res = []
    with ThreadPoolExecutor(max_workers=max(1, a.workers)) as ex:
        for i, r in enumerate(ex.map(lambda x: analyse(x, a.refresh), repos), 1):
            res.append(r)
            if i % 25 == 0:
                print(f"  ... {i}/{len(repos)}", file=sys.stderr, flush=True)
    report(res, a.out or None)


if __name__ == "__main__":
    main()
