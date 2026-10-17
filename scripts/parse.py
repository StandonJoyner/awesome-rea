#!/usr/bin/env python3
"""Read the two READMEs and the newest snapshot back into entries.json.

  python3 scripts/parse.py                 # writes entries.json from README.md + README.zh-CN.md
  python3 scripts/parse.py --stdout        # print the json instead

The READMEs are the current source of truth for prose and wording; the snapshot supplies the
numbers so entries.json never stores a figure the API has not been read to give. Fields the README
cannot show (method, admission evidence, assets boundary) come back null and are filled in by the
stage that reads a repository.
"""
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MEAS = ROOT / "data" / "measurement"
EN, ZH = ROOT / "README.md", ROOT / "README.zh-CN.md"
OUT = ROOT / "data" / "entries.json"

BULLET = re.compile(r"^- \[([^\]]+)\]\(([^)]+)\)(?: - (.*))?$")
TOC = re.compile(r"^(  )?- \[([^\]]+)\]\(#([^)]+)\)$")
HEADING = re.compile(r"^(#{2,3}) (.+)$")
TOKEN_EN = re.compile(r"^★ ([\d,]+)$")
TOKEN_NUM = re.compile(r"^([\d,]+) forks?$")
PUSHED = re.compile(r"^(?:pushed|last push|created and pushed|archived, last push) (\d{4}-\d\d-\d\d)$")
PUSHED_ZH = re.compile(r"^(?:推送于|最近推送|建库与推送于|已归档，最近推送) (\d{4}-\d\d-\d\d)$")
CREATED = re.compile(r"^created (\d{4}-\d\d-\d\d)$")
CREATED_ZH = re.compile(r"^建库于 (\d{4}-\d\d-\d\d)$")
TOKEN_RES = (TOKEN_EN, TOKEN_NUM, PUSHED, PUSHED_ZH, CREATED, CREATED_ZH)


def slugify(text):
    """GitHub's anchor: keep word characters, spaces and hyphens, lowercase, spaces to hyphens."""
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)          # [label](url) -> label
    t = re.sub(r"`([^`]*)`", r"\1", t)                           # `code` -> code
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", t)                   # images vanish
    t = re.sub(r"[^\w\s-]", "", t, flags=re.UNICODE)             # punctuation and 、。「」 go away
    return t.strip().lower().replace(" ", "-")


def split_tail(tail):
    """('★ 9 · created and pushed 2026-10-06. Its NOTICE …') -> (tokens, note).

    A segment's sentence-final period is the renderer's job, so it is stripped here rather than kept
    in the token's wording; what follows it is the entry's closing note.
    """
    segs = [s.strip() for s in tail.split(" · ")]
    note = ""
    m = re.match(r"^(.+?[。.])(?:\s*)(.*)$", segs[-1])
    if m and any(r.match(m.group(1).rstrip("。. ")) for r in TOKEN_RES):
        segs[-1], note = m.group(1).rstrip("。. "), m.group(2)
    elif segs[-1].endswith(("。", ".")):
        segs[-1] = segs[-1].rstrip("。. ")
    return segs, note


def token_value(seg):
    """One tail segment -> (kind, field, printed wording with a {field} placeholder)."""
    if m := TOKEN_EN.match(seg):
        return "stars", "stars", "★ {stars}"
    if m := TOKEN_NUM.match(seg):
        return "forks", "forks", seg.replace(m.group(1), "{forks}")
    if m := PUSHED.match(seg):
        return "pushed", "pushed", seg.replace(m.group(1), "{pushed}")
    if m := PUSHED_ZH.match(seg):
        return "pushed", "pushed", seg.replace(m.group(1), "{pushed}")
    if m := CREATED.match(seg):
        return "literal", None, seg
    if m := CREATED_ZH.match(seg):
        return "literal", None, seg
    return "literal", None, seg


def read(path):
    return path.read_text(encoding="utf-8").splitlines()


def latest_snapshot():
    files = sorted(MEAS.glob("snapshot-*.tsv"))
    if not files:
        sys.exit("no snapshot-<date>.tsv in data/measurement/ — run verify.py refresh first")
    with open(files[-1], newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    return files[-1].stem.split("-", 1)[1], {r["repo"].lower(): r for r in rows}


def blockify(lines):
    """Document order blocks: (kind, payload) with kind in heading/intro/entry/note/toc/para."""
    out, section = [], None
    for n, line in enumerate(lines, 1):
        if not line.strip():
            continue
        if line.startswith("# "):
            out.append(("title", line))
            continue
        if h := HEADING.match(line):
            section = {"level": len(h.group(1)), "text": h.group(2), "intro": [],
                       "entries": [], "notes": [], "toc": []}
            out.append(("heading", section))
            continue
        if section is None:
            out.append(("pre", line))
            continue
        if m := TOC.match(line):
            section["toc"].append((bool(m.group(1)), m.group(2), m.group(3)))
            continue
        if BULLET.match(line):
            section["entries"].append(line)
            continue
        # a paragraph is an intro until the section's first entry, a note after it
        (section["notes"] if section["entries"] else section["intro"]).append(line)
    return out


def parse_entry(en_line, zh_line):
    me, mz = BULLET.match(en_line), BULLET.match(zh_line)
    slug, url, rest_en = me.group(1), me.group(2), me.group(3)
    assert mz.group(1) == slug and mz.group(2) == url, f"{slug}: link text or URL differs by language"
    # the URL is derived from the slug, never stored, so a mistyped owner cannot survive a refresh
    assert url == f"https://github.com/{slug}", f"{slug}: link text and URL path disagree"
    i_en, i_zh = rest_en.find("★ "), mz.group(3).find("★ ")
    assert i_en >= 0 and i_zh >= 0, f"{slug}: no ★ in the line"
    desc_en, desc_zh = rest_en[:i_en].rstrip(), mz.group(3)[:i_zh].rstrip()
    for d in (desc_en, desc_zh):
        assert d.endswith(".") or d.endswith("。") or not d, f"{slug}: description not closed: {d[-8:]}"
    segs_en, note_en = split_tail(rest_en[i_en:])
    segs_zh, note_zh = split_tail(mz.group(3)[i_zh:])
    assert bool(note_en) == bool(note_zh), f"{slug}: a closing note in one language only"
    assert len(segs_en) == len(segs_zh), f"{slug}: {len(segs_en)} en tokens vs {len(segs_zh)} zh"
    tokens = []
    for s_en, s_zh in zip(segs_en, segs_zh):
        k_en, field_en, w_en = token_value(s_en)
        k_zh, field_zh, w_zh = token_value(s_zh)
        assert k_en == k_zh, f"{slug}: token kind differs ({s_en!r} / {s_zh!r})"
        tokens.append({"t": k_en, "field": field_en, "en": w_en, "zh": w_zh})
    return slug, url, desc_en.rstrip(".。 "), desc_zh.rstrip(".。"), tokens, note_en, note_zh


def main():
    write_stdout = "--stdout" in sys.argv
    en_lines, zh_lines = read(EN), read(ZH)
    assert len(en_lines) == len(zh_lines), "the two READMEs are no longer line-parallel"
    snap_date, snap = latest_snapshot()
    blocks_en, blocks_zh = blockify(en_lines), blockify(zh_lines)
    assert [k for k, _ in blocks_en] == [k for k, _ in blocks_zh], "block kinds differ by language"

    # numbers and the refreshed date live in the provenance paragraph
    pre = [v for k, v in blocks_en if k == "pre"]
    pre_zh = [v for k, v in blocks_zh if k == "pre"]
    prov = next(l for l in pre if "Data last refreshed" in l)
    refreshed = re.search(r"Data last refreshed (\d{4}-\d\d-\d\d)", prov).group(1)
    header = [{"en": e, "zh": z} for e, z in zip(pre, pre_zh)]
    for h in header:
        h["en"] = h["en"].replace(f"Data last refreshed {refreshed}", "Data last refreshed {refreshed}")
        h["zh"] = h["zh"].replace(f"数据刷新于 {refreshed}", "数据刷新于 {refreshed}")
        if h["en"].startswith("- [") or h["zh"].startswith("- ["):
            sys.exit("a pre-Contents bullet is not a header paragraph — the parser would drop it")

    sections, entries, seen_slugs = [], [], set()
    heads_en = [v for k, v in blocks_en if k == "heading"]
    heads_zh = [v for k, v in blocks_zh if k == "heading"]
    assert len(heads_en) == len(heads_zh), "the two READMEs have a different number of headings"
    toc_en, toc_zh, p = [], [], 0
    parent = {"en": None, "zh": None}
    for be, bz in zip(heads_en, heads_zh):
        if be["text"] == "Contents":
            assert [t[0] for t in be["toc"]] == [t[0] for t in bz["toc"]], \
                "the two Contents lists indent differently"
            toc_en, toc_zh = be["toc"], bz["toc"]
            continue
        sec = {"level": be["level"], "en": be["text"], "zh": bz["text"],
               "anchor": {"en": slugify(be["text"]), "zh": slugify(bz["text"])}}
        # Contents is positional: it lists a subset, in document order, so a pointer walks it
        if p < len(toc_en) and toc_en[p][1] == be["text"]:
            ind, _, anchor = toc_en[p]
            assert ind == (sec["level"] == 3), f"{be['text']}: Contents indent contradicts its heading level"
            assert anchor == sec["anchor"]["en"], \
                f"{be['text']}: Contents anchor {anchor!r} != derived {sec['anchor']['en']!r}"
            assert toc_zh[p][2] == sec["anchor"]["zh"], \
                f"{bz['text']}: Chinese Contents anchor {toc_zh[p][2]!r} != derived {sec['anchor']['zh']!r}"
            sec["toc_label"] = {"en": toc_en[p][1], "zh": toc_zh[p][1]}
            sec["in_contents"] = True
            p += 1
        if be["level"] == 2:
            parent = {"en": be["text"], "zh": bz["text"]}
        if be["intro"]:
            assert len(be["intro"]) == len(bz["intro"]) == 1, f"{be['text']}: multiple intro paragraphs"
            sec["intro"] = {"en": be["intro"][0], "zh": bz["intro"][0]}
        if be["notes"]:
            sec["notes"] = [{"en": e, "zh": z} for e, z in zip(be["notes"], bz["notes"])]
        assert len(be["entries"]) == len(bz["entries"]), f"{be['text']}: entry count differs by language"
        for en_line, zh_line in zip(be["entries"], bz["entries"]):
            slug, url, d_en, d_zh, toks, n_en, n_zh = parse_entry(en_line, zh_line)
            if slug.lower() in seen_slugs:
                sys.exit(f"duplicate slug {slug}")
            seen_slugs.add(slug.lower())
            s = snap.get(slug.lower())
            measured = None
            if s:
                measured = {"stars": int(s["stars"]), "forks": int(s["forks"]), "pushed": s["pushed"],
                            "archived": s["archived"] == "True", "license_spdx": s["license"],
                            "snapshot": snap_date}
            entries.append({"slug": slug, "_section_index": len(sections),
                            "section": parent["en"], "platform": sec["en"] if be["level"] == 3 else None,
                            "desc": {"en": d_en, "zh": d_zh}, "tokens": toks,
                            "note": {"en": n_en, "zh": n_zh} if n_en or n_zh else None,
                            "measured": measured, "method": None,
                            "admission": {"a1": None, "a2_quote": None, "a2_read_at": None, "a3": None},
                            "assets": None, "check": sec["en"] != "Related lists"})
        sections.append(sec)

    doc = {"schema": 1, "refreshed": refreshed, "title": blocks_en[0][1], "header": header,
           "sections": sections, "entries": entries,
           "counts": {"entries": len(entries), "sections": len(sections)}}
    text = json.dumps(doc, ensure_ascii=False, indent=2)
    if write_stdout:
        print(text)
    else:
        OUT.write_text(text + "\n", encoding="utf-8")
        measured_missing = [e["slug"] for e in entries if e["measured"] is None]
        print(f"wrote {OUT.name}: {len(entries)} entries, {len(sections)} sections, "
              f"{sum(1 for e in entries if e['note'])} notes, "
              f"{sum(1 for s in sections if s.get('notes'))} sections with notes")
        if measured_missing:
            print("no snapshot row for: " + ", ".join(measured_missing))


if __name__ == "__main__":
    main()
