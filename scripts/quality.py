#!/usr/bin/env python3
"""Judge what a repository publishes as proof, without judging whether it is good.

  check                     — run every repository linked from README.md
  check --repos FILE        — run one owner/repo per line instead
  check --repo owner/repo   — run a single hand-named repository
  check --aggregate FILE    — run rows of a data/games.json-style dump (no manual reading)
  check ... --band MIN MAX  — star window for --aggregate
  check ... --sample N      — deterministic random subset of the matching rows

  read --repo owner/repo    — stage 2's evidence pack: one screen per candidate, from the cache
  read --repos FILE         — the same for a batch of rows about to be read
  read ... --has FILE       — intersect the cached tree with a list of filenames you supply
  read ... --docs N         — side-docs to pull per candidate (default 3, 0 = README only)
  read ... --out FILE       — also write the pack to FILE (it still prints)
  read ... --refresh        — re-read from the API instead of the cache, and say so

`read` is what a stage-2 pass starts and ends with, and it is meant to be **the only thing it does**: one
call per batch prints the measured row, the precheck, a tree summary, where the source sits per top-level
directory, the external links that betray a pointer repository, every method-shaped sentence in its entirety
(wrap joined, markup stripped) with the `a2_read_at` locator to paste beside it, and the `facts` block of
format/boundary/unfinished-state sentences that `desc`, `note` and `assets` are written from. Sentences come
from the README **and from the side-docs the README does not carry** — `FAQ.md`, `ROADMAP.md`, a gaps or
parity file, `NOTICE.md`/`ATTRIBUTION.md` — fetched once and cached, because a fact that lives in `FAQ.md`
otherwise costs the reader four requests of their own. Each locator names the file it came from.
It then records the slug in `data/measurement/read-<date>.tsv`, which is what `merge.py --coverage` holds the
pass to: after a `read`, a slug owes either a pending object or a `decisions.jsonl` line. Reading
`data/cache/quality/*.json` by hand, writing a throwaway script to pull a README line out of it, or `curl`ing
`FAQ.md` because a fact looked like it lived there, is the work this screen exists to
remove (`INTAKE.md`, `## The three stages and the three files`). It prints **no verdict and no prose**: the
sentences are a locator, not a filter (`INTAKE.md`: a word screen over the first 120 lines false-flagged 33
of the 136 entered slugs), so which sentence the entry quotes, and whether the tree holds the
reconstruction, stay the reader's. Nothing in the pack may be paraphrased into an entry without re-reading
the line it came from.

Per repository `check` costs three requests: `GET /repos/{owner}/{repo}`, the README, and the
recursive git tree. Responses are cached under data/cache/quality so a re-run is free; --refresh re-reads.
The fourth request (releases) fires only when no build file was found.

`read` adds up to `--docs` raw requests per candidate for its side-docs and **nothing else** — the
source-per-directory screen and the submodule line are computed from the tree `check` already cached, at
zero cost. `check` never fetches side-docs, so a sweep over every entered repository stays at three
requests per repository (`INTAKE.md`: standards must not require measuring everything, every day).

Four evidence classes, each either present in the repository or not:

  E1 match      byte-for-byte / matching ROM / a hash / a decompilation percentage
  E2 compat     a compatibility or progress table with a denominator
  E3 repro      a build system or CI, so the reader can reproduce it
  E4 boundary   an explicit "ships no game files, bring your own copy"

verdict: exclude (no source code, no README) / eligible (E1 or E2) /
conditional (E3 or E4 only) / watch (nothing checkable published).
`archived` is a flag, not a verdict: an author who marks a finished reconstruction read-only
has stated completion, not disqualification. A takedown does not set it — it returns 404.
The `e` column writes `E1x` when that class is present and `E1-` when it is absent.

`precheck` is the other half, and it runs **negatively**: it says which candidates the API already
settles (`already-entered` · `fork-of-entered`) and which still need a read (`pass`). It does not
name the vendor-source, instrument or fan-content classes — measured, a word screen catches an
eighth of the refusals we have on record and false-flags entered entries, so `INTAKE.md`'s `## Admission` keeps
A1 and A3 as reads of the credits section, the provenance sentences and the root listing.
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
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
README = ROOT / "README.md"
CACHE = ROOT / "data" / "cache" / "quality"
MEAS = ROOT / "data" / "measurement"
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

META_KEYS = ("stargazers_count", "forks_count", "subscribers_count", "language", "size",
             "archived", "pushed_at", "created_at", "description", "license", "fork")

# What stage 1 can decide without reading anything: the two classes the API states outright.
# The other three documented rejection classes are not machine-decidable, and that is a measurement,
# not an assumption. Run 2026-10-17 against the refusals listed in `## The aggregator we are sized
# against`, a word screen over each repository's own description and README opening caught 4 of the 32
# rows it was meant for (vendor-source 1/16, tool-or-list 0/3, mod-or-hack 3/13) while false-flagging 33
# of the 136 entered slugs over 120 README lines — `launcher`, `decompiler` and `debugger` appear in
# dependency lists and setup sections of real reconstructions, and `kichikuou/xsys35c` is titled
# "System 3.x Compiler and Decompiler" and belongs here. The one class the API does settle is the fork
# one: `parent`/`source` names the entered repository in 3 of the 4 recorded fork refusals, missing
# `d07RiV/diabloweb`, a WebAssembly build *of* a devilution fork rather than a fork of one. So A1 and A3
# stay a read of the credits section, the provenance sentences and the root listing; `precheck` only says
# which candidates are settled without one.
PRECHECK_ORDER = ("already-entered", "fork-of-entered", "pass")


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
    entries = tree.get("tree") or []
    names = [t.get("path", "") for t in entries]
    # A gitlink is a directory that arrives by submodule: the code that lives there is not this
    # repository's result, which is half of what A3 asks. The same response already says it, so it costs
    # nothing to keep — a tree cached before this field simply prints no submodule line.
    submodules = sorted({t["path"] for t in entries if t.get("type") == "commit"})
    if not names:
        status = "unknown"
    else:
        status = "full" if not tree.get("truncated") else "truncated"
    if status == "unknown":  # big repo or a slow answer: root listing plus the language bytes
        top = gh(repo, f"/git/trees/{branch}", timeout=45)
        entries = top.get("tree") or []
        names = [t.get("path", "") for t in entries]
        submodules = sorted({t["path"] for t in entries if t.get("type") == "commit"})
        status = "partial" if names else "none"
    langs = gh(repo, "/languages", timeout=45) if status != "full" else {}
    rec = {"repo": repo, "meta": {k: meta.get(k) for k in META_KEYS},
           "parent": parent_of(meta),
           "readme_len": len(readme), "names": names, "tree_status": status,
           "tree_truncated": bool(tree.get("truncated")), "langs": langs,
           "submodules": submodules,
           "readme_head": [line for line in readme.splitlines() if line.strip()][:400],
           "readme_blocks": readme_blocks(readme),
           "fetched": datetime.date.today().isoformat()}
    if not rec["tree_truncated"] and len(names) < 5000:
        rec["readme_snips"] = ""  # quotes come from readme_head, kept small on purpose
    CACHE.mkdir(parents=True, exist_ok=True)
    p = cache_path(repo)
    p.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
    if not names:  # the tree call may have failed while the rest worked
        rec["names"] = []
    return rec


CORPUS_SLUGS = None


def corpus_slugs():
    """Every slug already linked from README.md, resolved once per run."""
    global CORPUS_SLUGS
    if CORPUS_SLUGS is None:
        CORPUS_SLUGS = {s.lower() for s in from_readme()}
    return CORPUS_SLUGS


def parent_of(meta):
    """The upstream `owner/repo` of a fork, or '' — GitHub names both a parent and a source."""
    return (meta.get("parent") or {}).get("full_name") or \
           (meta.get("source") or {}).get("full_name") or ""


def precheck(repo, parent=None, corpus=None):
    """`already-entered`, `fork-of-entered` or `pass` — the three states needing no prose read.

    `pass` is not a recommendation: it means the API has nothing to say about the class, so A1–A3
    are still ahead of it. A hit is settled: the reader reaches the result through the one entry.
    """
    corpus = corpus_slugs() if corpus is None else corpus
    if repo.lower() in corpus:
        return "already-entered", repo
    if parent is None:  # not at hand: one request, and stage 1 always has it already
        parent = parent_of(gh(repo))
    if parent and parent.lower() in corpus:
        return "fork-of-entered", parent
    return "pass", ""


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
    if "shell" in flags or "noreadme" in flags:
        verdict = "exclude"
    elif e1 or e2:
        verdict = "eligible"
    elif e3 or e4:
        verdict = "conditional"
    else:
        verdict = "watch"
    return {"repo": repo, "stars": m.get("stargazers_count") or 0,
            "forks": m.get("forks_count") or 0, "watchers": m.get("subscribers_count") or 0,
            "pushed": (m.get("pushed_at") or "")[:10], "created": (m.get("created_at") or "")[:10],
            "lang": m.get("language") or "", "size_kb": m.get("size") or 0,
            "license": (m.get("license") or {}).get("spdx_id") or "",
            "archived": bool(m.get("archived")),
            "src": src, "files": len(names),
            "e": f"E1{'x' if e1 else '-'}E2{'x' if e2 else '-'}E3{'x' if e3 else '-'}E4{'x' if e4 else '-'}",
            "evidence": ev, "quote": (e1 or e2 or e4 or e3 or prog)[:200],
            "flags": flags, "verdict": verdict}


# --------------------------------------------------------------------------- stage 2's evidence pack

SHAPE = (
    ("M1", re.compile(r"decompil\w*|disassembl\w*|byte[\s-]?match\w*|matching (?:rom|exe|binary|image)|"
                      r"反编译|反組譯|反组译|逐字节|逐位元組", re.I)),
    ("M2", re.compile(r"clean[\s-]?room|re-?implement\w*|remake|remaster|\bclone\b|re-?creation|"
                      r"written from scratch|rewrit\w*|从零|從零|重寫|重写|還原|还原|重製|重制", re.I)),
    ("M3", re.compile(r"\bformat(?:s|ed|ting)?\b|\bprotocol\w*|\bdriver\w*|\bAPI\b|encod\w*|decod\w*|"
                      r"\bpars\w*|compiler|decompiler|格式|協議|协议|編譯器|解码|還原器", re.I)),
    ("M4", re.compile(r"\bport(?:ed|ing|s)?\b|static[\s-]?(?:recomp|recompil)\w*|recompil\w*|移植|搬運", re.I)),
    ("RE", re.compile(r"reverse[\s-]?engin\w*|逆向", re.I)),
)
COPULA = re.compile(r"\b(?:is|are|was|were)\b|[是为]|は|です")
DATA_DIR = re.compile(r"asset|resource|content|data|texture|audio|model|font|art|original|baserom|rom",
                      re.I)
ASSET_EXT = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tga", ".wav", ".ogg", ".mp3", ".mp4", ".arc",
             ".dat", ".bin", ".pak", ".mpq", ".grp", ".idx", ".nam", ".rom", ".z64", ".n64", ".gba",
             ".nds", ".iso", ".ttf", ".otf", ".xa", ".str", ".usm", ".umap", ".uasset"}
EXTERNAL = re.compile(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)")


def shapes(line):
    return "+".join(label for label, rx in SHAPE if rx.search(line))


def plain(s):
    """README markup off, whitespace folded — the text an entry quotes, not the HTML it sits in."""
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"__(.+?)__", r"\1", s)
    return re.sub(r"`([^`]*)`", r"\1", re.sub(r"\s+", " ", s)).strip()


def readme_blocks(text, cap=400):
    """A document as quotable blocks — (first line, joined text) — with code fences dropped.

    Built for the README and reused for every side-doc the pack fetches, so a sentence from `FAQ.md` is
    located the same way as one from `README.md`.

    `readme_head` cannot answer "which sentence is this line part of", because the blank lines that ended
    the paragraphs are gone by the time it is built. The boundary is recorded here, at fetch time, so a
    stage-2 quote is a whole sentence rather than a wrapped fragment.
    """
    out, cur, start, fence = [], [], 0, False
    for n, raw in enumerate(text.splitlines(), 1):
        s = raw.strip()
        if s.startswith("```"):
            fence = not fence
            s = ""
        if fence or not s:
            if cur:
                out.append((start, plain(" ".join(cur))))
                cur, start = [], 0
            continue
        start = start or n
        cur.append(s)
    if cur:
        out.append((start, plain(" ".join(cur))))
    return [(i, t) for i, t in out if len(t) >= 25][:cap]


SENT = re.compile(r"(?<=[.!?])\s+")


def quote_of(text, rxs=None):
    """The one sentence in a block that carries the claim — a whole feature paragraph is not a quote.

    Chosen by how many of the given patterns it names, then by brevity, so what lands in
    `admission.a2_quote` is a sentence a later reader can find again in one look. A colon is not a sentence
    end: splitting on it produced fragments like "XLSX is the native format:".
    """
    parts = [s.strip() for s in SENT.split(text) if s.strip()]
    rxs = [rx for _, rx in SHAPE] if rxs is None else rxs
    hits = [(sum(1 for rx in rxs if rx.search(s)), len(s), s) for s in parts
            if len(s) >= 40 and any(rx.search(s) for rx in rxs)]
    return max(hits, key=lambda h: (h[0], -h[1]))[2] if hits else ""


def method_lines(sources, rec, cap=12):
    """Every method-shaped sentence the README **and its side-docs** publish, whole, with its locator.

    A locator, not a filter: `INTAKE.md` measured that the same vocabulary false-flagged 33 of the 136
    entered slugs, so the pack ranks sentences and never decides between them. Ranked by how many of the
    four method shapes a sentence names, then by whether it reads as a sentence (a copula), then by
    document order — README before side-docs, and each file by its own line number.
    """
    labels = [label for label, _ in sources] + [""]
    hits = []
    for order, (_, blocks) in enumerate(sources):
        for i, text in blocks:
            if "releases" in text.lower()[:40] or text.startswith("|"):
                continue
            sh = shapes(text)
            if sh:
                q = quote_of(text) or (text if len(text) >= 40 else "")
                if q:
                    hits.append((-len(shapes(q).split("+")), 0 if COPULA.search(q) else 1, order, i,
                                 shapes(q), q))
    desc = (rec["meta"].get("description") or "").strip()
    if desc and shapes(desc):
        hits.append((-len(shapes(desc).split("+")), 0, len(labels) - 1, 0, shapes(desc), desc))
    hits.sort()
    return [(labels[o], i, sh, s) for _, _, o, i, sh, s in hits[:cap]]


RE_CAP = re.compile(r"\.[a-z0-9]{2,5}\b|import|export|convert|your own|bring your|ships no|"
                    r"pre-?alpha|\bbeta\b|early development|not yet|still missing|incomplete|\bwip\b|"
                    r"trademark|not affiliated", re.I)
NOT_A_FORMAT = (r"(?:md|log|txt|dll|so|dylib|png|jpg|jpeg|svg|gif|html|json|yml|yaml|sh|py|rs|js|ts|css"
                r"|xml|com|org|net|io|dev|gg|app|xyz|pdf|zip|tar|gz|exe|ini|toml|lock)\b")
RE_EXT = re.compile(rf"\.(?!{NOT_A_FORMAT})[a-z0-9]{{2,5}}\b", re.I)
RE_BOUND_PHRASE = re.compile(r"your own|bring your|ships no|not included|requires? the original", re.I)
RE_STATUS = re.compile(r"pre-?alpha|\bbeta\b|early development|not yet|still missing|incomplete|\bwip\b|"
                       r"active research|decompilation progress", re.I)


def capability_lines(sources, cap=12):
    """The sentences about formats, the asset boundary and unfinished state, README and side-docs alike.

    These are what `desc`, `note` and `assets` get written from, so the pack prints them whole: without
    this half of the screen a stage-2 pass had to open `data/cache/quality/*.json` itself, the hand work
    `INTAKE.md` now forbids. Only a named data format, a boundary sentence or an admitted gap qualifies —
    a dotted domain in a nav line is not a fact about the reconstruction.
    """
    labels = [label for label, _ in sources]
    hits = []
    for order, (_, blocks) in enumerate(sources):
        for i, text in blocks:
            if text.startswith("|"):
                continue
            q = quote_of(text, [RE_CAP])
            if not q or q[-1] not in ".!?":
                continue          # nav and link lines are not sentences about the reconstruction
            score = (3 if RE_EXT.search(q) else 0) + (2 if RE_BOUND_PHRASE.search(q) else 0) + \
                (1 if RE_STATUS.search(q) else 0)
            hits.append((-score, order, i, q))
    hits.sort()
    return [(labels[o], i, s) for _, o, i, s in hits[:cap]]


def tree_pack(rec):
    from collections import Counter
    names = rec.get("names") or []
    depth1 = [n for n in names if "/" not in n.rstrip("/")][:30]
    ext = Counter(os.path.splitext(n)[1].lower() for n in names
                  if os.path.splitext(n)[1].lower() in SOURCE_EXT)
    first = Counter(n.split("/")[0] for n in names if len(n.split("/")) > 1)
    data_dirs = [(d, c) for d, c in first.most_common() if DATA_DIR.search(d)][:4]
    docs = next((f"{d} {c}" for d, c in first.most_common(20) if d.lower() in ("docs", "doc")), "none")
    assets = Counter(n.split("/")[0] for n in names
                     if os.path.splitext(n)[1].lower() in ASSET_EXT and "/" in n)
    return depth1, ext.most_common(6), data_dirs, docs, sum(assets.values()), assets.most_common(3)


def source_dirs(rec, top=6):
    """Where the source files actually sit, per top-level directory — the first half of an A3 read.

    `--has` can only test filenames the reader already guessed; A3 asks the other question, *how much*
    code is in this tree and *where*. This answers it from the cached recursive tree, so it costs no
    request: `.` is the repository root, and a directory holding a large share of the source is where the
    reconstruction lives. It ranks, it does not decide — a mod loader can hold plenty of its own code.
    """
    from collections import Counter
    src = [n for n in (rec.get("names") or []) if os.path.splitext(n)[1].lower() in SOURCE_EXT]
    if not src:
        return [], 0, 0
    per = {}
    for n in src:
        per.setdefault(n.split("/")[0] if "/" in n else ".", []).append(
            os.path.splitext(n)[1].lower())
    rows = []
    for d, exts in per.items():
        detail = " ".join(f"{e} {c}" for e, c in Counter(exts).most_common(3))
        rows.append((len(exts), d, detail))
    rows.sort(key=lambda r: (-r[0], r[1]))
    total = len(src)
    return [((d, n, f"{n * 100 // total}%", detail) for n, d, detail in rows[:top]),
            len(per), total]


# --------------------------------------------------------------------------- the side-docs a README omits

DOC_NAMES = (                                   # (basename pattern, rank) — lower rank is fetched first
    (re.compile(r"^faq\.md$", re.I), 0),
    (re.compile(r"^roadmap\.md$", re.I), 1),
    (re.compile(r"^(?:status|progress|gaps?|limitations|missing|caveats|unsupported)\.md$", re.I), 2),
    (re.compile(r"^(?:target-app-)?parity.*\.md$", re.I), 3),
    (re.compile(r"^(?:notice|attribution|credits|authors|third[-_]?part(?:ies|y)[-_]notices?)\.md$", re.I), 4),
)
DOC_CAP = 20_000        # characters kept per side-doc; a 400 KB changelog is not evidence, it is bulk


def doc_shortlist(rec, cap):
    """The side-docs worth a request, chosen from the cached tree — root first, then by rank.

    Nothing is guessed at a URL: every path here is a path the tree already returned, so a repository
    without a `FAQ.md` costs zero requests and a wrong name cannot be fetched.
    """
    cands = []
    for n in rec.get("names") or []:
        if not n.lower().endswith((".md", ".rst", ".txt")):
            continue
        base = os.path.basename(n)
        for rx, rank in DOC_NAMES:
            if rx.match(base):
                cands.append((rank, n.count("/"), len(n), n))
                break
    cands.sort()
    out, seen = [], set()
    for _, _, _, n in cands:
        # one basename once: a repository that keeps ROADMAP.md at the root and a copy under docs/ should
        # spend its third slot on a parity or gaps file, which says something the other two do not.
        b = os.path.basename(n).lower()
        if b in seen:
            continue
        seen.add(b)
        out.append(n)
        if len(out) == cap:
            break
    return out


def fetch_docs(repo, rec, cap=3, refresh=False):
    """Pull the shortlisted side-docs once, keep their quotable blocks, and cache them in the record.

    This is the difference between one pack call and the four raw requests a reader otherwise spends to
    find the sentence in `FAQ.md` that settles `assets`. Blocks are stored rather than bodies: the cache
    stays small and the locator (`FAQ.md head#14`) is a line number in the same file.
    """
    want = doc_shortlist(rec, cap)
    have = rec.get("docs") or []
    if want and not refresh and [d["path"] for d in have] == want:
        return have, 0
    out = []
    for path in want:
        body = gh(repo, "/contents/" + urllib.parse.quote(path), raw=True, timeout=45)[:DOC_CAP]
        out.append({"path": path, "chars": len(body),
                    "truncated": len(body) == DOC_CAP,
                    "blocks": readme_blocks(body, cap=160)})
    rec["docs"] = out
    p = cache_path(repo)                    # write back beside the tree, so a re-run costs nothing
    if p.exists():
        cached = json.loads(p.read_text(encoding="utf-8"))
        cached["docs"] = out
        p.write_text(json.dumps(cached, ensure_ascii=False), encoding="utf-8")
    return out, len(out)


def blocks_of(rec, docs=()):
    """Everything the pack quotes from, in order: the README, then each side-doc it fetched.

    The README keeps the label `README.md`, so a locator written before side-docs existed still reads the
    same way (`README.md head#12, 2026-10-17`) and an entry's `a2_read_at` never has to be re-derived.
    """
    out = [("README.md", rec.get("readme_blocks") or [])]
    out += [(d["path"], d.get("blocks") or []) for d in docs]
    return out


def external_links(rec):
    out = []
    for m in EXTERNAL.finditer("\n".join(rec.get("readme_head") or [])):
        s = re.sub(r"\.git$", "", m.group(1))
        if s.lower() != rec["repo"].lower() and s.lower() not in [o.lower() for o in out]:
            out.append(s)
    return out


def intersect_has(rec, path):
    """Cached tree basenames against a filename list the reader supplies — the leaked-source check.

    The script does the set intersection; naming the files that would mean vendor source is external
    knowledge and stays the reader's call (`INTAKE.md`, `## Admission`: A1 is a read, not a regex).
    """
    want = [l.strip().lower() for l in Path(path).read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")]
    have = {os.path.basename(n).lower(): n for n in rec.get("names") or []}
    return want, [have[w] for w in want if w in have]


class _Tee:
    """Write the pack to a file and keep printing it, so one `read` run is both a screen and an artefact."""

    def __init__(self, stdout, fh):
        self.stdout, self.fh = stdout, fh

    def write(self, s):
        self.stdout.write(s)
        self.fh.write(s)

    def flush(self):
        self.stdout.flush()
        self.fh.flush()

    def close(self):
        self.fh.close()


def record_read(repo, via):
    """The one trace a stage-2 pass must leave: `merge.py --coverage` holds it to pending or ledger."""
    MEAS.mkdir(parents=True, exist_ok=True)
    p = MEAS / f"read-{datetime.date.today().isoformat()}.tsv"
    fresh = not p.exists()
    with p.open("a", encoding="utf-8") as fh:
        if fresh:
            fh.write("slug\tread\tvia\n")
        fh.write(f"{repo}\t{datetime.datetime.now().isoformat(timespec='seconds')}\t{via}\n")
    return p


def pack(repo, refresh=False, has="", docs_cap=3):
    cached = cache_path(repo).exists() and not refresh
    rec = fetch(repo, refresh)
    via = "cache" if cached else ("network" if rec else "404")
    if rec and cached and "readme_blocks" not in rec:
        # a cache written before quotes were sentence-shaped cannot answer which sentence a line is in
        rec = fetch(repo, True)
        via = "cache, re-read once for quotable blocks"
    print(f"\n== {repo}   [{via}, cached fetch: {rec.get('fetched', '-') if rec else '-'}]")
    if not rec:
        print("   meta: 404 — `AGENTS.md` `## Removal` reason `gone` if this slug is entered, "
              "otherwise a refusal line with this call as its quote")
        print(f"   read: recorded in {record_read(repo, via)}")
        return
    m = rec["meta"]
    lic = (m.get("license") or {}).get("spdx_id") or "no licence file"
    print(f"   measure  ★ {m.get('stargazers_count', 0):,} · {m.get('forks_count', 0):,} forks · "
          f"{m.get('subscribers_count', 0)} watchers · pushed {(m.get('pushed_at') or '')[:10]} · "
          f"created {(m.get('created_at') or '')[:10]} · {m.get('language') or '-'} · {lic}"
          f"{' · ARCHIVED (a completion signal, never a verdict)' if m.get('archived') else ''}")
    print(f"   source   fork: {m.get('fork')} · parent: {rec.get('parent') or '-'} · "
          f"description: {m.get('description') or '-'}")
    state, hit = precheck(repo, rec.get("parent"))
    print(f"   precheck {state}{f' → {hit}' if hit else ''}"
          + ("  (settled without a read; the single-link rule)" if state != "pass" else ""))
    depth1, ext, data_dirs, docs_dir, n_assets, asset_dirs = tree_pack(rec)
    print(f"   tree     {rec.get('tree_status')} · {len(rec.get('names') or [])} paths · "
          f"src: {', '.join(f'{k} {v}' for k, v in ext) or 'NONE'}")
    print(f"            root: {' '.join(depth1[:18])}")
    print(f"            data-ish dirs: {', '.join(f'{d} {c}' for d, c in data_dirs) or 'none'} · "
          f"docs: {docs_dir}")
    print(f"            asset-like files: {n_assets}"
          + (f", under {' '.join(f'{d} {c}' for d, c in asset_dirs)}" if asset_dirs else "")
          + " — a hint for `assets`; the boundary claim is the README's or a side-doc's own sentence (E4)")
    dirs, n_dirs, n_src = source_dirs(rec)
    if dirs:
        print(f"   A3 src   {n_src} source file(s) in {n_dirs} dir(s): "
              + " · ".join(f"{d} {n} ({detail} · {pct})" for d, n, pct, detail in dirs))
        print(f"            where the code sits is half of A3 — is that directory the reconstruction, a "
              f"loader written around it, or a pointer to someone else's")
    subs = rec.get("submodules")
    if subs is not None:
        print("   A3 sub   none: every path in the tree is this repository's own" if not subs else
              f"   A3 sub   {len(subs)} submodule(s): {' '.join(subs[:6])}"
              f"{' …' if len(subs) > 6 else ''} — code that arrives by gitlink is not this tree's result")
    links = external_links(rec)
    print(f"   links    {len(links)} external repo link(s)"
          + (f": {' '.join(links[:6])} — check whether the reconstruction lives there, that is A3"
             if links else ": none"))
    if has:
        want, found = intersect_has(rec, has)
        print(f"   --has    {len(found)}/{len(want)} of your names are in the tree: {' '.join(found[:8])}"
              + (" — none: no vendor-source filenames present" if not found else ""))
    docs, spent = ([], 0) if not docs_cap else fetch_docs(repo, rec, docs_cap, refresh)
    if docs_cap:
        if docs:
            print(f"   docs     " + " · ".join(
                f"{d['path']} {d['chars']:,}c{' (truncated)' if d['truncated'] else ''}" for d in docs)
                + (f" — fetched now, {spent} request(s), cached for the next run" if spent
                   else " — from the cache, 0 requests"))
        else:
            print("   docs     no FAQ/ROADMAP/gaps/parity/notice file in the tree — README only, 0 requests")
    sources = blocks_of(rec, docs)
    hits = method_lines(sources, rec)
    print(f"   A2       {len(hits)} method-shaped sentence(s) — whole, markup stripped, ready to paste "
          f"into admission.a2_quote with the locator below it, or write no line")
    shown = set()
    for label, i, sh, s in hits:
        if s in shown:
            continue
        shown.add(s)
        loc = "description" if not label else f"{label}#{i}"
        print(f"     {loc:<20}{sh:<8}{s}")
        if label:
            print(f"     {'':<20}{'':<8}a2_read_at → \"{label} head#{i}, {rec.get('fetched', '-')}\"")
    caps = capability_lines(sources)
    print(f"   facts    {len(caps)} sentence(s) on formats, the asset boundary and unfinished state — "
          f"what desc, note and assets are written from")
    seen_cap = set()
    for label, i, s in caps:
        if s in seen_cap:
            continue
        seen_cap.add(s)
        print(f"     {f'{label}#{i}':<20}{s}")
    print("   decide   A1 who shipped it and did the rights holder release its source — the pack shows "
          "the licence field, not that. A2 which sentence above the entry quotes, and where it was read. "
          "A3 whether these paths are the reconstructed code, a mod loader, or a pointer.")
    print(f"   read: recorded in {record_read(repo, via)} — this slug now owes pending-<date>.json "
          f"or one decisions.jsonl line (merge.py --coverage)")


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
        cols = ["repo", "verdict", "stars", "forks", "watchers", "pushed", "created", "lang",
                "size_kb", "license", "archived", "src", "files", "e", "evidence", "flags", "quote"]
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
    ap.add_argument("command", choices=["check", "read"])
    ap.add_argument("--repos", help="file with one owner/repo per line")
    ap.add_argument("--repo", action="append", default=[], help="a single hand-named repository")
    ap.add_argument("--aggregate", help="data/games.json-style dump to sample instead")
    ap.add_argument("--band", default="0:1000000000", help="star window MIN:MAX for --aggregate")
    ap.add_argument("--sample", type=int, default=0)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--refresh", action="store_true", help="ignore the cache")
    ap.add_argument("--has", default="", help="read: file of filenames to look for in the cached tree")
    ap.add_argument("--docs", type=int, default=3,
                    help="read: side-docs to fetch per candidate (0 = README only)")
    ap.add_argument("--out", default="", help="check: TSV to write · read: also write the pack text here")
    ap.add_argument("--workers", type=int, default=4 if TOKEN else 1)
    a = ap.parse_args()

    if a.command == "read":
        repos = list(a.repo)
        if a.repos:
            repos = from_file(a.repos, a.limit) + repos
        if not repos:
            sys.exit("read takes --repo owner/repo or --repos FILE — it is the per-candidate pack, "
                     "not a sweep")
        print(f"evidence pack for {len(repos)} candidate(s); "
              f"{sum(1 for r in repos if cache_path(r).exists())} already cached")
        sink = sys.stdout
        tee = None
        if a.out:  # the pack is one screen per candidate; --out keeps it for the pending file's author
            Path(a.out).parent.mkdir(parents=True, exist_ok=True)
            tee = _Tee(sink, open(a.out, "w", encoding="utf-8"))
            sys.stdout = tee
        try:
            for r in repos:
                pack(r, a.refresh, a.has, a.docs)
        finally:
            sys.stdout = sink
            if tee:
                tee.close()
                print(f"pack written to {a.out}", file=sink)
        sys.exit(0)

    if a.aggregate:
        lo, hi = (int(x) for x in a.band.split(":"))
        repos = from_aggregate(a.aggregate, (lo, hi), a.sample)
    elif a.repos:
        repos = from_file(a.repos, a.limit)
    elif a.repo:
        repos = a.repo
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
