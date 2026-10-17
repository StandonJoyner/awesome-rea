#!/usr/bin/env python3
"""Append one audited line to `decisions.jsonl` — the record of what was refused, deferred or removed.

  python3 scripts/decide.py refuse --slug owner/repo --blocked-on A1 \\
      --quote "Arx Libertatis is based on the publicly released Arx Fatalis source code" \\
      --read-at README.md --note "vendor source, compiled and continued"
  python3 scripts/decide.py remove --slug owner/repo --blocked-on gone \\
      --quote "GET /repos/owner/repo -> 404" --read-at scripts/verify.py --note "confirmed by verify.py links"

Seven keys, always in this order: `date slug decision blocked_on quote read_at note`. `admit` is
written by `merge.py`, which has the quote from the pending object; this script writes the other five:
refuse · defer · wording-fix · remove. A refusal with no `quote` and no `read_at` is not a refusal,
it is a hunch, so the script exits 2 rather than append it.

The file is append-only: a corrected decision is a new line, never an edit of an old one.
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = HERE.parent / "data" / "decisions.jsonl"
KEYS = ["date", "slug", "decision", "blocked_on", "quote", "read_at", "note"]
DECISIONS = ("admit", "refuse", "defer", "wording-fix", "remove")
BLOCKS = ("A1", "A2", "A3", "filing", "none")
REMOVALS = ("gone", "taken-down", "class-no-longer-met", "claim-falsified")


def validate(rec):
    """The rule the ledger exists to keep: a rejection names the test and the sentence read."""
    d = rec["decision"]
    if d not in DECISIONS:
        return f"decision must be one of {' · '.join(DECISIONS)}"
    if not rec["slug"].strip():
        return "a decision without a slug decides nothing"
    if d == "refuse":
        if rec["blocked_on"] not in ("A1", "A2", "A3"):
            return f"refuse must name the A-test it failed, not {rec['blocked_on']!r}"
        if not rec["quote"].strip() or not rec["read_at"].strip():
            return "a refusal needs the sentence actually read and the file it was read from"
    if d == "defer":
        if rec["blocked_on"] not in ("A1", "A2", "A3", "filing", "none"):
            return f"defer names an A-test or none, not {rec['blocked_on']!r}"
        if not rec["note"].strip():
            return "a deferral must say what it is waiting for, or whose editorial call it is"
    if d == "remove" and rec["blocked_on"] not in REMOVALS:
        return f"remove must name one of {' · '.join(REMOVALS)}"
    if d == "wording-fix" and not rec["note"].strip():
        return "a wording-fix line must say what changed"
    if rec["blocked_on"] not in BLOCKS + REMOVALS:
        return f"blocked_on must be one of {' · '.join(BLOCKS)}"
    return ""


def main():
    ap = argparse.ArgumentParser(prog="decide.py", description=__doc__.splitlines()[0])
    ap.add_argument("decision", choices=DECISIONS)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--blocked-on", default="none")
    ap.add_argument("--quote", default="", help="the sentence actually read, verbatim")
    ap.add_argument("--read-at", default="", help="which file or endpoint it was read from")
    ap.add_argument("--note", default="")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--out", default=str(LOG))
    a = ap.parse_args()

    rec = {"date": a.date, "slug": a.slug, "decision": a.decision, "blocked_on": a.blocked_on,
           "quote": a.quote, "read_at": a.read_at, "note": a.note}
    if err := validate(rec):
        sys.exit(f"refusing to write: {err}")
    with open(a.out, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"appended {a.decision} {a.slug} to {Path(a.out).name}")


if __name__ == "__main__":
    main()
