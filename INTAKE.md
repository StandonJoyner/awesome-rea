# INTAKE.md — how a repository becomes an entry

Read in this order: **`## Admission`** decides whether a candidate enters, **`## Filing axis`** where it files, **`## Method labels`** and **`## Entry mechanics`** what its line says, **`## The three stages and the three files`** how it is written down and rendered, and the last two sections where candidates come from. Nothing here is reader-facing product; `README.md` is. A number still comes only from `GET /repos/{owner}/{repo}`, through one of the two files the pipeline names.

## Admission: the three tests every entry has to pass

`## Filing axis` below decides **where** a project sits. This section decides whether it sits here at all. Admission is one rule with three parts, each answerable from the repository itself, in one pass, at intake:

- **A1 — Provenance, in two halves.** There has to **be** something reconstructed — a program, engine, format, platform or behaviour the rights holder actually shipped — and it has to have been arrived at **without the rights holder's source**: from a shipped binary, the original data or archives, or behaviour observed over a wire or through a save file. A project that builds on source the vendor or the author published itself fails the second half, because the thing we would count as a reconstruction is the thing that was handed over; a ROM hack, a fan level, a randomizer or an original game fails the first, because nothing shipped was taken apart.
- **A2 — Claim.** The repository's **own README or description states one of the four method shapes** — byte-matching decompilation or disassembly, clean-room engine reimplementation, format/protocol/driver/API reimplementation, port or static recompilation of the original binary (including a compatibility patch). Read it at write time and keep the sentence; an inference by the reviewer is not a claim, and neither is a search result's title.
- **A3 — Artifact.** The linked repository **contains the reconstructed code**. A compatibility database, a showcase page, a video, an installer, a run-recipe document, a mod loader, or a docs tree whose recompiler lives in a submodule is not an entry.

Six classes fail, and the class plus the test letter is what a rejection cites — never merit, never the star count:

| Does not enter | Fails | Because |
| --- | --- | --- |
| Source released by the rights holder, then compiled, continued or ported (`source-sdk-2013`, C&C Generals, Descent 3, Flash Player, `Werkkzeug3`, `TerryCavanagh/VVVVVV`, the `ioquake`/`yquake2`/`vkQuake`/`Quake3e`/`ironwail` family, `chocolate-doom`, `dhewm3`, `RBDOOM-3-BFG`, `JACoders/OpenJK`, `TheSuperHackers/GeneralsGameCode`, `Warzone2100`, `arx/ArxLibertatis`, `kripken/BananaBread`, `inolen/quakejs`) | **A1** | The code was given, so the artifact contains no reconstruction of it. |
| Instrumentation: debuggers, decompilers, hex editors, MCP bridges, dumpers, launchers, other lists (`ran-j/PS2Recomp`, `tgeorgiadis/quiver-launcher`, `michelpereira/awesome-open-source-games`) | **A3** | The product is a tool or a list, not an outcome; the boundary lists are named under Related lists. |
| Runtime read/write of another process's state — trainers and memory editors | **A3** | The class and its section were deleted 2026-10-17 and M5 retired; the record is in `AGENTS.md`, `## Takedown and legal record`. |
| Original or fan content, ROM hacks, new levels, randomizers, multiplayer mods on somebody else's port (`space-station-14`, `freedoom`, `celeste64`, `Rangi42/polishedcrystal`, `coop-deluxe/sm64coopdx`, `zsrtp/Randomizer`) | **A1** | Nothing shipped was reconstructed; new work was authored on top of the shipped work. |
| A fork of a repository already entered (`sm64-port/sm64-port`, `Keriew/augustus`, `Supermedo/bloodborne_pc`, `d07RiV/diabloweb`, `HayatoG/dusklight`) | **A3** + the single-link rule | The reader reaches the result through the one entry; the fork is prose in that paragraph. |
| A real project whose README publishes no method sentence at all | **A2** | Unprovable in one pass, so it stays a lead rather than an entry — and A2 is re-run the day the project states its method. |

- **What is machine-checkable and what is not.** `scripts/quality.py` answers A3 (404, `exclude` for no code or no README) and measures the E1–E4 completion evidence, but **no E-class or flag means "vendor source" or "the original binaries are in this tree"** — the A1 read is of the credits section, the README's own provenance sentences, and the repository root listing. `JoppieToppie/Galaxy-on-Fire-2-Unity-Remake` is the worked case: the gate returned `conditional` on its CI alone while `Reference/binaries/` held the shipped ARM library and a modded APK.
- **Nothing here or in `AGENTS.md` rules on what a linked repository's tree contains.** The only boundary rule we have is 「No game files, ROMs, cracked binaries, or keys anywhere in this repo」, and it constrains *our* tree; it was cited once as a reason to hold an entry and that citation was wrong, because a link to somebody else's repository is not our copy of their files. Whether a binary inside a third-party repository really is the rights holder's build cannot be determined from the outside, so on 2026-10-17 the owner declined to adopt a proposed rule that would have excluded such repositories (**「不加这条规则，我们没有能力判断仓库里放的是不是厂商的程序」**) and none was written. A1 still asks only *how the project obtained what it reconstructed*; where the project keeps its reference material is not an admission test, and it is not a recheck trigger either (see `RECHECK.md`).
- **Failing admission is not a quality judgement.** A vendor-source port can be excellent software and still not be a reconstruction; `soyrochus/mucrab` and `storytold/wordcraft` clear A1 on a behaviour claim with no binary at all. Write the test the project failed, in the rejection, and nothing else.
- **Passing is entering.** Owner's decision 2026-10-18 (「我现在要交出裁量权，不禁止的就是要收录的」, narrowed to the decidable half): a candidate read in a pass that clears A1–A3 is merged in that same pass, and `decide.py` no longer accepts a `defer` with `blocked_on=none` — a deferral must name the unresolved thing it waits on, a test to re-run or the filing level to create. What stays discretionary is **which candidates get read at all**: the batch, the priority band, where the pass stops. An unread project that would pass is not being held out; it has simply not been reached, and rate limits make some version of that choice unavoidable. `storytold/photocraft` is the worked case of the old way: read, passing, deferred 2026-10-17 on an editorial call, entered 2026-10-18 when the owner revoked that discretion — both ledger lines stay as the record.
- **Stars, push age, license and `ai_flag` are not admission tests.** A ★×age band orders *attention* and is written into a line as a status phrase when a project has gone quiet; a license gap is stated in the line; how a result was produced is an attribute. None of them opens or closes the door — A1–A3 do. That is why a numeric bar cannot be used to drop the source-port class: those repositories are large and active by construction.

## Filing axis: kind of software, then platform

Sections are the **kind of software that was reconstructed**, because that is the question a scanner is asking: is there a game here I can play, and is there a component here I can reuse. These are **filing** tests, applied only after A1–A3 pass — they say which section, not whether the project enters.

| Section                                | Filing test                                                                                                     |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `## Games`                             | The artifact **is a shipped game** (or an engine that plays them). Second level = the **original platform**.        |
| `## Applications`                      | The artifact is a non-game program: a player runtime, an office application, a desktop utility.                      |
| `## Runtimes and compatibility layers` | The artifact is the platform the program expects: an API, firmware interface, managed runtime, emulator, or the patch that unblocks a title on a new host. |
| `## Formats, file systems and protocols` | The artifact is a data structure or a wire protocol reimplemented from observation.                                |

Four type sections since 2026-10-17: the fifth, `## Trainers and modifiers`, was deleted with its four entries, so a repository whose artifact reads or writes another process's memory at runtime has no filing home and fails A3, and does not enter. The removed class and its legal record are in `AGENTS.md`, `## Takedown and legal record`.

`Games` second levels: `### Nintendo`, `### Sony PlayStation`, `### Microsoft Xbox and Xbox 360`, `### MS-DOS, Windows and Macintosh`, `### Home computers`, `### Mobile`, keyed on the platform the original software ran on. Add a platform level only when an entered title's original platform is not covered by one that exists — the Xbox level was created on 2026-10-16 for three titles, `### Mobile` on 2026-10-17 for one (`Galaxy on Fire 2`, Android and iOS), `### Home computers` on 2026-10-17 for two (`Pyrdacor/Ambermoon.net` on the Amiga, `skoolkid/pyskool` on the Sinclair ZX Spectrum), none as a placeholder. The home-computer level covers the 8- and 16-bit machines that are neither a PC nor a console; a title whose original ran on both a home computer and DOS files under the PC level with both named in its line, because the heading is one home and the line carries the rest (`Pyrdacor/freeserf.net`: DOS and Amiga data). A destination belongs in the entry line, never in a heading (`PS4 → Windows and Linux`).

Precedents set while re-filing, follow them for new entries:

- `jhaizhou-ops/d2r-mobile` is **Games / Nintendo** (Switch), not Runtimes: it reimplements a platform surface, but the artifact the reader gets is Diablo II running on a Mac.
- `JoppieToppie/Galaxy-on-Fire-2-Unity-Remake` is **Games / Mobile**, keyed on Android and iOS as the platform the original ran on — the same test that puts a Switch→iOS recompile under Nintendo rather than here. Its line is the one place in the README that says the reconstruction ships the original assets, because it does; `## Games`' intro is worded to allow that one entry rather than to describe the corpus. Whether a linked repository holds vendor binaries is not a thing either file rules on (see `## Admission` above).
- `yuzuatri/Sengoku-Rance-Deck-Fix` is **Runtimes and compatibility layers** even though it patches one game: what was reconstructed is the missing codepage behaviour, and it sits next to the Wine paragraph that explains it.
- `azahar-emu/azahar` is **Runtimes** (it runs games but is not a game); `ruffle-rs/ruffle`, `storytold/wordcraft`, `soyrochus/mucrab` are **Applications**; `kichikuou/xsys35c` is **Formats** (a bytecode format's compiler and decompiler), while `kichikuou/xsystem4` is **Games** (it plays AliceSoft titles).
- `gibbed/Gibbed.LetUsClingTogether` is **Formats** on the `xsys35c` precedent even though its own README opens "Tools for modding": what the linked repository holds is the read of the game's data structures — 152 .cs files, 53 of them in the `…FileFormats` projects, and `docs/` with the cutscene opcode and text-encoding tables. So the rule for a mod-tool self-description is: **file on the artifact, not the purpose**, and A3 decides it — format libraries and importers/exporters of the reconstructed structures are in, a repository that only ships a loader, redirect or save-scumming hook into the shipped game is not.
- The one ledger section left at the bottom of the README (`Related lists`) is a ledger, not a type section. A repository mentioned there is linked once, in its type section, and written as plain text here. `Takedown and licence history` was the other ledger until 2026-10-17; its content is now `AGENTS.md`, `## Takedown and legal record`.

## Method labels: four live internal ids, written inline

M1–M5 are **internal ids for the method label written into each entry line**; M5 is retired (see the table below), so four are in use. They are no longer the filing axis — `## Filing axis` above is — and the codes themselves never appear in a README. Since 2026-10-16 there is also no README paragraph set that groups repositories by them. Every project still has exactly one home, and that home is a type section. These must never become sections either: how a result was produced (agent, Ghidra, a person), how it attracted attention (a short-video wave), what its license is, whether it was taken down. Those are attributes to write into the entry, or material for `## Takedown and legal record` in `AGENTS.md`.

M5 — trainer and memory editing — was **retired on 2026-10-17** with the `## Trainers and modifiers` section. The id survives here so an old entry line is not reinterpreted, but no repository admitted on that signal belongs in the README now.

Judge by **what the artifact is**, not by the technique used to obtain it:

| Signal in the artifact | Id | Label the README line uses |
| --- | --- | --- |
| source that diffs against / compiles byte-identical to the shipped binary; "matching bytes", "exact reconstruction" | M1 | Byte-matching decompilation and disassembly |
| a new engine or application that **consumes the original data/archives**, containing no original code | M2 | Clean-room engine reimplementation |
| a behaviour-compatible reimplementation of a format, protocol, driver or API, obtained by black-box observation / spec drafting / differential testing | M3 | Format, protocol, driver and API reimplementation |
| the original binary running somewhere it did not before — ports, static recompilations | M4 | Port and static recompilation |
| shims, patchers and compatibility fixes for one host | M4 | Compatibility patch |
| runtime read/write of another process's state | ~~M5~~ | retired 2026-10-17 with the `Trainers and modifiers` section — such a repository is not admitted by type any more |

M4 covers two README labels: use **Port and static recompilation** when the artifact moves a whole game to a new platform, **Compatibility patch** when it unblocks one title on a host it already nominally supported.

Precedents set while re-filing the list (follow them for new entries):

- Static recompilation of a console game to a new platform is **M4 / Port and static recompilation** (`gow3_pc`, `Tekken3Recomp`, `god-of-war-recomp`, `tkdr-recomp`, `TeamGDB/Yakumo`): recompilation is the means, "runs where it did not before" is the product.
- `N0zoM1z0/th04` and `N0zoM1z0/dx-ball` are **M1** on the strength of their own claims ("2,139 matching bytes", "exact reconstruction is in progress"). If a project later drops the byte-matching claim, reclassify.
- `soyrochus/mucrab` is **M3**, not M2: it reimplements an application's observed behaviour and consumes no original game data.
- `storytold/wordcraft` is **M2** and is *not* agent-RE output: it is filed clean-room on the strength of its own README, which since 2026-10-16 reads "Clean-room: built from public specifications and observation, with every asset original or openly licensed". The earlier sentence this bullet and the README line quoted ("we explicitly do not use reverse engineering… 100% clean room") is **no longer in that repository** — code search for it returns `total_count = 0` — so the README now quotes the current text; see `## Sourcing ledger` in `AGENTS.md`. Never label clean-room work as agent output. `sushi-shi/homm1-decomp` belongs to a different model; `Moxnatiy/OpenBattlefield2` is Ghidra work.
- Officially released source that merely got compiled is **not RE** and fails admission at **A1**; the class, the worked examples and the reason live in `## Admission` above. Do not file such a repository under a method label, and do not link it from a type section.
- Tools (debuggers, decompilers, hex editors, MCP bridges) are out of scope entirely, at **A3**; the boundary lists are named under "Related lists".

## Entry mechanics

```markdown
- [owner/repo](https://github.com/owner/repo) - Title or product, original platform → destination, method label. ★ 1,234.
```

- Real examples of the shape: `- Zelda: Ocarina of Time, Nintendo 64, byte-matching decompilation.` / `- God of War III Remastered, PS4 → Windows and Linux, static recompilation of the original console binary, C++.`
- **Nothing after the ★ but the star count, and no licence anywhere in the line** (the owner's rule of
  2026-10-17: 「不要显示license，后面只展示star数，其他不要」). Measured before the change, over 159 entries: 108 fork
  tokens, 107 push-date tokens, 30 `created <date>` literals, 3 licence literals, and 122 descriptions ending
  on a licence clause — all of it stripped in one pass and re-rendered, with no non-licence text lost (the
  pass was verified segment by segment). `forks`, `pushed`, `archived` and `license_spdx` stay in `measured`:
  `RECHECK.md`'s triggers read them, and the refresh keeps them true; the reader simply no longer sees them.
  `merge.py` now fails a pending object whose `tokens` are not exactly `[stars]`, and one whose `desc` ends on
  a licence clause, so the shape cannot drift back — `BSD` counts as an operating system, only `BSD-<n>` is a
  licence.
- The **software type comes from the section**, so never repeat it in the line — no `**Game code**` prefix any more.
- The link must be a repository that contains code. The description starts uppercase, ends with a period, and is separated from the link by ` - `.
- A port or recompile states both ends (`PS4 → Windows and Linux`); a non-port states only the platform it came from. Platform names are the vendor's own (Nintendo 64, not "N64" on first use).
- A list item either starts with a link (an entry) or is prose in a paragraph. Analysis without a link of its own goes in a paragraph, never a bullet.
- **No hard-wrapping**: one paragraph per line, entry bullets included.
- Every URL appears **exactly once** in each README — `awesome-lint` fails on a duplicate. Where a project matters to two sections, link it in its type section and write its name as plain text (`owner/repo`) in the other; `Related lists` is plain text for that reason. That is also why the GitHub REST endpoint appears in the data-provenance line as code, not as a link.
- Keep tables narrow enough that a wide cell is not needed: a row carrying twenty names belongs in prose, and since 2026-10-16 nothing in the README is that shape.
- Entries within a section are listed **largest-first by stars as a courtesy**, not as a claim: a number refresh rewrites the numbers and never the line order, so the order goes stale by design. Never cite the ordering as data.
- This is the shape the README *shows*. From the first render of `entries.json` (`## The three stages and the three files` below) it is output: the bullets are generated, and a contributor edits the json and the sentence inside it, not the rendered line.
- `## Contents` must be the first section and must not list `Contributing`, `Footnotes`, or a licence; no `## Licence` section and no CI badge; no logo requirement unmet if you add one. Nested `###` platform levels are listed in `Contents` as sub-items.
- Do not write a measurement date into a rendered line: the refreshed-date line comes from `entries.json`'s `refreshed`, so anything hand-written there ("re-read from the API on 2026-10-16", "measured 2026-10-16") is overwritten by the next render. It is the only snapshot date in the README; a `created <date>` is a historical fact and is allowed.
- Write for a reader who is scanning a list, not for a reader of our essay: no rhetorical framings like "the class most useful to 'get my old game running here'", no "cautionary tale" / "the most instructive entry" verdicts, and no bold one-line moral at the end of a paragraph. State what the project does, what was reconstructed, and what the numbers are; leave the judgement implicit in the entry list.
- Fidelity distinctions that only our filing procedure cares about (byte-matching vs reassembles-to-ROM, for instance) stay in the entry line as two words, never in a paragraph explaining the ladder.
- The colliding name stays recorded here only: `kaixinbaba/awesome-rea` exists at 5★ and presents OpenMW / ScummVM / OpenRA / Ruffle as "rea" results, which they are not — those are decades-old projects with no agent in their history, and this list's naming paragraph is what makes that distinction. The entry was deleted from Related lists on 2026-10-16: a same-name list we rate badly is not a resource a reader needs. Recognisability beat uniqueness, and this bullet is where the collision is documented.

## The three stages and the three files

Standardised 2026-10-17. **The corpus is now built with them.** `parse.py` read the two READMEs and the newest snapshot back into `entries.json`, the migration test below passed, and two merges have since been written through stage 3 and committed (`88a4d6e`: eleven entries, then three): the json holds every entry, token wording and paragraph the files carry, and **the READMEs are output only**. `--out` and `--decisions` still exist for a run against a copy of the corpus, which is how a batch is exercised before it touches the committed file.

So `verify.py refresh --apply` is the measurement step and nothing more: it writes the snapshot `merge.py` copies from, then puts this run's numbers into `entries.json`'s `measured` and its date into `refreshed`. **It does not touch either README, and neither may a hand** — `render.py` writes them from the corpus, which is why `render.py --check` is a CI gate now (`lint.yml`, and in the refresh job before that PR opens). One trap in the commands below: `--coverage` is the gate, not the merge — `merge.py pending.json` writes the corpus, `merge.py --coverage` only checks it, and `render.py` then writes both READMEs.

| Stage | Input | Output | Committed |
| --- | --- | --- | --- |
| **1 Pre-screen** | a search, a source catalogue, or a repository the owner names | `data/measurement/candidates-<date>.tsv`, one row per candidate | no — measurement, like every snapshot |
| **2 Read** | one candidate row at a time, from `quality.py read`'s evidence pack | `pending-<date>.json` — the accepted entry objects; a refusal goes to `decisions.jsonl` instead | yes, with the PR |
| **3 Merge and render** | `entries.json` plus a pending file | merged `entries.json`, then `README.md` and `README.zh-CN.md` | all three; the READMEs are output, never hand-edited |

Stage 2's object is the same shape stage 3 stores, so merging is an insert, not a translation — no format layer sits between the read and the corpus, which is where a generated list usually starts lying. The insert is positioned by star count **inside the heading it files under, and nothing already there is moved**: a full re-sort would rewrite both READMEs for no reader-visible reason, and `## Entry mechanics` already says the order is a courtesy. A rejection is not a pending object: it is one `decisions.jsonl` line, and that is what makes a refusal checkable after the uncommitted TSV is gone — the row, the sentence read, and the test letter all survive. `pending-<date>.json`, the accepted array, is committed with the PR so a reviewer sees what was read, and the merge commit removes it.

## The pass, and what it forbids

One intake pass is five steps, in this order, and nothing else:

```console
$ python3 scripts/preflight.py --repos /path/to/batch.txt      # 1  measure + pre-screen: one request per slug
$ python3 scripts/quality.py read --repos /path/to/batch.txt   # 2  the whole pack: README + side-docs, sentences untruncated, 0 requests if cached
$ …the A1–A3 read, from the pack alone…                        # 3  the only step that is a judgement, not plumbing
$ python3 scripts/decide.py … · write pending-<date>.json      # 4  every row read gets a disposition, either way
$ python3 scripts/merge.py pending-<date>.json                 # 5a merge into entries.json
$ python3 scripts/render.py                                    # 5b regenerate BOTH READMEs from the corpus
$ python3 scripts/merge.py --coverage                          # 5c the gate: no read left without a disposition
```

Step 5 is three commands because none of them implies the next: the merge does not render, and the coverage
gate does not merge. **A pass that stops after 5a has changed the committed corpus and left the product
unchanged** — the two READMEs move only when `render.py` writes them, never by hand. `merge.py` prints this
chain after a successful write (`next: render.py && render.py --check && check-i18n.py && merge.py --coverage`);
follow it rather than remembering it.

Measured over the first full pass (18 rows, 2026-10-17): 2 were settled by `precheck` without any read, 5 ended
as ledger lines, and the queue came down to **11 judgement reads**. Everything spent beyond those is in the list
below, so it is now forbidden rather than merely discouraged:

- **Do not fetch evidence twice.** `data/cache/quality/` holds the metadata, the README and the recursive tree,
  and `quality.py read` prints from it; three of that pass's calls re-read cached files, one of them a
  7,555-path tree. New evidence means `quality.py read --refresh`, with the reason in the ledger note.
- **Do not read the corpus to learn the format.** The entry-object schema, the four token kinds and their
  per-language wording are written out in `### data/entries.json` below. That pass dumped 40 rendered lines and
  counted characters before writing one object: O(corpus) work per batch to recover a rule the document already
  states.
- **Do not run stage 1 twice on one day.** `preflight.py` overwrites `candidates-<date>.tsv`, so a 1-row run
  destroyed that batch's 17-row file and re-measuring cost 18 requests. Name the whole batch in one call. The
  overwrite is a known defect; the ban is the mitigation until the file is versioned per run.
- **Do not improvise a preview.** No importing `render.py`, no scratch script, no hand-written bullet quoted back
  as though it were rendered. `merge.py --dry-run` reports the insert position and which file each number came
  from, and the rendered line is stage 3's output, not stage 2's input.
- **Do not leave a verdict in a reply.** `merge.py --coverage` fails if a slug recorded in
  `data/measurement/read-<date>.tsv` (which `quality.py read` appends to) has no disposition in the corpus, in
  the pending file, or in `decisions.jsonl`. Eleven of the first pass's 18 rows existed only as a table in a chat
  message — the exact failure the gate exists to catch.
- **Do not defer a passing project.** `decide.py` refuses a `defer` unless it names the open thing it waits on — an A-test to re-run or the filing level to create. The discretion in a pass is which slugs it reads, not which passing ones it keeps out (`## Admission`).
- **Do not read the cached README by hand.** No `cat` of `data/cache/quality/*.json`, no throwaway script to
  pull a line out of it. The pass that followed the ban below's first run spent **six python calls on three
  candidates**: stage 1 (1), the pack (1), two failed invocations of my own making, and three inline scripts
  reading the cache — because the pack truncated each sentence at 180 characters and could not see that a
  README paragraph wraps over three lines, so the verbatim `a2_quote` it was supposed to supply was not
  really on the screen. `quality.py read` now caches the README as paragraph blocks (`readme_blocks`, fenced
  code dropped) and prints whole sentences with the `a2_read_at` string to paste beside them, plus a `facts`
  block of the format/boundary/unfinished sentences `desc`, `note` and `assets` are written from. A cache
  written before that field costs one re-read, and the pack says so. If a sentence is still missing from the
  screen, **the fix is the pack, not a fourth script.**
- **Do not fetch a side-doc instead.** The same ban covers `FAQ.md`, `ROADMAP.md`, a gaps or parity file and
  `NOTICE.md`, which is where the asset boundary and the unfinished-state admission often live: on
  2026-10-17 a batch read cost **five extra raw requests on one candidate** because the pack quoted only
  `README.md` and the sentence that settled its `note` was in `FAQ.md`. The pack now shortlists those names
  **from the cached tree** (so a repository without them costs nothing and a wrong filename cannot be
  fetched), pulls at most three per candidate, 20 KB each, caches them in the same record, and prints their
  sentences into `A2` and `facts` with a locator that names the file — `FAQ.md head#37, 2026-10-17`. It is
  one basename per slot: a root `ROADMAP.md` and a `docs/roadmap.md` copy do not both get fetched. `--docs N`
  sets the cap, `--docs 0` is the README-only pack of before. Measured cost: `storytold/deckcraft` 3
  requests on a first read, **0 on the second**, and its `docs/gaps.md` lines (`.odp` unsupported,
  `vbaProject.bin` untouched, SVG not rendered) reach the screen that previously cost three calls.
- **Do not guess where the code is.** A3 asks whether the tree holds the reconstruction, and `--has` could
  only ever test filenames the reader already guessed. The pack now prints the source files grouped by
  top-level directory with each directory's share (`A3 src`) and the gitlinks it found (`A3 sub`) — both
  computed from the tree that is already cached, at **zero requests**, and neither is a verdict: 130 of
  `RSDKModding/RSDKv4-Decompilation`'s 148 source files sit in `RSDKv4/` while its four submodules are
  vendored libraries, which is the opposite situation to a repository whose "reconstruction" is a submodule
  pointer.
- **Do not make the editorial calls.** A new `###` platform level, and any borderline class decision (is a
  format library whose README says "tools for modding" a result?), are the owner's — until they say 你来定,
  which transfers exactly the calls it names, for that batch, and no others. `merge.py` already refuses a
  heading that does not exist in both READMEs; the correct output is `decide.py defer --blocked-on filing`
  plus the question, not a heading invented in a PR.

Rules stated elsewhere stay in force and are not repeated here: no hand-edited README, no invented or edited
number, no guessed slug, no quote rewritten from memory — see `## Entry mechanics`, `### The commands` below and
`AGENTS.md`, `## Sourcing ledger`. This list is only about the second kind of error: work an agent did that the
flow never asked for.

### `data/measurement/candidates-<date>.tsv` (stage 1, not committed)

Column names are `quality.py`'s, so its rows flow in unchanged.

```
slug  source  priority  stars  forks  watchers  pushed  created  lang  size_kb
license  archived  upstream_type  precheck  blocked_on  verdict  e  flags  quote  next
```

- `slug` is the key and is only written after `GET /repos/{owner}/{repo}` answers 200 — never a guessed URL. This is all stage 1 costs: **one metadata request per candidate**, no README and no file tree; stage 2 pays for the README and the tree, once, and only for the rows it reads.
- `source` = `search` · `catalogue` · `owner`. `blocked_on` = `A1` · `A2` · `A3` · `filing` · `none`, and `verdict`, `e`, `flags`, `quote` are stage 2's, taken from `quality.py`. `upstream_type` is filled only where a source supplies one (`decompilation`, `static-recomp`, `source-port`, …) — a hint, never a verdict.
- `priority` = `P1`–`P4`, the ★×recency band, defined in `scripts/preflight.py` as **P1** ★≥1,000 or (★≥100 and pushed within 90 days) · **P2** ★≥100 or (★≥10 within 90 days) · **P3** ★≥10 · **P4** the rest. **It orders work and decides how many rows a pass reads; it does not decide admission.** It is carried no further than this file: an entry object has no `priority`, because a reader cannot evaluate one.
  - Measured 2026-10-17 over the newest corpus snapshot (136 rows): **P1 118 · P2 10 · P3 2 · P4 6** — 86.8% of what is entered sits in the top band, so the band ranks the queue, not the corpus.
  - Measured over that upstream queue (`data/games.json`, 2,118 rows read 2026-10-17, this list's slugs removed and duplicates folded: 1,937 rows): **P1 367 · P2 861 · P3 511 · P4 198**. The 367 P1 rows are `decompilation` 106 · `static-recomp` 93 · `source-port` 77 · `engine-remake` 70 by upstream `type` — a hint, not a verdict: `source-port` straddles `## Method labels`, because a port built on a *decompilation* is M4 and admissible while a build on *vendor-released source* is not a result at all, and no upstream `type` field tells the two apart. Read together: a P1 pass costs 367 metadata requests in stage 1, and stage 2 is where the per-row human read begins.
- `precheck` = `pass` · `already-entered` · `fork-of-entered` — the only three states the API settles without prose: the slug is in the corpus, or its `parent`/`source` field names a repository that is. `already-entered` sets `next` to *nothing — the reader already has it through one entry*, `fork-of-entered` to *write its facts into the parent entry's paragraph, then refuse it*; both are the single-link rule of `## Entry mechanics`, applied before anyone opens a README. The fork class is the one the API, not words, settles: over the four recorded fork refusals `parent`/`source` catches 3 (`Keriew/augustus` → `bvschaik/julius`, `Supermedo/bloodborne_pc` → `deadinside28/bloodborne_pc`, `sm64-port/sm64-port` → `n64decomp/sm64`) and misses `d07RiV/diabloweb`, a WebAssembly build *of* a devilution fork rather than a fork of one, which has no `parent` and stays a prose read at stage 2.
- The three class words this column was drafted with — `vendor-source`, `tool-or-list`, `mod-or-hack` — were **measured out of the script on 2026-10-17** and are stage-2 human verdicts recorded in `blocked_on` and in the `decisions.jsonl` line. Screening a README for those words false-flagged **33 of the 136** entered repositories over the first 120 lines, and **1 of 136** narrowed to the description plus 8 lines anchored on a copula; against the 32 upstream refusal rows that band had, the same screen caught **4** — vendor-source 1/16 (`arx/ArxLibertatis` alone), tool-or-list 0/3, mod-or-hack 3/13. Filtering therefore runs **negatively**: positive method vocabulary is a weak and adversely correlated filter (over the 2,118-row pool it kept 57% overall and 44% of the ★≥1,000 band — the stricter the word list, the more real results it dropped).
- `next` is one verb phrase — `read its README for the method claim` for a `pass` row, plus the two settled strings above — required whenever `quote` is empty and `blocked_on=A2`, and written by stage 1 for every row, so a queue is never a list of rows without an instruction.

### `data/entries.json` (the corpus — committed, and written only by the pipeline)

One object per entry, plus `header`, `sections` and `notes` for the prose the READMEs carry — measured at
8,533 of 41,023 characters in `README.md`, which is why prose is in the schema: json that held only bullets
would render a list that reads as machine output.

`merge.py` and `parse.py` both write it with `json.dumps(..., ensure_ascii=False, indent=2)`, and that is the
form committed here. It matters only for review: a writer at any other indent reflows all 7,000 lines, turning
a three-entry merge into a 13,883-line diff in which no reviewer can find the three entries. If a merge ever
shows a whole-file diff, the indent is the first thing to check, not the merge.

**A new filing level is inserted in `sections`, and then the corpus is renumbered.** An entry's heading comes from
its own `section` and `platform` names; the `_section_index` each entry carries is a cache of that answer, because
inserting a `###` between two existing levels shifts every position after it. Both the render and the merge resolve
by name, and `render.py` **refuses** a corpus whose cache disagrees, printing the slugs and their real index — the
command that repairs it is `python3 scripts/render.py --renumber`, which writes only those numbers and touches no
heading. Measured the hard way on 2026-10-17: a `### Sega` level added to `sections` without renumbering left 103
entries one heading away from home and rendered the whole `MS-DOS, Windows and Macintosh` block under `### Sega`,
while `render.py --check` and `check-i18n.py` both passed — they prove the two files are the render and its mirror,
not that the render filed anything correctly.

| Field | Written by | Printed | Notes |
| --- | --- | --- | --- |
| `slug` | stage 2 | link text | key; unique; `url` is derived from it and never stored, so a mistyped owner cannot survive a refresh — `parse.py` fails if a README's link text and its URL path ever disagree |
| `section`, `platform` | stage 2 | no | the filing result from `## Filing axis`; `platform` only inside `Games` |
| `desc` `{en, zh}` | stage 2 | yes | the sentence between ` - ` and `★`, verbatim; it carries no licence clause and no `created <date>` — both left the line on 2026-10-17, and `merge.py` refuses a `desc` that ends on a licence statement |
| `tokens` | stage 2 builds it, stage 3 fills it | yes | the number tail, as an ordered list — see below |
| `note` `{en, zh}` | stage 2 | yes | the closing sentence after the last token; 11 entries have one, and a number refresh rewrites the tokens beside it, never this |
| `measured` | `verify.py refresh` writes it, `merge.py` copies it | via `tokens` | `stars` `forks` `pushed` `archived` `license_spdx` `snapshot` — copied from `GET /repos/{owner}/{repo}` output and nothing else; see the number path under `### The commands` |
| `method` | stage 2 | no | `M1`–`M4` |
| `admission` | stage 2 | no | `a1` (the provenance sentence read), `a2_quote`, `a2_read_at` (the file the quote came from and its line — `README.md head#12, 2026-10-17`, or `FAQ.md head#37, …`; the pack prints the string ready to paste), `a3` |
| `assets` | stage 2 | no | `reader-supplied` · `shipped` · `none-needed`; the sentence `## Games` opens with depends on it |
| `priority` | — | — | deliberately absent |

`tokens` is what lets a rendered README match a hand-written one byte for byte. **Since the owner's 2026-10-17
rule one kind is in use, on every line:**

```jsonc
"tokens": [ {"t":"stars","field":"stars","en":"★ {stars}","zh":"★ {stars}"} ]
```

`forks`, `pushed` and `literal` stay implemented and remain in the schema — the renderer still joins with
`" · "`, a filled token still has to name its own field and carry `{field}` in both languages, and the corpus
below the rule is what that machinery was built for. Measured over the 146 bullets that printed a ★ after the
first real merge, the tail was **four** kinds in one order, every line `stars` → `forks` → `pushed` with at
most one literal inserted: 39 print only `★`, 96 print forks, 107 print a date, 10 print two dates, and 25
tokens are literals — 22 `created <date>` and 3 licence words (`d2r-mobile`, `Sengoku-Rance-Deck-Fix`,
`SubmitGame/awesome-decomp-games`). A created date is a literal rather than a filled field because it is a
historical fact: a refresh rewrites `pushed`, never `created`.

Joined with `" · "`. Every token stores **its own wording per locale**, with `{field}` naming which
`measured` value fills it; the value itself is never in the json, only its name. That is what makes the
render exact rather than merely plausible: over the 117 date tokens on those 107 lines, English prints
`pushed` 88, `created` 22, `last push` 5, `created and pushed` 1, `archived, last push` 1, and Chinese
prints `推送于` 88, `建库于` 22, `最近推送` 5, `建库与推送于` 1, `已归档，最近推送` 1 — count for count, with 10 lines
carrying two. A renderer that derived the word from the field name would get 29 of the 107 wrong:
`README.md:87` reads `created 2024-09-28 · last push 2026-04-03`, `README.md:125` reads
`archived, last push 2023-04-13`. The wording is data, not formatting.

`merge.py` holds a pending object to that shape before it writes anything: the kind must be one of the
four, a filled token must name its own field and carry `{field}` in **both** languages, a literal must name
no field and print no placeholder, `method` must be `M1`–`M4`, `assets` one of the three, the slug absent
from the corpus, and the `section`/`platform` pair already a heading on both sides. Any problem stops the
file: **a pending batch merges whole or not at all**, because a half-merged batch is not reviewable and a
rejected row would silently disappear from the PR.

A **`note`** (`{en, zh}`, after the last token, outside the bracket) is a closing sentence — 13 of the 146
have one, in each language on the same slugs (`Its README declares LLM-assisted coding.`, `A post claims a
Steam build runs; the repository does not say so.`, and eleven others). It is separate from the tokens
because a refresh leaves it alone. Numbers agree across the two files today — 0 divergences measured
over 146 slugs — which the merge then guarantees instead of leaving to a reader's eye.

### `data/decisions.jsonl` (append-only)

Seven fixed keys, always in that order: `date`, `slug`, `decision` (`admit` · `refuse` · `defer` ·
`wording-fix` · `remove`), `blocked_on`, `quote` (the sentence actually read), `read_at` (which file),
`note`. `merge.py` writes the `admit` lines from the object it just merged; `scripts/decide.py` writes the
other four and refuses to write a line it cannot audit — a `refuse` with no A-test, or with no `quote` and
no `read_at`, exits 2 rather than appending; a `remove` has to name one of the four reasons in
`AGENTS.md`'s `## Removal`; a `defer` has to say what it waits for or whose editorial call it is. That validator is what
makes a rejection auditable after the uncommitted TSV is gone. A `defer` with `blocked_on=none` is the
honest shape for a project that passes A1–A3 and is held out for a list-shape reason — the owner's
`storytold/photocraft` call of 2026-10-16 is the first line in the file. A `defer` with
`blocked_on=filing` is the shape for a read that clears A1–A3 but has no heading to file under: the level
itself is the owner's editorial call (`## The pass, and what it forbids`), and the line is what keeps the
read on record while it waits.

The gate's input is `data/measurement/read-<date>.tsv` — one line per `quality.py read`, columns
`slug read via`, gitignored like every other measurement file. It records only that a repository was
opened, and claims nothing about it; `merge.py --coverage` is what turns that into the rule that an opened
repository cannot be left undecided.

### The commands

```console
$ python3 scripts/preflight.py --repo owner/repo                       # stage 1, one candidate the owner named
$ python3 scripts/preflight.py --repos path/to/one-owner-per-line.txt   # stage 1, a search result
$ python3 scripts/preflight.py --aggregate data.json --band 100:999     # stage 1, a catalogue dump
$ python3 scripts/quality.py read --repo owner/repo                     # stage 2, the evidence pack; records the read
$ python3 scripts/quality.py read --repos batch.txt --has names.txt     #   batched; --has intersects the cached tree
$ python3 scripts/quality.py read --repos batch.txt --docs 0            #   README-only pack: no side-doc requests at all
$ python3 scripts/quality.py check --repo owner/repo                    # stage 2's machine half: verdict, e, flags, quote
$ python3 scripts/merge.py --coverage                                  # the pass gate: no read without a disposition
$ python3 scripts/merge.py pending-<date>.json --dry-run                # stage 3, what would enter and where
$ python3 scripts/merge.py pending-<date>.json                          # stage 3: append, position, copy measured
$ python3 scripts/render.py                                             # stage 3: write both READMEs
$ python3 scripts/render.py --check                                     # the acceptance test below, for CI
$ python3 scripts/decide.py defer --slug owner/repo --blocked-on none --quote "…" --read-at README.md --note "…"
$ python3 scripts/parse.py                                              # READMEs + newest snapshot -> entries.json
```

`--dry-run` prints the planned insert position and the file each number came from, and writes nothing;
`--out` and `--decisions` point the two writes elsewhere, which is how a merge is tested against a copy of
the corpus before the corpus is committed.

`parse.py` needs a snapshot (`verify.py refresh`) because `measured` is copied from it, never read off a
README line; an entry with no snapshot row comes back with `measured: null` and its slug is printed, so the
gap is visible instead of silently rendering a number that was never read. It asserts as it goes: the two
files line-parallel, the same link text and URL on each pair, that every URL is exactly
`https://github.com/{slug}` for the text beside it (so a wrong owner cannot survive a refresh), the same
token count and kind per language, a closing note in both languages or neither, every `Contents` anchor
equal to the one derived from its heading in its own language, and no duplicate slug.

**The number path.** `GET /repos/{owner}/{repo}` is the only place a number is obtained (see
`AGENTS.md`, `## Refresh automation`), and it reaches the corpus through two files and no other: `verify.py refresh`
writes the snapshot of everything both READMEs already link, and `preflight.py` writes the same fields for
a candidate **too new to be in a snapshot** — a slug cannot appear in `refresh`'s output before it appears
in a README, so stage 1's file is what a first merge reads. The merge copies from one of the two, prints
which one, and invents nothing. Nothing else may fill `measured`.

### What the renderer must not do

- Invent or add a number: a token absent from `measured` renders nothing, and a slug the refresh did not measure keeps its last-known numbers rather than gaining a `★`.
- Reorder in a way the reader can take as data (order is a courtesy — `## Entry mechanics`).
- Emit a URL twice in one file, or write a heading in one language and not the other. `Contents` is generated from `sections`, including the `###` platform levels.
- Rewrite prose as a side effect of a number refresh: `header`, `sections[].intro` and `notes` are inputs to a render, never outputs.

**Migration acceptance test.** Rendered `README.md` and `README.zh-CN.md` must equal the committed files
**byte for byte** (the refreshed-date line included: `refreshed` is a field in the json, so no exception is
needed), the link set must round-trip, and per-heading entry counts and ⚠ counts must hold. A mismatch is
fixed in the renderer or the json, never by editing a README to satisfy the test. **Run 2026-10-17 at the
migration baseline: both files identical**, with `check-i18n.py` reporting 138 links and 135 entries on both
sides and no GitHub URL repeated in either file. **Re-run the same evening after the first real merge**
(11 entries): identical again, 149 links and 146 entries. It runs locally today and enters
`.github/workflows/lint.yml` with `entries.json`; once in CI, no later render can silently rewrite prose.
