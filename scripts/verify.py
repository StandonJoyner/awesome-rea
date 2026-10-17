#!/usr/bin/env python3
"""Re-derive the numbers in the READMEs.

  links            — HEAD/GET every URL in both READMEs (no API quota spent)
  refresh          — measure every linked repo again with GET /repos/{owner}/{repo}
  refresh --apply  — additionally rewrite the measured tokens in both READMEs

refresh writes data/measurement/snapshot-<date>.tsv and prints the star delta against the newest
older snapshot, plus any slug that no longer resolves.

--apply only rewrites `★ <n>`, `<n> forks` and `pushed <date>` on entry bullets, plus the
refreshed-date line. It never touches `created <date>`, prose, or descriptions.
GITHUB_TOKEN (or GH_TOKEN) removes the inter-request sleep; anonymous runs are throttled.
"""
import csv
import datetime
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MEAS = ROOT / "data" / "measurement"
README = ROOT / "README.md"
ZH = ROOT / "README.zh-CN.md"
SLUG = re.compile(r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)")
URL = re.compile(r"https?://[^\s)\[\]\"'<>]+")
DELAY = 7.0  # anonymous GitHub search/core is per-IP; stay under the limit
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

ENTRY = re.compile(r"^- \[[^\]]*\]\(https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\)")
STAR = re.compile(r"★ (\d{1,3}(?:,\d{3})*)")
FORK = re.compile(r"(\d{1,3}(?:,\d{3})*) forks?\b")
PUSH = re.compile(r"(last push|pushed|推送于|最近推送) (\d{4}-\d{2}-\d{2})")
REFRESHED = re.compile(r"(Data last refreshed|数据刷新于) (\d{4}-\d{2}-\d{2})")


def gh(repo, proxy=None, path=""):
    cmd = ["curl", "-s", "--max-time", "20"]
    if proxy:
        cmd += ["-x", proxy]
    if TOKEN:
        cmd += ["-H", f"Authorization: Bearer {TOKEN}"]
    out = subprocess.run(cmd + [f"https://api.github.com/repos/{repo}{path}"],
                         capture_output=True, text=True, check=False).stdout
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {}


def readmes():
    return "\n".join(p.read_text(encoding="utf-8") for p in (README, ZH) if p.exists())


def _probe(u, proxy=None):
    cmd = ["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "20", "-L",
           "-A", "Mozilla/5.0 (X11; Linux x86_64) verifyscript"]
    if proxy:
        cmd += ["-x", proxy]
    return subprocess.run(cmd + [u], capture_output=True, text=True, check=False)


def links(proxy=None):
    bad = []
    quiet = []
    urls = sorted(set(URL.findall(readmes())))
    for u in urls:
        p = _probe(u, proxy)
        if p.stdout == "200":
            continue
        # 000 is a transport failure (bot wall, TLS, timeout) — not a dead link.
        (quiet if p.stdout == "000" else bad).append(f"{p.stdout} {u} {p.stderr.strip()[:60]}")
    for b in bad:
        print(f"DEAD  {b}")
    for q in quiet:
        print(f"WALL  {q}")
    ok = len(urls) - len(bad) - len(quiet)
    print(f"{ok} ok / {len(quiet)} unreachable-not-verifiable / {len(bad)} dead  ({len(urls)} total)")
    return 1 if bad else 0


def patch_line(line, repo, data, fork_word="forks"):
    """Return (new_line, [changes]) for one entry bullet."""
    changes = []
    stars = f"{data['stars']:,}"
    forks = f"{data['forks']:,}"
    word = fork_word if data["forks"] != 1 else "fork"

    def sub_stars(m):
        if m.group(1) != stars:
            changes.append(f"★ {m.group(1)} -> ★ {stars}")
        return f"★ {stars}"

    line = STAR.sub(sub_stars, line)

    def sub_forks(m):
        if data["forks"] is None or (m.group(1) == forks and m.group(0).endswith(word)):
            return m.group(0)
        changes.append(f"{m.group(0)} -> {forks} {word}")
        return f"{forks} {word}"

    line = FORK.sub(sub_forks, line)

    def sub_push(m):
        if not data["pushed"] or m.group(2) == data["pushed"]:
            return m.group(0)
        changes.append(f"{m.group(1)} {m.group(2)} -> {m.group(1)} {data['pushed']}")
        return f"{m.group(1)} {data['pushed']}"

    return PUSH.sub(sub_push, line), changes


def apply_to(path, data, date, fork_word="forks"):
    if not path.exists():
        return 0
    lines = path.read_text(encoding="utf-8").split("\n")
    n = 0
    for i, line in enumerate(lines):
        if REFRESHED.search(line):
            new, cnt = REFRESHED.subn(lambda m: f"{m.group(1)} {date}", line, count=1)
            if cnt:
                lines[i] = new
                n += 1
            continue
        if not ENTRY.match(line):
            continue
        repo = SLUG.search(line).group(1)
        if repo not in data:
            continue
        new, changes = patch_line(line, repo, data[repo], fork_word)
        if changes:
            lines[i] = new
            n += len(changes)
            for c in changes:
                print(f"patch {path.name}:{i + 1} {repo} {c}")
    if n:
        path.write_text("\n".join(lines), encoding="utf-8")
    return n


def refresh(proxy=None, apply=False):
    repos = sorted(set(SLUG.findall(readmes())))
    date = datetime.date.today().isoformat()
    rows = []
    for i, repo in enumerate(repos, 1):
        d = gh(repo, proxy)
        if not d.get("full_name"):
            print(f"MISSING {repo}")
            continue
        rows.append({"snapshot": date, "repo": d["full_name"], "stars": d["stargazers_count"],
                     "forks": d["forks_count"], "pushed": (d.get("pushed_at") or "")[:10],
                     "archived": d.get("archived"), "license": (d.get("license") or {}).get("spdx_id")})
        print(f"[{i}/{len(repos)}] {d['stargazers_count']:>8}  {d['full_name']}")
        if i < len(repos) and not TOKEN:
            time.sleep(DELAY)
    if not rows:
        print("nothing measured — quota or network")
        return 1
    MEAS.mkdir(parents=True, exist_ok=True)
    out = MEAS / f"snapshot-{date}.tsv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, delimiter="\t", fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    prior = sorted(MEAS.glob("snapshot-*.tsv"))
    if len(prior) >= 2:
        old = {r["repo"]: int(r["stars"]) for r in
               csv.DictReader(prior[-2].open(encoding="utf-8"), delimiter="\t")}
        for r in rows:
            if r["repo"] in old:
                d = r["stars"] - old[r["repo"]]
                if d:
                    print(f"delta {d:+d} {r['repo']} ({old[r['repo']]} -> {r['stars']})")
    print(f"wrote {out}")
    if apply:
        data = {r["repo"]: r for r in rows}
        n = apply_to(README, data, date) + apply_to(ZH, data, date, fork_word="fork")
        print(f"applied {n} token change(s) to the READMEs; refreshed date {date}")
    return 0


if __name__ == "__main__":
    argv = [a for a in sys.argv[1:] if a != "--apply"]
    do_apply = "--apply" in sys.argv[1:]
    mode = argv[0] if argv else "links"
    proxy = argv[1] if len(argv) > 1 else None
    if mode == "links":
        sys.exit(links(proxy))
    if mode == "refresh":
        sys.exit(refresh(proxy, do_apply))
    print(__doc__)
    sys.exit(2)
