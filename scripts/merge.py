#!/usr/bin/env python3
"""Stage 3 of intake: merge accepted entries into the corpus and log what entered.

  python3 scripts/merge.py pending-<date>.json            # merge into entries.json
  python3 scripts/merge.py pending-<date>.json --dry-run  # report the plan, write nothing
  python3 scripts/merge.py --coverage                    # stage 2's gate: every read owes a disposition
  python3 scripts/merge.py pending-<date>.json --corpus /tmp/entries.json --out /tmp/entries.json \
       --decisions /tmp/decisions.jsonl                   # the same run against a copy of the corpus
  python3 scripts/merge.py pending-<date>.json --out /tmp/entries.json --decisions /tmp/d.jsonl
                                                          # the same run against a copy

The pending file is an array of entry objects in the same shape `entries.json` stores, which is why
a merge inserts rather than translates: a filled token has to name the `measured` field it prints and
carry that placeholder in both languages, and a literal one has to carry neither. Numbers are **not** taken from the pending
object: `measured` is copied from the newest `data/measurement/snapshot-<date>.tsv`, or — for a slug
too new to be in it, since `verify.py refresh` measures what the two READMEs already link — from the
newest `data/measurement/candidates-<date>.tsv`. Both are `GET /repos/{owner}/{repo}` output, so a
figure can only be what that endpoint reported.

What it refuses to merge, each with a reason — and one problem stops the whole file, because a
pending file is committed with a PR and a half-merged batch is not reviewable:
  · a slug already in the corpus — an update is a `wording-fix` decision, not a second entry;
  · a missing or unreadable numbers row — no figure is invented;
  · no `admission.a2_quote` or `a2_read_at` — A2 is the sentence actually read, and an entry without
    it is a lead in WATCHLIST.md;
  · a `method` outside M1–M4, an `assets` value outside the three, a token kind outside the four, a
    token whose `field` or `{placeholder}` disagrees with its kind or is worded in one language only;
  · a `section` or `platform` with no heading in both READMEs — a new filing level is an editorial
    decision made in the READMEs first (INTAKE.md `## Filing axis`).

`--coverage` is the other half of the same discipline, and it exists because a read that ends as chat
leaves no trace. `quality.py read` appends every candidate it shows to `data/measurement/read-<date>.tsv`,
so that file is the list of repositories somebody actually opened; the gate holds each slug to one of
three dispositions — already in the corpus, in the pending file it is given, or named by a line in
`decisions.jsonl` — and exits 1 printing the rows that have none. `INTAKE.md` says a rejection *is* a
ledger line; this is what makes that sentence checkable instead of aspirational.

New rows are positioned by star count inside their section, descending, without moving the rows that
are already there: order is a courtesy, and re-sorting an existing section would rewrite the README
for no reader-visible reason. After a merge, run `python3 scripts/render.py` — the two READMEs are
output, never hand-edited — and the merge commit removes the pending file.
"""
import argparse
import csv
import datetime
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MEAS = ROOT / "data" / "measurement"
DATA = ROOT / "data"
REQUIRED = ("slug", "section", "desc", "tokens")
METHODS = ("M1", "M2", "M3", "M4")
ASSETS = ("reader-supplied", "shipped", "none-needed")
TOKEN_KINDS = ("stars", "forks", "pushed", "literal")


def read_tsv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def newest_snapshot():
    files = sorted(MEAS.glob("snapshot-*.tsv"))
    if not files:
        sys.exit("no snapshot-<date>.tsv in data/measurement/ — run verify.py refresh first")
    return files[-1].stem.split("-", 1)[1], {r["repo"].lower(): r for r in read_tsv(files[-1])}


def newest_candidates():
    """Stage 1's file, keyed by `slug` instead of `repo`: the only numbers a *new* entry can have.

    `verify.py refresh` measures the slugs already linked in the two READMEs, so a candidate has no
    snapshot row until it enters. Its figures come from the same `GET /repos/{owner}/{repo}` call,
    which stage 1 wrote before anyone read the repository.
    """
    files = sorted(MEAS.glob("candidates-*.tsv"))
    if not files:
        return "", {}
    return files[-1].stem.split("-", 1)[1], {r["slug"].lower(): r for r in read_tsv(files[-1])}


def check(entry, problems):
    """One candidate object, judged against the schema, before anything is written."""
    for k in REQUIRED:
        if not entry.get(k):
            problems.append(f"{entry.get('slug', '?')}: missing {k}")
    for lang in ("en", "zh"):
        if not (entry.get("desc") or {}).get(lang, "").strip():
            problems.append(f"{entry.get('slug', '?')}: desc.{lang} is empty")
    adm = entry.get("admission") or {}
    if not (adm.get("a2_quote") or "").strip() or not (adm.get("a2_read_at") or "").strip():
        problems.append(f"{entry.get('slug', '?')}: no a2_quote/a2_read_at — fails A2 as an entry, "
                        "so it is a lead in WATCHLIST.md")
    if entry.get("method") not in METHODS:
        problems.append(f"{entry.get('slug', '?')}: method must be one of {' · '.join(METHODS)}")
    if entry.get("assets") not in ASSETS:
        problems.append(f"{entry.get('slug', '?')}: assets must be one of {' · '.join(ASSETS)}")
    toks = entry.get("tokens") or []
    if not toks:
        problems.append(f"{entry.get('slug', '?')}: an entry prints no numbers, so write it as prose")
    for t in toks:
        kind = t.get("t")
        if kind not in TOKEN_KINDS:
            problems.append(f"{entry.get('slug', '?')}: token kind {kind!r} is not one of "
                            f"{' · '.join(TOKEN_KINDS)}")
            continue
        for lang in ("en", "zh"):
            if not t.get(lang):
                problems.append(f"{entry.get('slug', '?')}: token {kind} has no {lang} wording")
        field = t.get("field")
        if kind == "literal":
            if field is not None or any("{" in (t.get(l) or "") for l in ("en", "zh")):
                problems.append(f"{entry.get('slug', '?')}: a literal token holds fixed text with no "
                                "placeholder — a licence word or a created date")
        elif field != kind or not all(f"{{{kind}}}" in (t.get(l) or "") for l in ("en", "zh")):
            problems.append(f"{entry.get('slug', '?')}: token {kind} needs field \"{kind}\" and the "
                            f"placeholder {{{kind}}} in both languages")
    if "/" not in entry.get("slug", "") or " " in entry.get("slug", ""):
        problems.append(f"{entry.get('slug', '?')}: not an owner/repo slug")


def resolve(entry, sections):
    """The heading index an entry files under: the platform level if it names one, else the section."""
    want = entry["section"]
    level2 = [i for i, s in enumerate(sections) if s["level"] == 2 and s["en"] == want]
    if not level2:
        return None, f"no ## {want} heading in the corpus"
    top = level2[0]
    if not entry.get("platform"):
        return (top, "") if sections[top]["level"] == 2 else (None, f"{want} needs a platform")
    kids = [i for i in range(top + 1, len(sections))
            if sections[i]["level"] == 3 and sections[i]["en"] == entry["platform"]]
    if not kids:
        return None, f"no ### {entry['platform']} under ## {want}"
    return kids[0], ""


def measure(entry, snap_date, snap, cand_date, cand):
    """Copy measured numbers from the newest file that carries the slug; invent nothing."""
    for date, rows, src in ((snap_date, snap, "snapshot"), (cand_date, cand, "candidates")):
        row = rows.get(entry["slug"].lower())
        if row:
            return {"stars": int(row["stars"]), "forks": int(row["forks"]), "pushed": row["pushed"],
                    "archived": row["archived"] == "True", "license_spdx": row["license"],
                    "snapshot": date}, src
    return None, ""


def position(corpus_entries, index, stars):
    """Insert before the first row of the same heading whose star count is lower — nothing moves."""
    for i, e in enumerate(corpus_entries):
        if e["_section_index"] == index:
            start = i
            break
    else:
        return len(corpus_entries)
    end = next((i for i, e in enumerate(corpus_entries[start:], start)
                if e["_section_index"] != index), len(corpus_entries))
    for i in range(start, end):
        m = corpus_entries[i].get("measured") or {}
        if (m.get("stars") or 0) < stars:
            return i
    return end


def newest_read_log(explicit=""):
    if explicit:
        p = Path(explicit)
        if not p.exists():
            sys.exit(f"no such read log: {p}")
        return p
    files = sorted(MEAS.glob("read-*.tsv"))
    if not files:
        sys.exit("no read-<date>.tsv in data/measurement/ — a stage-2 pass records what it reads with "
                 "`python3 scripts/quality.py read --repo owner/repo`")
    return files[-1]


def pending_rows(path):
    if not path:
        return []
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    return rows.get("entries", []) if isinstance(rows, dict) else rows


def coverage(corpus, pending, decisions, explicit=""):
    """Every slug that was read owes a disposition: the corpus, this pending file, or a ledger line."""
    log = newest_read_log(explicit)
    slugs = list(dict.fromkeys(r["slug"] for r in read_tsv(log)))
    entered = {e["slug"].lower() for e in corpus["entries"]}
    pend = {e["slug"].lower() for e in pending}
    ledger = set()
    if Path(decisions).exists():
        for line in Path(decisions).read_text(encoding="utf-8").splitlines():
            if line.strip():
                ledger.add(json.loads(line)["slug"].lower())
    where = lambda s: ("corpus" if s.lower() in entered else
                       "pending" if s.lower() in pend else "ledger")
    loose = {s.lower() for s in slugs if s.lower() not in (entered | pend | ledger)}
    print(f"coverage: {len(slugs)} slug(s) read, from {log.name}")
    for s in slugs:
        if s.lower() not in loose:
            print(f"  settled    {s}  ({where(s)})")
    if not loose:
        print(f"  every read row is dispositioned — {len(slugs)}/{len(slugs)}")
        return 0
    print(f"  UNSETTLED  {len(loose)} of {len(slugs)} — a read with no decision is a read no later "
          f"reader can audit:")
    for s in slugs:
        if s.lower() in loose:
            print(f"    {s}")
    print("  each one owes an object in pending-<date>.json, or one line: python3 scripts/decide.py "
          "defer --slug owner/repo --blocked-on A1|A2|A3|filing --quote \"the sentence read\" "
          "--read-at README.md --note \"what it waits on\"")
    return 1


def main():
    ap = argparse.ArgumentParser(prog="merge.py", description=__doc__.splitlines()[0])
    ap.add_argument("pending", nargs="?", help="pending-<date>.json")
    ap.add_argument("--corpus", default=str(DATA / "entries.json"))
    ap.add_argument("--out", help="corpus path to write (default: in place)")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--decisions", default=str(DATA / "decisions.jsonl"),
                    help="decision ledger to append the admit lines to")
    ap.add_argument("--coverage", nargs="?", const="", default=None, metavar="READ_TSV",
                    help="check that every slug `quality.py read` recorded has a disposition "
                         "(default: the newest data/measurement/read-<date>.tsv)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not a.pending and a.coverage is None:
        ap.error("pending-<date>.json is required unless --coverage runs the stage-2 gate on its own")

    corpus = json.loads(Path(a.corpus).read_text(encoding="utf-8"))
    pending = pending_rows(a.pending)
    if a.coverage is not None:
        sys.exit(coverage(corpus, pending, a.decisions, a.coverage))
    snap_date, snap = newest_snapshot()
    cand_date, cand = newest_candidates()
    have = {e["slug"].lower() for e in corpus["entries"]}

    problems, merged, sources = [], [], {}
    for e in pending:
        check(e, problems)
        if not e.get("section") or not e.get("slug"):
            continue                     # nothing below this can be judged without them
        if e["slug"].lower() in have:
            problems.append(f"{e['slug']}: already entered — a change to it is a wording-fix decision")
            continue
        index, why = resolve(e, corpus["sections"])
        if index is None:
            problems.append(f"{e['slug']}: {why}")
            continue
        measured, src = measure(e, snap_date, snap, cand_date, cand)
        if measured is None:
            problems.append(f"{e['slug']}: no row in snapshot-{snap_date}.tsv or the newest "
                            "candidates-<date>.tsv — run verify.py refresh or preflight.py first")
            continue
        e = {k: v for k, v in e.items() if k not in ("_section_index", "measured", "check")}
        e["_section_index"] = index
        e["measured"] = measured
        e["note"] = e.get("note") or None
        e["check"] = e["section"] != "Related lists"
        merged.append(e)
        sources[e["slug"]] = src
        have.add(e["slug"].lower())

    if problems:
        print(f"not merged ({len(problems)} problem(s)):")
        for p in problems:
            print(f"  {p}")
        if not a.dry_run:
            sys.exit("nothing written — a pending file merges whole or not at all")
    if not merged:
        sys.exit("nothing to merge")
    if a.dry_run:
        print(f"dry run: {len(merged)} row(s) would enter")
        for e in merged:
            print(f"  would add {e['slug']}  ★ {e['measured']['stars']:,} "
                  f"({sources[e['slug']]}-{e['measured']['snapshot']}.tsv) at corpus index "
                  f"{position(corpus['entries'], e['_section_index'], e['measured']['stars'])}, "
                  f"in ## {e['section']}" + (f" / {e['platform']}" if e.get("platform") else ""))
        sys.exit(1 if problems else 0)

    for e in sorted(merged, key=lambda x: x["_section_index"]):
        corpus["entries"].insert(position(corpus["entries"], e["_section_index"],
                                           e["measured"]["stars"]), e)
    out = Path(a.out) if a.out else Path(a.corpus)
    tmp = out.with_suffix(out.suffix + ".tmp")
    tmp.write_text(json.dumps(corpus, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(out)

    log = Path(a.decisions)
    with log.open("a", encoding="utf-8") as fh:
        for e in merged:
            adm = e["admission"]
            fh.write(json.dumps({"date": a.date, "slug": e["slug"], "decision": "admit",
                                 "blocked_on": "none", "quote": adm["a2_quote"],
                                 "read_at": adm["a2_read_at"],
                                 "note": f"{e['section']}"
                                         + (f" / {e['platform']}" if e.get("platform") else ""),
                                 }, ensure_ascii=False) + "\n")

    print(f"merged {len(merged)} entr(ies) into {out.name}; corpus is now "
          f"{len(corpus['entries'])} entries, {len(merged)} admit line(s) in {log.name}")
    for e in merged:
        print(f"  + {e['slug']}  ★ {e['measured']['stars']:,} "
              f"({sources[e['slug']]}-{e['measured']['snapshot']}.tsv)  {e['section']}"
              + (f" / {e['platform']}" if e.get("platform") else ""))
    print("next: python3 scripts/render.py && python3 scripts/render.py --check && "
          "python3 scripts/check-i18n.py && python3 scripts/merge.py --coverage   "
          "(the merge commit removes the pending file)")


if __name__ == "__main__":
    main()
