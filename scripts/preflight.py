#!/usr/bin/env python3
"""Stage 1 of intake: turn a set of slugs into a measured, pre-screened work queue.

  python3 scripts/preflight.py --repo owner/repo [--repo …]          # a hand suggestion
  python3 scripts/preflight.py --repos FILE                          # one owner/repo per line
  python3 scripts/preflight.py --aggregate FILE --band 100:999       # a data/games.json-style dump

Writes `data/measurement/candidates-<date>.tsv` (gitignored) and prints the tally. Nothing is admitted here:
a row says what a repository measures at, whether the API already settles its class, and what the
next verb is. `blocked_on`, `verdict`, `e`, `flags` and `quote` are stage 2's and are left blank.

A slug is written only after `GET /repos/{owner}/{repo}` answers 200, so a guessed URL cannot enter
the queue — which is all stage 1 costs: **one request per candidate**, no README and no file tree.
Stage 2 pays for the README and tree through `quality.py`, once, only for the rows it actually reads.

Priority is the rationing field, not an admission test (INTAKE.md, `## The three stages and the three files`):
P1 ★≥1,000 or ★≥100 pushed within 90 days · P2 ★≥100, or ★≥10 within 90 days · P3 ★≥10 · P4 the rest.
"""
import argparse
import csv
import datetime
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import quality as q  # noqa: E402  stage 2's evidence tool; stage 1 shares its cache and its screen

HERE = Path(__file__).resolve().parent
MEAS = HERE.parent / "data" / "measurement"
COLUMNS = ["slug", "source", "priority", "stars", "forks", "watchers", "pushed", "created", "lang",
           "size_kb", "license", "archived", "upstream_type", "precheck", "blocked_on", "verdict",
           "e", "flags", "quote", "next"]
RECENT_DAYS = 90
SCREEN_NEXT = {"already-entered": "nothing — the reader already has it through one entry",
               "fork-of-entered": "write its facts into the parent entry's paragraph, then refuse it"}


def priority(stars, pushed, today=None):
    """The ★×recency band: orders the queue and decides how many rows a pass reads. Nothing else."""
    today = today or datetime.date.today()
    try:
        age = (today - datetime.date.fromisoformat((pushed or "")[:10])).days
    except ValueError:
        age = 10 ** 9
    if stars >= 1000 or (stars >= 100 and age <= RECENT_DAYS):
        return "P1"
    if stars >= 100 or (stars >= 10 and age <= RECENT_DAYS):
        return "P2"
    return "P3" if stars >= 10 else "P4"


def row(slug, meta, source, upstream_type="", today=None):
    """One candidate row, from the metadata call that established the slug exists."""
    stars = meta.get("stargazers_count") or 0
    pushed = (meta.get("pushed_at") or "")[:10]
    cls, _settled = q.precheck(slug, q.parent_of(meta))
    return {"slug": meta.get("full_name") or slug, "source": source,
            "priority": priority(stars, pushed, today), "stars": stars,
            "forks": meta.get("forks_count") or 0, "watchers": meta.get("subscribers_count") or 0,
            "pushed": pushed, "created": (meta.get("created_at") or "")[:10],
            "lang": meta.get("language") or "", "size_kb": meta.get("size") or 0,
            "license": (meta.get("license") or {}).get("spdx_id") or "",
            "archived": bool(meta.get("archived")), "upstream_type": upstream_type,
            "precheck": cls, "blocked_on": "", "verdict": "", "e": "", "flags": "", "quote": "",
            "next": SCREEN_NEXT.get(cls, "read its README for the method claim")}


def candidates(a):
    """The slug queue, plus the upstream `type` hint where a source supplies one."""
    if a.aggregate:
        dump = json.loads(Path(a.aggregate).read_text(encoding="utf-8"))
        rows = dump if isinstance(dump, list) else dump.get("games") or dump.get("data") or []
        hint = {}
        for r in rows:
            m = q.SLUG.search(r.get("url") or "")
            if m:
                hint.setdefault(m.group(1).lower(), r.get("type") or "")
        lo, hi = (int(x) for x in a.band.split(":"))
        return q.from_aggregate(a.aggregate, (lo, hi), a.sample), "catalogue", hint
    if a.repos:
        return q.from_file(a.repos, a.limit), "search", {}
    return list(a.repo), "owner", {}


def main():
    ap = argparse.ArgumentParser(prog="preflight.py", description=__doc__.splitlines()[0])
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--repo", action="append", default=[], help="a hand-named repository")
    src.add_argument("--repos", help="file with one owner/repo per line")
    src.add_argument("--aggregate", help="data/games.json-style dump to pull slugs from")
    ap.add_argument("--band", default="0:1000000000", help="star window MIN:MAX for --aggregate")
    ap.add_argument("--sample", type=int, default=0, help="deterministic subset of the band")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--source", choices=("search", "catalogue", "owner"),
                    help="how the candidate reached us (default depends on the input)")
    ap.add_argument("--out", help="TSV path (default data/measurement/candidates-<date>.tsv)")
    a = ap.parse_args()

    slugs, kind, hint = candidates(a)
    kind = a.source or kind
    today = datetime.date.today()
    MEAS.mkdir(parents=True, exist_ok=True)
    out_path = Path(a.out) if a.out else MEAS / f"candidates-{today.isoformat()}.tsv"
    print(f"{len(slugs)} candidates ({kind}), measuring before writing…")

    written, skipped = [], Counter()
    for i, slug in enumerate(slugs, 1):
        meta = q.gh(slug)
        if not meta.get("full_name"):
            skipped["no 200"] += 1
            print(f"  no 200: {slug}")
            continue
        written.append(row(slug, meta, kind, hint.get(slug.lower(), ""), today))
        if i % 25 == 0:
            print(f"  ... {i}/{len(slugs)}", file=sys.stderr, flush=True)

    written.sort(key=lambda r: (r["priority"], -r["stars"], r["slug"].lower()))
    with out_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, delimiter="\t", fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(written)

    pc, pr = Counter(r["precheck"] for r in written), Counter(r["priority"] for r in written)
    print(f"\nwrote {out_path}: {len(written)} rows"
          + (", skipped " + ", ".join(f"{k}:{v}" for k, v in skipped.items()) if skipped else ""))
    print("  priority: " + " · ".join(f"{p}={pr.get(p, 0)}" for p in ("P1", "P2", "P3", "P4")))
    print("  precheck: " + " · ".join(f"{c}={n}" for c, n in pc.most_common()))
    print(f"  {pc.get('pass', 0)} row(s) still need the README read for the method claim; "
          "a pass takes P1 in full and P2 as far as time goes")


if __name__ == "__main__":
    main()
