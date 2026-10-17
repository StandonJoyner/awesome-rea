# Contributing

This list is a set of **measurements**, not a set of opinions. The rules below exist so that every number in the README can be re-derived by someone else.

The short version for a PR is here. The full operational spec — filing precedents, the sourcing ledger, known coverage holes, and how the numbers are refreshed — is [AGENTS.md](AGENTS.md); the leads that have not become entries are in [WATCHLIST.md](WATCHLIST.md), and looking back over repositories already entered is [RECHECK.md](RECHECK.md).

## What belongs

Admission is three tests, all of them answered from the repository itself. A suggestion that cannot clear all three is a lead in [WATCHLIST.md](WATCHLIST.md), not an entry.

- **A1 — Provenance, in two halves.** There has to **be** something reconstructed — a program, engine, format or behaviour the rights holder actually shipped — and it has to have been arrived at **without the rights holder's source**: from a shipped binary, the original data or archives, or observed behaviour.
- **A2 — Claim.** The project's **own README or description states which method** it used: byte-matching decompilation or disassembly, clean-room engine reimplementation, format/protocol/driver/API reimplementation, port or static recompilation of the original binary, or a compatibility patch. Quote the sentence; do not infer it.
- **A3 — Artifact.** The linked repository **contains the reconstructed code** — not a compatibility database, showcase page, video, installer, run recipe, mod loader, or the documentation tree of a tool.

The classes that fail, in the order people hit them:

| You are looking at | Fails | |
| --- | --- | --- |
| Source the vendor or the author released, then compiled, continued or ported (`source-sdk-2013`, C&C Generals, Descent 3, Flash Player, `Werkkzeug3`, `TerryCavanagh/VVVVVV`, the Quake `ioq3`/`yquake2`/`vkQuake` family, `chocolate-doom`, `OpenJK`) | **A1** | Nothing was reconstructed — the code was handed over. |
| A debugger, decompiler, hex editor, dumper, launcher, or another awesome list | **A3** | This list carries outcomes, not instrumentation. |
| A trainer or memory editor | **A3** | The class was deleted from both READMEs on 2026-10-17 and M5 retired with it; its legal record is in AGENTS.md under `## Takedown and legal record`. |
| A ROM hack, fan level, randomizer, new content, or a multiplayer mod on someone else's port | **A1** | New work authored on top of a shipped work, not a reconstruction of it. |
| A fork whose upstream is already entered | **A3** | One link per result; the fork belongs as plain text in that paragraph. |
| A real project that publishes no method sentence | **A2** | Unprovable on one read, so it waits in `WATCHLIST.md` until the project states its method. |

**Failing admission is not a grade.** Star count, last-push age, license and whether an agent helped are **not** admission tests — write dormancy or a missing license into the line as a plain status phrase, never as a reason to drop a project. A rejection names the test the project failed and nothing else.

## Entry format

```markdown
- [owner/repo](https://github.com/owner/repo) - Title or product, original platform → destination, method, license if declared. ★ 1,234 · 12 forks · pushed 2026-10-15.
```

Required fields:

1. **A software-type section** — `Games`, `Applications`, `Runtimes and compatibility layers`, or `Formats, file systems and protocols`. Inside `Games`, also pick the platform subsection (`Nintendo`, `Sony PlayStation`, `Microsoft Xbox and Xbox 360`, `MS-DOS, Windows and Macintosh`, `Mobile`). The filing test for each section is in AGENTS.md, and it is applied only after A1–A3 pass; a new entry always goes in exactly one of them.
2. **Original platform** — the platform the thing being reconstructed ran on, in the vendor's own words, and for a port or recompile also where it runs now (`PS4 → Windows and Linux`). The type is carried by the section, so do not repeat it in the line.
3. **Method** — one of the four live labels: byte-matching decompilation or disassembly, clean-room engine reimplementation, format/protocol/driver/API reimplementation, port and static recompilation (or compatibility patch). Say which one in words, in the line; the M1–M4 ids are internal and never appear in a README (M5, trainer and memory editing, was retired with its section on 2026-10-17). There is no separate index of methods to update.
4. **Snapshot** — stars, and last-push or creation date wherever liveliness is part of the claim. Do not write a snapshot date into the entry: the README carries one refreshed date, and CI rewrites `★ <n>`, `<n> forks` and `pushed <date>` from `GET /repos/{owner}/{repo}`. A `created <date>` is a historical fact and stays.
5. **A resolvable path** — `https://github.com/{owner}/{repo}`, verified by opening it, not by remembering it.

Format rules the linter enforces, so learn them before CI does:

- The README is not hard-wrapped: one paragraph per line, entry bullets included.
- Link and description are separated by ` - `, and the description starts uppercase and ends with a period.
- Every URL appears exactly once in the README. Where a project belongs to two sections, link it in its type section and write its name as plain text in the other. The Related lists section names repositories in plain text for the same reason; so does the legal record in AGENTS.md.
- Section names stay short and are not self-explaining: `Games`, `Applications`, `Runtimes and compatibility layers`. If a name needs a paragraph to justify it, the paragraph goes in AGENTS.md and the name gets trimmed. Adding a section or a `Games` platform subsection means adding it to `Contents`, to `README.zh-CN.md`, and to the admission table in AGENTS.md.
- A list item either starts with a link (an entry) or is prose in a paragraph. Analysis without a link of its own goes in a paragraph, not a bullet.
- Write for a reader scanning a list: no rhetorical framings, no "most instructive entry" verdicts, no bold one-line moral closing a paragraph. How the list is built, verified and refreshed is AGENTS.md material, not README prose.

## How an entry leaves

Four reasons only, each with what to read first: the link is dead, a DMCA notice took it down, the project no longer meets a test it passed (`## What belongs`), or the sentence our line quotes turned out to be wrong. `AGENTS.md` `## Removal` is the table. Stars, push age, licence and `archived` remove nothing.

## Verification bar

- Call `GET https://api.github.com/repos/{owner}/{repo}` and copy the numbers from the response. Do not use a search engine's reported star count, and do not use a README badge.
- If you cite a legal outcome, read the filing, the notice text, or the project's own statement. If you cannot, write **⚠** plus what you actually read.
- If a claim rests on press coverage, say so in the entry.
- Negative findings are worth recording: "no offline-trainer acquittal found" is a real data point, and stating it stops the next person from inventing one.
- Do not guess URLs. A wrong slug is worse than a missing entry — `yuzuatri`, not `yuzatri`.
- Do not rewrite a quote from a video title, a README, or a filing to satisfy a spell checker. Keep it verbatim and let the warning stand.

## Style

- `README.md` is English; `README.zh-CN.md` is a full mirror of it — same sections, same entries, same ⚠ marks. Change both, or say in the PR which one you touched.
- No game files, no ROMs, no cracked binaries, no keys **in this repository**. Most entries ask the reader to supply their own licensed copy and say so in the line; an entry whose upstream tree carries the original assets is written as such, and this list still ships none of them.
- Retract visibly. If a number in this list is wrong, correct it in the same commit and keep the note explaining what was wrong and why it looked right.

## Checks before you open a PR

```console
$ npx awesome-lint README.md
$ python3 scripts/check-i18n.py
$ python3 scripts/verify.py links
$ GITHUB_TOKEN=$(gh auth token) python3 scripts/verify.py refresh --apply   # re-measure everything
```

Leave the numbers to the last command and the refresh workflow: a PR that only changes a description should not contain hand-edited star counts.

To check A3 and see what a repository publishes as proof, run the intake gate before you write anything — it is not in CI, because it reads new repositories rather than the ones already entered:

```console
$ GITHUB_TOKEN=$(gh auth token) python3 scripts/quality.py check --repos path/to/one-owner-per-line.txt
```

## PRs

One entry per PR is fine. A PR that adds entries without a type section, an original platform, or a method label will be closed with a request to add them.
