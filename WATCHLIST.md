# WATCHLIST.md — leads that are not yet entries

Operating procedure; `README.md` is the product. A lead lives here until a repository exists,
has been opened, and has had its numbers read from `GET /repos/{owner}/{repo}`. Until then it is
a lead, not data: nothing on this list may be quoted into a README, and a lead's own numbers are
dated facts about a past read, not a current measurement.

Admission is decided in `AGENTS.md` (`## Admission`, tests A1–A3); which section an admitted
project lands in is decided in `AGENTS.md` (`## Filing axis`). This file records, per lead, only
what has been verified, what has not, and what the filing decision would be. Re-review of what
is *already entered* is a different procedure and lives in `RECHECK.md`.

## Status

| Lead | Asked | State | Blocking test | Next action |
| --- | --- | --- | --- | --- |
| HackiOS | 2026-10-16 | no repository exists to open | nothing to read — A2 cannot be run | re-search when the owner says it is published |
| Switch titles → iOS on the `d2r-mobile` recipe | 2026-10-16 | none exist yet | A3, no artifact | check the named titles, file by the precedent below |
| 星之卡比 / Kirby | 2026-10-16 | partly entered (5 of 12 read) | A2 on the remainder | read `overjt/knidl`'s own README |
| 大富翁4 / Richman 4 | 2026-10-16 | partly entered (2 of 3) | size only, on `tytannial/rich4-re` | none pending; re-read at 30★ |
| 怪物猎人 / Monster Hunter | 2026-10-16 | partly entered (1 of 4) | A3 on three small ports | watch `GURecomp/SUYU-GURecomp` |
| 使命召唤 / Call of Duty | 2026-10-16 | entered (1), rest refused | A1/A3 on every remainder | re-read `vladtrc/iw4L` before changing its claim |
| GTA V, 荒野大镖客 / RDR2 | 2026-10-16 | closed negative — nothing admissible at any size | A1 or A3 on every candidate | none; San Andreas is where the family is real |
| 黄昏公主 / Twilight Princess | 2026-10-16 | closed — both real projects entered | single-link rule, forks | none |
| pret Gen-II remainder | 2026-10-16 | closed negative on the remainder | A1 (prototype) on `pokegold-spaceworld` | only if the prototype is re-framed |
| 血源诅咒 / Bloodborne | 2026-10-16 | closed — entered | single-link rule on the fork | none |
| Galaxy on Fire 2 | 2026-10-17 | **entered 2026-10-17** | cleared: A1–A3 all passed | see its block for the platform level it created |

`State` is about the lead, not the quality of the work. `Blocking test` always names an A-test
or a filing rule — never a star count, which is not an admission test in this repository.

## HackiOS

- **Asked** 2026-10-16 by the owner, who expects the project to be published later.
- **Verified** nothing. The description ("an effort to run iOS on non-Apple hardware") is my own
  recollection and is **not read from a primary source**, which is exactly why there is no entry.
- **Negative finding** on 2026-10-16: repository search for `HackiOS` (by name, and ordered by
  stars) returned only unrelated 0★ repositories; `topic:hackios` has `total_count = 0`; the four
  plausible slugs `LefticusMD/HackiOS`, `Lefticuss/HackiOS`, `almarazi/HackiOS` and
  `HackiOS/HackiOS` all return 404. Do not guess a URL for it.
- **If it appears**: the artifact is the platform, so it files under `Runtimes and compatibility
  layers`, platform written `iOS → PC hardware`, with a boot / firmware-interface method label —
  **not** under `Games`, whatever title it eventually boots.

## Switch titles ported to iOS on the `d2r-mobile` recipe

- **Asked** 2026-10-16; expected within days by the owner, naming Mario and Animal Crossing
  specifically. No such repository exists yet, so nothing here is verified.
- **Expected shape** if they follow `d2r-mobile`: the Switch aarch64 program runs directly, only
  the non-executable instructions are rewritten, and the reconstructed object is the platform
  surface (NVN, syscalls, VFS, audio, input).
- **Filing test, from the `## Filing axis` precedents in AGENTS.md**: ahead-of-time recompile plus
  a reimplemented surface is `Games / Nintendo` with a `→ iOS` destination, the way
  `jhaizhou-ops/d2r-mobile` is entered as Nintendo rather than Runtimes.
- **Not an entry at all**: runtime emulation, cloud streaming, or a repack of an official build
  labelled 移植 — that was the finding of the short-video wave, recorded under `## Census`.

## 星之卡比 / Kirby

- **Asked** 2026-10-16 («星之卡比，大富翁都留意一下»). Entered the same day from the measurements
  below: `Kirby64Ret/kirby64`, `jiangzhengwenjz/katam`, `doldecomp/kar` and `Swiftshine/key` in
  `Games / Nintendo`, and `ExpansionPak/ModernGekko` in `Runtimes and compatibility layers`.
  Numbers read 2026-10-16 from `GET /repos/{owner}/{repo}`.
- **Remaining leads, by platform.**
  - Nintendo 64 — the entered pair is `Kirby64Ret/kirby64` ★ 234 · 21 forks · Assembly · **no
    licence declared** · created 2020-05-20, pushed 2026-09-13 (its own README is the method
    claim: "work-in-progress decompilation", the build needs `baserom.us.z64` in the tree, and
    contributions are accepted "as long as it increases the decomp percentage" — M1 shape) and
    `Kirby64Ret/Kirby64Recomp` ★ 46 · 6 forks · GPL-3.0 · C++ · pushed 2026-09-18, the M4 line for
    the same title (`Nintendo 64 → Windows, Linux and macOS`). The recompile is entered as its own
    line because the artifact differs; it is not a fork of the decompilation.
  - Game Boy Advance — `overjt/knidl` ★ 17 · 5 forks · C · no licence · created 2026-08-20, pushed
    2026-10-05 has an **empty description**, so its title has to be read from the repository
    itself before it can be entered, not from a search result. `jiangzhengwenjz/katam` ★ 158 is
    entered ("WIP Decompilation of Kirby & The Amazing Mirror (USA)").
  - GameCube / Wii — entered: `doldecomp/kar` ★ 88 · 10 forks · Assembly · no licence · created
    2020-10-15, pushed **2025-02-26** (a real Kirby Air Ride decompilation quiet for twenty
    months, so its line carries that push date rather than reading as active), `Swiftshine/key`
    ★ 52 · 4 forks · CC0-1.0 · pushed 2026-10-14 (Kirby's Epic Yarn) and `Swiftshine/kdc` ★ 13 ·
    3 forks · CC0-1.0 · C · created 2025-10-29, pushed 2026-10-11 (Kirby's Dream Collection), and
    `ExpansionPak/ModernGekko` ★ 169 · 17 forks · GPL-3.0 · C++ · created 2026-06-25, pushed
    2026-09-17, which describes itself as a "**Runtime** for recompilations of GameCube games" —
    the `azahar` precedent applies: the artifact is the runtime, so it files under Runtimes even
    though the aggregator files it with the titles it runs.
  - Game Boy — `huderlem/kirbydreamland` ★ 54 · 7 forks · pushed 2020-06-16 and
    `Ankouno/KSS-disassembly` ★ 12 · 1 fork · created 2018-11-15, pushed 2023-10-07 are stalled
    disassemblies: candidates for a line that states the push date honestly, not for an active
    section. `omegakatana92/Kirby-Dream-Land-Recomp` ★ 11 · C · created 2026-08-25 and
    `omegakatana92/Kirby-Pinball-Land-Recomp` ★ 1 · created 2026-08-26 are fan recompiles that
    require the user's own ROM.
- **Refused, with the test** — `SeanMott/KAR-Decomp` ★ 4 (its own description is "yet another
  Kirby Air Ride decomp"; check it against `doldecomp/kar` before entering, A3 single-link),
  `LeftInWalmart/KirbyAR-Decomp-Public` ★ 0, `Etrainquandt17/Whippy` ★ 0, `sh1ftmaker/katam-port`
  ★ 0, and `andrewnakas/knidl-web` (its README 404s on 2026-10-16, so **A2** could not be read).
  Dump tools of the `mytbk/r2dumpbin` kind are refused at A3 as instrumentation.
- A 0★ repository here is a live lead, not a rejection; absence from this file is not evidence of
  non-existence.

## 大富翁4 / Richman 4 (Softstar, 1998, Windows)

- **Asked** 2026-10-16. The strongest Chinese-language reconstruction chain in the corpus;
  `mytbk/rich4` and `lhr0909/richman4-remastered` became entries the same day. Numbers read
  2026-10-16 from the API.
- **Entered, and how each is labelled.**
  - `mytbk/rich4` ★ 146 · 20 forks · GPL-3.0 · Assembly · created 2018-09-27, pushed 2026-10-08,
    description 「大富翁4逆向」. Its primary source is `readme.rst` — the file is `readme.rst`, not
    `README.md`, which 404s — and it states the target as `rich4.exe` v3.11, 588 KiB, SHA-256
    `5a90aee28ee5f7a5c3ba5cb935c9e55751a529c25fcd91208748a66293569550`; 2018 found the data-file
    unpacking algorithm and the save format, 2021-05 turned `rich4.exe` into modifiable,
    re-linkable assembly with `r2dumpbin`, and 2025 stripped the Watcom C runtime so the
    disassembly links against MinGW and `msvcrt` into a runnable `rich4.exe`. That is **disassembly
    that reassembles into the shipped program**, the same distinction the `pret/pokered` line
    carries as two words; it files `Games / MS-DOS, Windows and Macintosh`. The annotated split
    lives on Codeberg (`vimacs/rich4_asm`), which is not a GitHub link — name it as plain text,
    never as the entry URL.
  - `lhr0909/richman4-remastered` ★ 9 · 3 forks · GPL-3.0 · C++ · created **and** pushed 2026-10-06
    — a native C++20/SDL3 engine running the original rules, art, animation, music and voice on
    macOS / Android / iOS from the reader's own licensed copy, which it points at on Steam. Its own
    README says plainly that it is **not clean-room** in the `storytold/wordcraft` sense: every
    rule and timing was rewritten against `mytbk/rich4`'s published disassembly, stated in its
    acknowledgements. So the method label is a **behaviour reimplementation read from a
    disassembly**, and it is never labelled agent- or clean-room-output on the strength of being a
    new engine. Its licence constraint is worth one clause in the line: the repository excludes
    game files, and its NOTICE limits redistribution of a built APK to the builder's own devices.
- **Remaining lead** — `tytannial/rich4-re` ★ 2 · MIT · C++ · created 2026-09-29, pushed 2026-10-05,
  "Rich4 game community reconstruction edition", the third 大富翁4 effort, named in `mytbk/rich4`'s
  own readme under 相关工作. Too small to carry weight yet; re-read at 30★, which is a re-read
  trigger, not a threshold it must clear to be admissible.
- **Negative finding, recorded so nobody invents one** — searching `monopoly`,
  `monopoly-game-remake`, `monopoly-reimplementation`, `board-game-monopoly`, `richman`, `softstar`
  and 「大富翁 逆向」 on 2026-10-16 turned up **no reverse-engineering result for Hasbro's Monopoly**;
  every hit is an original clone or a student/board-game implementation (`Mitul-Joby/Monopoly`
  ★ 50 is a C terminal implementation, not a reconstruction of a shipped game). 大富翁 in this
  corpus means Softstar's Richman series; keep the two senses apart in any line written.

## 怪物猎人 / Monster Hunter (Capcom)

- **Asked** 2026-10-16 (「荒野大镖客，怪物猎人，使命召唤，GTA5，血源诅咒，PhotoCraft，黄昏公主，
  pokeyellow，pokegold。这几个都查一下」). Entered the same day: `TeamGDB/Yakumo`, `Games / Sony
  PlayStation`, ★ 448 · 33 forks · MIT · C++ · created 2026-09-18 · pushed 2026-10-13. Its README
  *is* the method claim, verbatim: 「A native port of **Monster Hunter Portable 3rd HD Ver.** made
  by static recompilation: the game's PSP code is translated ahead of time into C++ and compiled
  for your machine, then run on a reimplementation of the PSP system software. It is not an
  emulator — there is no interpreter or JIT at the heart of it — and it is not a decompilation.」
  No assets shipped; the installer accepts only the PS3 release `NPJB-40001`; Windows, Linux
  (Flatpak, Steam Deck Game Mode), macOS (Apple Silicon over MoltenVK) and Android builds; it
  builds on `jessicanataliagta/PSPRecomp`.
- **Still leads, all small** — `glinesbdev/mh3u-port` ★ 1 · Rust · AGPL-3.0 ("No emulator is
  involved at run time", boots into the village); `GURecomp/SUYU-GURecomp` ★ 4 · GPL-3.0 (adds an
  AArch32 static recompiler, targets MHGU 1.4.0); `Aoyagi01/Tutikumo` ★ 0 · MIT (MHP2ndG on the
  Yakumo base).
- **Refused at A3 as instrumentation or scaffolding** — `GURecomp/forge-pc` ★ 1 (mod loader),
  `jajdp/mhp3rd-xbox` ★ 0 (a run recipe), `vs-sr-dev/pc-monsterhunter3` ★ 0 (docs and tools only,
  the recompiler sits in a wiikit submodule), `SiD3W4y/mhfu-re` ★ 18 (Ghidra and Binary Ninja
  plugins plus notes), `Houmgaor/MHBridge` ★ 0 (protocol / private-server shim),
  `REClone-ART/REClone` ★ 1 (two files, a README-only proposal about the RE Engine).
- **Negative finding** — `monster hunter decompil`, `monster hunter recomp`, `monster hunter native
  port` and `MH4U decomp`, each with `stars:>100`, all return **0 results**: no reconstruction of
  an RE-Engine-era Hunter exists at admissible size.

## 使命召唤 / Call of Duty

- **Asked** 2026-10-16. `vladtrc/iw4L` ★ 1,062 is entered from the ≥1,000★ batch. Its README now
  says the asset readers "also cover MW3 and Black Ops", so its scope has grown past Modern
  Warfare 2 — **re-read the repository before changing what our line claims**.
- **Distribution facts kept here, not in the README** — its release archive is password-gated
  through a Telegram channel, and dedicated-server support needs an operator-issued
  `.iw4l-server` file.
- **Refused** — `callofduty4x/CoD4x_Server` ★ 435 (self-described "a modification of the Call of
  Duty 4 … server"), `CoD4x_Client_pub` ★ 97 (injected DLL), `iw4x/iw4x-client` ★ 340 and
  `iw4x-rawfiles` ★ 79 (custom multiplayer client), `GalvarinoDev/DeckOps` ★ 73 (installer),
  `RaidMax/IW4M-Admin` ★ 255 (admin panel): modification, injection or installation on somebody
  else's binary, so A1 or A3.
- **Negative finding** — `PlutoniumT7Code` and `XLiveRevo` return repository search
  `total_count = 0`: that source is not public. No Call of Duty decompilation exists at admissible
  scope.

## GTA V and 荒野大镖客 / Red Dead Redemption 2

- **Asked** 2026-10-16. **No admissible reconstruction at any size.** The GTA V corpus is tooling,
  mods and content dumps: `njames93/GTA-V-Script-Decompiler` ★ 118 (a Script Hook tool),
  `calamity-inc/GTA-V-Decompiled-Scripts` ★ 82 and `YimMenu/GTA-V-Decompiled-Scripts` ★ 46
  (extracted script bodies), `ThirteenAG/GTAIV.EFLC.FusionFix` ★ 3,405 (fix pack), `DeepGTAV`
  ★ 1,194 and `gta5-real-mod` ★ 1,185 (mods), `gta-v-data-dumps` ★ 1,047, `GTAVE-ModLoader` ★ 1,
  `tostercx/GTAO_Booster_PoC` ★ 2,866 (archived; a multiplayer exploit and patcher).
- **Never linked, never mirrored** — `creativewild/rdr2-scripts-decompiled` ★ 13 is a 128,989 KB
  repository of **extracted RDR2 game content**, so under 「No game files, ROMs, cracked binaries,
  or keys anywhere in this repo」 its name is written as code and it gets no URL. This is the one
  case where that rule bites, and it is a rule about *our* tree: it says nothing about what a
  linked repository holds (see `## Admission` in AGENTS.md).
- **Queries with counts recorded** — `rage engine reimplementation` 0, `rdr2 decompil` 5,
  `gta5 decompil` 8, `gta v reverse engineering` 3, `gta engine reimplementation` 5 (hits are San
  Andreas and IV only).
- **Where the family is real** — San Andreas: `gta-reversed/gta-reversed` and
  `in0finite/SanAndreasUnity` are entries; re3/reVC is recorded in AGENTS.md
  `## Takedown and legal record`.

## 黄昏公主 / Twilight Princess near-misses

- **Asked** 2026-10-16; nothing to add. `zeldaret/tp` ★ 2,091 and `TwilitRealm/dusklight` ★ 5,874
  are entries.
- **Refused by the single-link rule** — `HayatoG/dusklight` ★ 65 is a private fork of dusklight
  carrying a Switch platform port, but its README and its download links are upstream's, so it
  stays a lead rather than a second entry. `zsrtp/Randomizer` ★ 63 is a randomizer, which is a mod.
- **Two fabrications, kept as negative findings** — `SkyisHere15/Zelda-Twilight-Unity-Rebuild`
  ★ 56 and `mh9364944-tech/TPHD-Cemu-Save-Editor` ★ 53 each have **0 forks, 0 watchers** and a tree
  of README plus `index.html` only, with badges claiming C#, Python and Lua files that are not in
  the repository. Reading the file list is what changed those verdicts; a ★ count alone did not.

## pret Gen-II remainder

- `pret/pokeyellow` ★ 891 · 348 forks and `pret/pokegold` ★ 727 · 205 forks entered 2026-10-16,
  both Assembly, both **no licence declared**, every target ROM pinned by SHA-1. `pokegold` is a
  disassembly of *two* shipped releases (Gold **and** Silver) and its line names both.
- **Not entered** — `pret/pokegold-spaceworld` ★ 402 · 75 forks is the 1997 Space World
  **prototype demo**, weaker on the shipped-artifact half of A1; if it enters, the line must say it
  is a prototype. `Narishma-gb/pokeyellow-jp` ★ 9 is a Japanese-version branch built on
  pokeyellow (A3, single-link). ROM hacks stay excluded: `dannye/pokeyellow-gen-2-gfx` ★ 39,
  `Cram-o-dev/cramorantedition` ★ 21 (A1, nothing shipped was taken apart).

## 血源诅咒 / Bloodborne

- **Asked** 2026-10-16; already covered. `deadinside28/bloodborne_pc` ★ 3,006 is the entry and
  `Supermedo/bloodborne_pc` ★ 3,086 · GPL-2.0 · 2 watchers stays prose as the Windows distribution
  of the same port. No second link.

## Galaxy on Fire 2 — `JoppieToppie/Galaxy-on-Fire-2-Unity-Remake`

- **Asked** 2026-10-17 by the owner (「记录：JoppieToppie/Galaxy-on-Fire-2-Unity-Remake») and
  **entered the same day**, at `Games / Mobile`. Numbers read from `GET /repos/{owner}/{repo}`
  on 2026-10-17: ★ 145 · 16 forks · 2 watchers · C · 28,770 KB · 10 open issues · created
  2026-09-29 · pushed 2026-10-17 · license object `NOASSERTION` while `LICENSE.md` is the
  Apache-2.0 text in full — which is why its line names both, so the monthly `lic` trigger has
  nothing left to ask. It is not in the aggregator's 2,118 rows, so enumeration would not have
  found it.
- **What it is** — a Unity remake of FISHLABS' 2010 space game for Windows (also UWP), Linux and
  Android; its own status line says the main campaign and the Valkyrie and Supernova add-ons "can
  be played from start to end", with experimental multiplayer and OpenXR VR. `CLAUDE.md` is its
  per-system technical doc and names the original function each system is based on.
- **Method claim, from the repository rather than inference** — 「built on the original assets and
  on game logic ported from the decompiled game code」. `Reference/decompiled/native/` holds Ghidra
  output for 4,028 functions of the ARM build, one file per C++ class, with `_FUNCTIONS.tsv`
  (name, address, size), `INDEX.md`, `CLASS_HIERARCHY.txt`, and one function documented as "too
  large to decompile" whose result was obtained by emulation
  (`BuildResourceList_EMULATED_OUTPUT.json` → `Assets/Resources/GoF2Data/resources.json`). So the
  label is **a port of a decompilation, read from a decompiled original** — the
  `lhr0909/richman4-remastered` shape, and **never** written as clean-room.
- **What its tree holds, recorded because it is a fact about the project, not a test it failed** —
  `Reference/binaries/` carries `libgof2hdaa.so` (the original 32-bit ARM game library),
  `libfmodevent.so` and `GOF2_2.0.16_Android_Price.apk`, which the project's own table describes as
  「the modded APK the code came from」; `.gitattributes` puts `*.so`, `*.apk`, `*.png`, `*.ogg`,
  `*.bytes` in Git LFS and the README states the assets are 「about 2.1 GB in LFS」 with the 1.5 GB
  OBB on the release page. The credits name the source build: 「built on the **FULL HD version and
  modifications made by KiritoJPK** … thanks to the Galaxy on Fire 2™ and 4PDA community」, linking
  `KiritoJPK/Galaxy-on-Fire-2-FULL-HD-Android`. On 2026-10-17 the owner declined to turn this into
  a rule (**「不加这条规则，我们没有能力判断仓库里放的是不是厂商的程序」**), so it admits at A1–A3
  and this paragraph is the whole of our record.
- **What the gate saw** — `scripts/quality.py` calls it `conditional`: **only E3 fires**
  (`.github`, its CI). E1, E2 and E4 are absent, and E4 is absent because there is no assets
  boundary to find — it ships the assets. The gate is not wrong, it is silent: nothing in the
  E1–E4 vocabulary means "this tree holds the vendor's binaries", and nothing is supposed to
  decide that. The root listing is still read at intake, because where a project says its logic
  came from a decompilation, the root listing is how you check the decompilation is in the tree.
- **Filing consequence — it created a platform level.** The original ran on Android and iOS (the
  FULL HD build also on Windows and macOS), so `Games` gained `### Mobile` in both READMEs and in
  both `## Contents`, following the `### Microsoft Xbox and Xbox 360` precedent: a level is
  created when an entered title demands it, never as a placeholder, and `check-i18n.py` compares
  headings positionally, so a one-sided level fails the gate. Destination written both ends
  (`Android and iOS → Windows, Linux and Android`), every number re-read at write time.

## Two search notes that apply to every lead above

- Expect these to be under-counted by the existing enumeration vocabulary: such projects
  self-describe as "port", "native run" or "compatibility layer", which is precisely the vocabulary
  the rate-killed `linux-port` / `asset-extract` tokens failed to cover (see `## Census`).
- These families are the highest-DMCA-risk material in the corpus: Nintendo's 2026-08 notices are
  framed as TPM circumvention under DMCA §1201, not only copyright, which is what makes a whole
  fork network removable at once. Record the notice text if a takedown lands, and do not cite a
  fork as current after one.
