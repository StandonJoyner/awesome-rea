#!/usr/bin/env python3
"""Fail if README.zh-CN.md drifts from README.md.

The Chinese README claims to be a mirror, so both files must carry the same links,
the same sections, and the same number of entries in each section.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = re.compile(r"https?://[^\s)\]\"'<>]+")
HEADING = re.compile(r"^(#{2,3}) (.+)$")

en = (ROOT / "README.md").read_text(encoding="utf-8")
zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")


def urls(text):
    return {u.rstrip(".,;:") for u in URL.findall(text)}


def sections(text):
    """{heading: entry count} in file order, level 2 and level 3 both counted.

    A heading's entries are the bullets under it until the next heading of any
    level, so a level-3 block belongs to its own row, not to its parent.
    """
    out, cur = {}, None
    for line in text.splitlines():
        m = HEADING.match(line)
        if m:
            cur = ("\u00a0" * (len(m.group(1)) - 2)) + m.group(2)
            out.setdefault(cur, 0)
        elif cur and line.startswith("- [") and "](https://" in line:
            out[cur] += 1
    return out


problems = [f"missing from README.zh-CN.md: {u}" for u in sorted(urls(en) - urls(zh))]
problems += [f"missing from README.md: {u}" for u in sorted(urls(zh) - urls(en))]

en_secs, zh_secs = list(sections(en).items()), list(sections(zh).items())
if len(en_secs) != len(zh_secs):
    problems.append(f"section count: README.md={len(en_secs)} README.zh-CN.md={len(zh_secs)}")
for i, ((h1, n1), (h2, n2)) in enumerate(zip(en_secs, zh_secs)):
    if n1 != n2:
        problems.append(f"section {i + 1} ({h1} / {h2}) entries: {n1} != {n2}")

for label, count in [("warn marks", lambda t: t.count("⚠"))]:
    if count(en) != count(zh):
        problems.append(f"{label}: README.md={count(en)} README.zh-CN.md={count(zh)}")

if problems:
    print("\n".join(problems))
    sys.exit(1)

print(f"mirrored: {len(urls(en))} links, {sum(n for _, n in en_secs)} entries in {len(en_secs)} sections")
