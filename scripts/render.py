#!/usr/bin/env python3
"""Render README.md and README.zh-CN.md from entries.json.

  python3 scripts/render.py          # write both files
  python3 scripts/render.py --check  # compare against the files on disk, exit 1 on any diff

Rendering is how these two files change once the pipeline is live: prose and wording come from the
json, numbers come from `measured`, and a number the snapshot does not carry prints nothing rather
than a zero.
"""
import difflib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CORPUS = ROOT / "data" / "entries.json"
TARGETS = {"en": ROOT / "README.md", "zh": ROOT / "README.zh-CN.md"}
SEP = " · "
END = {"en": ".", "zh": "。"}
JOIN = {"en": " ", "zh": ""}          # Chinese closes with 。 and runs on; English puts a space after it
CONTENTS = {"en": "## Contents", "zh": "## 目录"}


def fill(tokens, measured, lang):
    """The number tail: a {field} placeholder takes its value from the snapshot, or drops out with it."""
    out = []
    for t in tokens:
        word = t[lang]
        if t["field"] is None:
            out.append(word)
            continue
        value = (measured or {}).get(t["field"])
        if value is None:
            continue                      # never invent a figure the API has not reported
        text = f"{value:,}" if isinstance(value, int) else str(value)
        out.append(word.replace("{" + t["field"] + "}", text))
    return out


def entry_bullet(e, lang):
    tail = SEP.join(fill(e["tokens"], e["measured"], lang))
    url = f"https://github.com/{e['slug']}"   # derived from the slug, never stored
    line = f"- [{e['slug']}]({url}) - {e['desc'][lang]}{END[lang]}{JOIN[lang]}{tail}{END[lang]}"
    if e["note"] and e["note"][lang]:
        line += JOIN[lang] + e["note"][lang]
    return line


def contents_order(sections):
    """Every section listed in Contents, level 2 followed by the level 3 lines under it."""
    ordered = []
    for i, s in enumerate(sections):
        if not s.get("in_contents") or s["level"] != 2:
            continue
        ordered.append(s)
        for k in sections[i + 1:]:
            if k["level"] == 2:
                break
            if k.get("in_contents"):
                ordered.append(k)
    return ordered


def build(doc, lang):
    lines = [doc["title"], ""]
    for h in doc["header"]:
        lines.append(h[lang].replace("{refreshed}", doc["refreshed"]))
        lines.append("")
    lines.append(CONTENTS[lang])
    lines.append("")
    for s in contents_order(doc["sections"]):
        lines.append(f"{'  ' if s['level'] == 3 else ''}- [{s['toc_label'][lang]}](#{s['anchor'][lang]})")
    lines.append("")
    for s in doc["sections"]:
        lines.append("#" * s["level"] + " " + s[lang])
        lines.append("")
        if s.get("intro"):
            lines.append(s["intro"][lang])
            lines.append("")
        for e in doc["entries_by_section"].get(s["i"], []):
            lines.append(entry_bullet(e, lang))
        for note in s.get("notes", []):
            lines.append("")
            lines.append(note[lang])
        lines.append("")
    while lines and not lines[-1]:
        lines.pop()
    # a section that carries only an intro and a child heading would otherwise open two blank lines
    out = [l for i, l in enumerate(lines) if not (l == "" and i and lines[i - 1] == "")]
    return "\n".join(out) + "\n"


def main():
    doc = json.loads(CORPUS.read_text(encoding="utf-8"))
    for i, s in enumerate(doc["sections"]):
        s["i"] = i
    doc["entries_by_section"] = {}
    for e in doc["entries"]:
        doc["entries_by_section"].setdefault(e["_section_index"], []).append(e)
    text = {lang: build(doc, lang) for lang in ("en", "zh")}

    if "--check" not in sys.argv:
        for lang, path in TARGETS.items():
            path.write_text(text[lang], encoding="utf-8")
            print(f"wrote {path.name}")
        return

    bad = 0
    for lang, path in TARGETS.items():
        want = path.read_text(encoding="utf-8")
        if want == text[lang]:
            print(f"{path.name}: identical")
            continue
        bad += 1
        diff = list(difflib.unified_diff(want.splitlines(), text[lang].splitlines(),
                                         f"{path.name} on disk", f"{path.name} rendered", lineterm="", n=1))
        changed = sum(1 for d in diff if d[:1] in "+-" and d[:3] not in ("+++", "---"))
        print(f"{path.name}: {changed} lines differ")
        print("\n".join(diff[:60]))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
