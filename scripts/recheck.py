#!/usr/bin/env python3
"""Re-review the entered corpus: four machine checks, and one column that says who acts.

  recheck                  — check every repository linked from README.md
  recheck --dmca-refresh   — fetch github/dmca into scripts/.dmca-cache/dmca first
  recheck --no-dmca        — skip the notices check (the only check that needs the clone)

Reads the newest `scripts/snapshot-<date>.tsv` written by `verify.py refresh` and refuses to
conclude from a snapshot older than --max-age days (31). It therefore costs zero API requests
unless a repository linked in the README has no snapshot row, which is confirmed with one
`GET /repos/{owner}/{repo}`; it costs one local scan of the notices clone otherwise.

  gone    a linked repository returns 404                      -> fix
  stale   ★ >= --floor (1000) and no push for --quiet (365) days -> read
  lic     the licence word in our entry line vs the API field  -> read, unless hedged -> none
  dmca    the owner token and the repo token in one notice file -> read

A row with no flag is still written: the file is the record that a pass happened, not a
list of complaints. Nothing here deletes an entry by itself; the `need` column only says
whether a person or an agent has to look.
"""
import argparse
import csv
import datetime
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
README = ROOT / "README.md"
DMCA = HERE / ".dmca-cache" / "dmca"
DMCA_URL = "https://github.com/github/dmca"
ENTRY = re.compile(r"^- \[[^\]]+\]\(https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\) - (.*)$")
LIC = re.compile(r"\b(AGPL-3\.0|GPL-3\.0|GPL-2\.0|LGPL-2\.1|LGPL-3\.0|Apache-2\.0|CC0-1\.0|"
                 r"BSD-\d-Clause|MPL-2\.0|MIT|ISC|Zlib)\b|\bno licen[cs]e declared\b", re.I)
HEDGE = re.compile(r"-style|with additional terms|if declared|licence unknown|no licence", re.I)
TOKEN = re.compile(r"[a-z0-9][a-z0-9_.-]*")
NEED_ORDER = {"fix": 0, "read": 1, "none": 2}


def gh_get(repo):
    """Return the HTTP status of GET /repos/{repo}: the only request this script may spend."""
    cmd = ["curl", "-s", "--max-time", "25", "-o", "/dev/null", "-w", "%{http_code}",
           f"https://api.github.com/repos/{repo}"]
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        cmd.insert(4, "-H")
        cmd.insert(5, f"Authorization: Bearer {token}")
    proxy = os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")
    if proxy:
        cmd.insert(4, "-x")
        cmd.insert(5, proxy)
    return subprocess.run(cmd, capture_output=True, text=True, check=False).stdout.strip() or "000"


def entries():
    """Entry bullets the reader can act on: `Related lists` holds lists, whose push age is
    not a claim we make, so its rows are not re-reviewed."""
    rows, section = {}, ""
    for line in README.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            section = line.lstrip("#").strip()
            continue
        m = ENTRY.match(line)
        if m and section != "Related lists":
            slug = m.group(1)
            rows.setdefault(slug.lower(), {"slug": slug, "line": m.group(2)})
    return rows


def newest_snapshot(max_age):
    paths = sorted(HERE.glob("snapshot-*.tsv"))
    if not paths:
        sys.exit("no scripts/snapshot-<date>.tsv — run verify.py refresh first")
    date = paths[-1].stem.split("snapshot-")[1]
    age = (datetime.date.today() - datetime.date.fromisoformat(date)).days
    if age > max_age:
        sys.exit(f"newest snapshot is {date}, {age}d old (> --max-age {max_age}) — refresh first")
    out = {}
    for r in csv.DictReader(paths[-1].open(encoding="utf-8"), delimiter="\t"):
        out[r["repo"].lower()] = r
    return date, out


def scan_dmca(slugs):
    """Owner token AND repo token in one notice file. A notice names the repositories it
    removed, which is often a fork of the project we entered, so a hit is only a lead to read."""
    if not DMCA.is_dir():
        return None
    by_repo = {}
    for slug in slugs:
        by_repo.setdefault(slug.lower().split("/")[1], set()).add(slug.lower())
    hits = {}
    for path in DMCA.rglob("*.md"):
        try:
            low = path.read_text(encoding="utf-8", errors="replace").lower()
        except OSError:
            continue
        found = set(TOKEN.findall(low))
        for repo in found & set(by_repo):
            for slug in by_repo[repo]:
                owner = slug.split("/")[0].lower()
                if owner in found:
                    hits.setdefault(slug, []).append(
                        (str(path.relative_to(DMCA)), f"github.com/{owner}/{repo}" in low))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dmca-refresh", action="store_true")
    ap.add_argument("--no-dmca", action="store_true")
    ap.add_argument("--floor", type=int, default=1000)
    ap.add_argument("--quiet", type=int, default=365)
    ap.add_argument("--max-age", type=int, default=31)
    a = ap.parse_args()

    if a.dmca_refresh:
        DMCA.parent.mkdir(exist_ok=True)
        if DMCA.is_dir():
            subprocess.run(["git", "-C", str(DMCA), "pull", "--ff-only", "--depth", "1"], check=False)
        else:
            subprocess.run(["git", "clone", "--quiet", "--depth", "1", "--single-branch",
                            DMCA_URL, str(DMCA)], check=False)

    snap_date, snap = newest_snapshot(a.max_age)
    rows = entries()
    hits = None if a.no_dmca else scan_dmca([r["slug"].lower() for r in rows.values()])
    today = datetime.date.today()
    out = []
    for slug, e in sorted(rows.items(), key=lambda kv: kv[0]):
        s = snap.get(slug)
        flags, details, need = [], [], "none"

        def hit(code, detail, want):
            nonlocal need
            flags.append(code)
            details.append(detail)
            if NEED_ORDER[want] < NEED_ORDER[need]:
                need = want

        if s is None:
            code = gh_get(e["slug"])
            if code == "404":
                hit("gone", "HTTP 404", "fix")
            else:
                hit("err", f"HTTP {code}, not in the {snap_date} snapshot", "read")
            stars, pushed, field = 0, "", ""
        else:
            stars, pushed, field = int(s["stars"]), s["pushed"], (s["license"] or "").strip()
            age = (today - datetime.date.fromisoformat(pushed)).days if pushed else 10_000
            if stars >= a.floor and age > a.quiet:
                hit("stale", f"{age}d", "read")
        m = LIC.search(e["line"])
        word = m.group(0) if m else ""
        hedged = bool(HEDGE.search(e["line"]))
        if word and field and not hedged:
            declared = word.lower().replace("licence", "license")
            if field in ("null", "") and "no license" not in declared:
                hit("lic", f"line={word} field=null", "read")
            elif field == "NOASSERTION":
                hit("lic", f"line={word} field=NOASSERTION", "read")
            elif field not in ("null", "") and field.lower() != declared:
                hit("lic", f"line={word} field={field}", "read")
        if hits is not None and slug in hits:
            paths = sorted(set(p for p, _ in hits[slug]))
            strong = any(s for _, s in hits[slug])
            hit("dmca", ",".join(paths[:3]) + ("" if strong else " [weak: no github.com/owner/repo]"),
                "read")
        status = "gone" if "gone" in flags else "err" if "err" in flags else "ok"
        out.append({"repo": e["slug"], "status": status, "stars": stars, "pushed": pushed,
                    "flags": ";".join(flags), "detail": ";".join(details), "need": need})

    date = today.isoformat()
    path = HERE / f"recheck-{date}.tsv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, delimiter="\t",
                           fieldnames=["repo", "status", "stars", "pushed", "flags", "detail", "need"])
        w.writeheader()
        for r in sorted(out, key=lambda r: (NEED_ORDER[r["need"]], -r["stars"])):
            w.writerow(r)

    errs = sum(1 for r in out if "err" in r["flags"])
    acts = [r for r in out if r["need"] != "none"]
    print(f"recheck {date} on snapshot {snap_date}: {len(out)} entries, "
          f"{len(acts)} need action, {errs} errored")
    for code in ("gone", "stale", "lic", "dmca", "err"):
        n = sum(1 for r in out if any(x == code for x in r["flags"].split(";")))
        if n:
            print(f"  {code:<11} {n}")
    for r in acts:
        print(f"  {r['need']:<5} ★{r['stars']:>7}  {r['repo']:<38} {r['flags']:<22} {r['detail']}")
    if hits is None:
        print("  dmca: not checked (clone missing or --no-dmca; run --dmca-refresh)")
    if out and errs / len(out) > 0.05:
        print("more than 5% of rows errored — treat this pass as partial")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
