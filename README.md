# Awesome REA [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

Finished reverse-engineering results: reimplemented engines, byte-matching decompilations, reimplemented formats, protocols, drivers and APIs, platform ports, compatibility patches.

**English** | [简体中文](README.zh-CN.md)

This list catalogues **outcomes**, not instrumentation: the programs, formats and protocols people have actually taken apart and rebuilt. Entries are filed by the **kind of software** that was reconstructed, and inside `Games` by the **platform it originally ran on**. Each line states that platform — both ends for a port — and the method it was rebuilt by. Debuggers, decompilers, hex editors, trainers and similar tooling are out of scope; the tool lists are named under Related lists.

Named for [`rea`](https://github.com/morluto/rea), an agent-driven reverse-engineering toolkit. Entries are the reconstructions themselves, whatever toolchain or person produced them.

★ counts and last-push dates are read from GitHub's `GET /repos/{owner}/{repo}` endpoint and are rewritten by a scheduled CI job. **Data last refreshed 2026-10-17.** **⚠** marks a claim not read from a primary source, so it is not data. The maintenance rules for this list are in [AGENTS.md](AGENTS.md).

## Contents

- [Games](#games)
  - [Nintendo](#nintendo)
  - [Sony PlayStation](#sony-playstation)
  - [Microsoft Xbox and Xbox 360](#microsoft-xbox-and-xbox-360)
  - [MS-DOS, Windows and Macintosh](#ms-dos-windows-and-macintosh)
  - [Home computers](#home-computers)
  - [Mobile](#mobile)
- [Applications](#applications)
- [Runtimes and compatibility layers](#runtimes-and-compatibility-layers)
- [Formats, file systems and protocols](#formats-file-systems-and-protocols)
- [Related lists](#related-lists)

## Games

Engines, decompiled binaries and recompiles of shipped games. Almost all of these leave the game files to the reader's own licensed copy; an entry that carries the original assets says so in its line.

### Nintendo

- [n64decomp/sm64](https://github.com/n64decomp/sm64) - Super Mario 64, Nintendo 64, decompilation to C that rebuilds a ROM matching the shipped one, CC0-1.0. ★ 8,890 · 1,652 forks · pushed 2024-02-04.
- [Zelda64Recomp/Zelda64Recomp](https://github.com/Zelda64Recomp/Zelda64Recomp) - The Legend of Zelda: Majora's Mask, Nintendo 64 → Windows, Linux and macOS, static recompilation of the cartridge binary, "This is not an emulator", GPL-3.0. ★ 7,447 · 344 forks · pushed 2026-09-25.
- [TwilitRealm/dusklight](https://github.com/TwilitRealm/dusklight) - The Legend of Zelda: Twilight Princess, GameCube → Windows, Linux, macOS, Android and iOS, "a reverse-engineered reimplementation" built on the `zeldaret/tp` decompilation, CC0-1.0. ★ 5,891 · 442 forks · pushed 2026-10-11.
- [HarbourMasters/Shipwright](https://github.com/HarbourMasters/Shipwright) - Zelda: Ocarina of Time, Nintendo 64 → Windows, Linux and macOS, source port of the `zeldaret/oot` decompilation onto libultraship, **no license declared**. ★ 5,645 · 919 forks · pushed 2026-10-15.
- [zeldaret/oot](https://github.com/zeldaret/oot) - Zelda: Ocarina of Time, Nintendo 64, byte-matching decompilation. ★ 5,595. The reference project for symbol-matching workflows.
- [pret/pokered](https://github.com/pret/pokered) - Pokémon Red and Blue, Game Boy, disassembly that reassembles to the original ROM. ★ 4,996.
- [snesrev/zelda3](https://github.com/snesrev/zelda3) - The Legend of Zelda: A Link to the Past, Super Nintendo → Windows, Linux and macOS, "a reverse engineered clone" in C that runs the original machine code side by side and compares RAM after each frame, MIT. ★ 4,866 · 453 forks · pushed 2026-10-02.
- [bryanthaboi/gen1recomp](https://github.com/bryanthaboi/gen1recomp) - Pokémon Red through Emerald, Game Boy and Game Boy Advance → Windows, Linux, macOS, iOS, Switch and consoles, engine and map behaviour hand-written in Lua from the pret disassemblies rather than clean-room, GPL-3.0 with additional terms. ★ 3,946 · 356 forks · pushed 2026-10-15.
- [pret/pokeemerald](https://github.com/pret/pokeemerald) - Pokémon Emerald, Game Boy Advance, decompilation that builds the SHA-1-matching ROM, **no license declared**. ★ 3,602 · 4,826 forks · pushed 2026-10-01.
- [jhaizhou-ops/d2r-mobile](https://github.com/jhaizhou-ops/d2r-mobile) - Diablo II: Resurrected, Nintendo Switch → iOS, iPad and Mac, static recompile over a reimplemented NVN, syscall, VFS, audio and input surface. ★ 3,592 · 1,034 forks · MIT · created 2026-10-12.
- [pret/pokecrystal](https://github.com/pret/pokecrystal) - Pokémon Crystal, Game Boy, disassembly. ★ 2,528.
- [HarbourMasters/SpaghettiKart](https://github.com/HarbourMasters/SpaghettiKart) - Mario Kart 64, Nintendo 64 → Windows, Linux, macOS and Nintendo Switch, source port on libultraship that requires the player's own ROM, **no license declared**. ★ 2,418 · 153 forks · pushed 2026-10-11.
- [doldecomp/melee](https://github.com/doldecomp/melee) - Super Smash Bros. Melee, GameCube, matching decompilation of the USA 1.02 `main.dol`, **no license declared**. ★ 2,416 · 357 forks · pushed 2026-10-16.
- [2ship2harkinian/2ship2harkinian](https://github.com/2ship2harkinian/2ship2harkinian) - Majora's Mask, Nintendo 64 → Windows, Linux and macOS, source port on the same libultraship stack as `HarbourMasters/Shipwright`, CC0-1.0. ★ 2,332 · 274 forks · pushed 2026-10-14.
- [zeldaret/botw](https://github.com/zeldaret/botw) - The Legend of Zelda: Breath of the Wild, Switch 1.5.0, "experimental, WIP decompilation", and its README states it **cannot** be used to play the game, **no license declared**. ★ 2,249 · 142 forks · pushed 2026-10-15.
- [HarbourMasters/Starship](https://github.com/HarbourMasters/Starship) - Star Fox 64, Nintendo 64 → Windows, Linux, macOS and Nintendo Switch, source port of the SF64 decompilation, CC0-1.0. ★ 2,099 · 144 forks · pushed 2026-09-15.
- [zeldaret/tp](https://github.com/zeldaret/tp) - The Legend of Zelda: Twilight Princess, GameCube, decompilation whose GameCube code "is completely matching", CC0-1.0. ★ 2,090 · 206 forks · pushed 2026-06-23.
- [perfect-dark-pc-port/perfect_dark](https://github.com/perfect-dark-pc-port/perfect_dark) - Perfect Dark, Nintendo 64 → Windows, Linux, macOS and Nintendo Switch, work-in-progress port of the decompilation whose original has moved to GitLab, MIT. ★ 2,057 · 156 forks · pushed 2026-08-13.
- [BanjoRecomp/BanjoRecomp](https://github.com/BanjoRecomp/BanjoRecomp) - Banjo-Kazooie, Nintendo 64 → Windows, Linux and macOS, static recompilation, "not based on the source code provided by a decompilation", GPL-3.0. ★ 2,047 · 74 forks · pushed 2026-09-25.
- [sm64pc/sm64ex](https://github.com/sm64pc/sm64ex) - Super Mario 64, Nintendo 64 → Windows, Linux and macOS, source port of the `n64decomp/sm64` decompilation with enhancement and camera mods, **no license declared**. ★ 1,865 · 574 forks · pushed 2024-12-17.
- [zeldaret/mm](https://github.com/zeldaret/mm) - Majora's Mask, Nintendo 64, byte-matching decompilation on the same toolchain as `oot`. ★ 1,744.
- [pret/pokefirered](https://github.com/pret/pokefirered) - Pokémon FireRed and LeafGreen, Game Boy Advance, decompilation that builds six named ROM images including Switch revisions, **no license declared**. ★ 1,665 · 1,041 forks · pushed 2026-09-26.
- [pmret/papermario](https://github.com/pmret/papermario) - Paper Mario, Nintendo 64, work-in-progress decompilation with per-region SHA-1 progress, **no license declared**. ★ 1,633 · 170 forks · pushed 2026-09-26.
- [flyngmt/ACGC-PC-Port](https://github.com/flyngmt/ACGC-PC-Port) - Animal Crossing, GameCube → Windows, "a native PC port … built on top of the ac-decomp decompilation project", custom licence. ★ 1,494 · 126 forks · pushed 2026-08-02. Its README records that AI tools were used on the PC-port code only.
- [ACreTeam/ac-decomp](https://github.com/ACreTeam/ac-decomp) - Animal Crossing, GameCube, decompilation of the USA GAFE01 disc to C, CC0-1.0. ★ 1,414 · 94 forks · pushed 2026-07-18.
- [n64decomp/mk64](https://github.com/n64decomp/mk64) - Mario Kart 64, Nintendo 64, decompilation with non-matching assemblies still listed in `asm/non_matchings`, **no license declared**. ★ 1,311 · 138 forks · pushed 2026-08-16.
- [SMGCommunity/Petari](https://github.com/SMGCommunity/Petari) - Super Mario Galaxy, Wii, work-in-progress decompilation of `main.dol`, and its README states the project is "not meant to be an effort to create a PC port", CC0-1.0. ★ 1,250 · 116 forks · pushed 2026-10-14.
- [patchzyy/Wiicompiled](https://github.com/patchzyy/Wiicompiled) - Mario Kart Wii, Wii → Windows, Linux and macOS, static recompilation of a PAL `RMCP01` disc image, "There's no emulator in the loop", GPL-3.0. ★ 1,173 · 111 forks · pushed 2026-10-16.
- [zeldaret/tww](https://github.com/zeldaret/tww) - The Wind Waker, GameCube, byte-matching decompilation, CC0-1.0. ★ 1,099 · pushed 2026-10-14.
- [pret/pokeruby](https://github.com/pret/pokeruby) - Pokémon Ruby and Sapphire, Game Boy Advance, self-described disassembly that builds the matching ROMs, **no license declared**. ★ 1,003 · 273 forks · pushed 2026-09-29.
- [pret/pokeyellow](https://github.com/pret/pokeyellow) - Pokémon Yellow, Game Boy, disassembly that reassembles to the SHA-1-checked original ROM, **no license declared**. ★ 892 · 348 forks · created 2015-05-10 · pushed 2026-10-16.
- [pret/pokegold](https://github.com/pret/pokegold) - Pokémon Gold and Silver, Game Boy Color, disassembly of both releases, each pinned by its own SHA-1, **no license declared**. ★ 727 · 205 forks · created 2015-07-09 · pushed 2026-10-06.
- [Kirby64Ret/kirby64](https://github.com/Kirby64Ret/kirby64) - Kirby 64: The Crystal Shards, Nintendo 64, work-in-progress byte-matching decompilation, **no license declared**. ★ 234 · 21 forks · pushed 2026-09-13.
- [tangosdev/sm64ds-decomp](https://github.com/tangosdev/sm64ds-decomp) - Super Mario 64 DS, Nintendo DS, decompilation produced with an agent workflow. ★ 202 · created 2026-06-14.
- [jiangzhengwenjz/katam](https://github.com/jiangzhengwenjz/katam) - Kirby & The Amazing Mirror, Game Boy Advance, work-in-progress decompilation, **no license declared**. ★ 158 · 21 forks · created 2020-01-11 · pushed 2026-09-17.
- [doldecomp/kar](https://github.com/doldecomp/kar) - Kirby Air Ride, GameCube, decompilation, **no license declared**. ★ 88 · 10 forks · pushed 2025-02-26.
- [Swiftshine/key](https://github.com/Swiftshine/key) - Kirby's Epic Yarn, Wii, byte-matching decompilation of the USA release, CC0-1.0. ★ 52 · 4 forks · pushed 2026-10-14.
- [Petexy/Tekken-Tag-2-Recompiled](https://github.com/Petexy/Tekken-Tag-2-Recompiled) - Tekken Tag Tournament 2, Wii U → Linux, static recompilation, MIT, no game files. ★ 9 · 1 fork · created 2026-10-05.

`d2r-mobile` is neither emulation nor recompilation of assets: the game's own aarch64 program runs directly, and only the instructions that cannot execute under Apple's kernel are rewritten. Its target is the Switch build of Diablo II: Resurrected, 1.0.34.0, which equals the PC 3.3.94012 build. What was reverse engineered is the platform surface the game expects — syscalls, VFS, NVN reimplemented on Metal with shaders translated offline, audio, input. The repository ships no game content and lists its own RE output in `docs/DERIVED.md` (shader interface descriptions, graphics API function table, addresses inside the program); the user supplies their own dump via `nxdumptool`.

The four Kirby entries above cover four Nintendo platforms and ship no ROM: `Kirby64Ret/kirby64` builds against a `baserom.us.z64` the reader supplies and tracks its decomp percentage, `jiangzhengwenjz/katam` targets the Game Boy Advance USA cartridge, `doldecomp/kar` the GameCube disc from the group behind the Super Smash Bros. Melee decompilation, `Swiftshine/key` the Wii USA release `RK5E01`. `Kirby64Ret/Kirby64Recomp` compiles the N64 image into a Windows, Linux and macOS program, and `ExpansionPak/ModernGekko` is the GameCube and Wii runtime such recomps load into.

The Super Mario 64 line is one reconstruction with several destinations: `n64decomp/sm64` builds the matching ROM from a `baserom.<VERSION>.z64`, `sm64-port/sm64-port` is the GitHub fork that adds native Linux and Windows targets, `sm64pc/sm64ex` forks that with enhancement packs and Emill's fast 3D renderer, and `coop-deluxe/sm64coopdx` continues the archived `djoslin0/sm64ex-coop` multiplayer mod on top of it. `HarbourMasters/Shipwright`, `2ship2harkinian/2ship2harkinian`, `HarbourMasters/SpaghettiKart` and `HarbourMasters/Starship` are one libultraship family — four titles, four ROM dumps, no shipped assets. Two of the decompilations state the boundary themselves: `zeldaret/tp` "is not, and will not, produce a port", which is the gap `TwilitRealm/dusklight` fills, and `SMGCommunity/Petari` refuses the port label outright; the Perfect Dark decompilation now lives on GitLab, with `n64decomp/perfect_dark` kept as a mirror.

### Sony PlayStation

- [open-goal/jak-project](https://github.com/open-goal/jak-project) - Jak & Daxter, PlayStation 2 → Windows, Linux and macOS, decompilation of the game code back into GOAL plus a compiler that rebuilds it for x86-64: "It shouldn't be emulated, interpreted, or transpiled", ISC. ★ 3,576 · 253 forks · pushed 2026-10-16.
- [deadinside28/bloodborne_pc](https://github.com/deadinside28/bloodborne_pc) - Bloodborne, PS4 → Linux, the game's own x86-64 code running against "a runtime written for this one game \[that\] replaces the PS4 system libraries", with graphics translated to Vulkan, GPL-2.0. ★ 3,060 · 733 forks · pushed 2026-10-15.
- [phoboslab/wipeout-rewrite](https://github.com/phoboslab/wipeout-rewrite) - wipEout, PlayStation → Windows, Linux, macOS and the browser, "a re-implementation of the 1995 PSX game", **no license declared**. ★ 2,977 · 264 forks · pushed 2026-09-27.
- [FelipePrado0/gow3_pc](https://github.com/FelipePrado0/gow3_pc) - God of War III Remastered, PS4 → Windows and Linux, static recompilation of the original console binary, GPL-2.0, C++. ★ 2,962 · 190 forks · created 2026-10-08.
- [LoreanXavier/pt-pc](https://github.com/LoreanXavier/pt-pc) - P.T., PS4 → Windows, Linux and macOS, "the game logic was rebuilt in C++ from the original's behaviour" in a new engine that reads the original archives, MIT. ★ 1,873 · 124 forks · pushed 2026-10-16.
- [OpenDriver2/REDRIVER2](https://github.com/OpenDriver2/REDRIVER2) - Driver 2, PlayStation → Windows, Linux and the browser, "completely disassembled and translated from MIPS back to C… no emulation involved", MIT. ★ 1,405 · 91 forks · pushed 2026-09-22.
- [Xeeynamo/sotn-decomp](https://github.com/Xeeynamo/sotn-decomp) - Castlevania: Symphony of the Night, PlayStation, PSP and Saturn, "the code compiles byte-for-byte to the same binaries of the game", AGPL-3.0. ★ 1,149 · 111 forks · pushed 2026-10-17.
- [TeamGDB/Yakumo](https://github.com/TeamGDB/Yakumo) - Monster Hunter Portable 3rd HD Ver., PSP → Windows, Linux, macOS and Android, static recompilation of the PSP machine code into C++ on a reimplemented PSP system surface, "It is not an emulator — there is no interpreter or JIT at the heart of it — and it is not a decompilation", MIT, no game assets; the installer accepts only the original PS3 release `NPJB-40001`. ★ 459 · 33 forks · created 2026-09-18 · pushed 2026-10-13.
- [crowded-street/3s-decomp](https://github.com/crowded-street/3s-decomp) - Street Fighter III: 3rd Strike, PlayStation 2, byte-matching decompilation, AGPL-3.0. ★ 280 · 24 forks · created 2024-09-28 · last push 2026-04-03.
- [fabioap-cpu/Tekken3Recomp](https://github.com/fabioap-cpu/Tekken3Recomp) - Tekken 3, PlayStation 1 → PC, static recompilation, **no license declared**. ★ 139 · 3 forks · created 2026-07-31.
- [zFitness/gow3_android](https://github.com/zFitness/gow3_android) - God of War III Remastered, PS4 → Android, "Native Android port of God of War III Remastered (PS4)", GPL-2.0. ★ 145 · 12 forks · created 2026-10-14.
- [KIexster/god-of-war-recomp](https://github.com/KIexster/god-of-war-recomp) - God of War, PS2 → Windows PC, static recompilation, GPL-3.0. ★ 99 · 4 forks · created 2026-10-05.
- [gasparegas/tkdr-recomp](https://github.com/gasparegas/tkdr-recomp) - Tekken: Dark Resurrection, PSP → native and WebAssembly, static recompilation. ★ 5 · created 2026-10-11.

Four different reconstructions sit behind the PlayStation entries. `Xeeynamo/sotn-decomp` compiles back to the same bytes as the shipped binaries. `OpenDriver2/REDRIVER2` translates the MIPS code to C and runs it natively without emulation. `FelipePrado0/gow3_pc` and `deadinside28/bloodborne_pc` keep the original console code running and reimplement the system layer under it. `LoreanXavier/pt-pc` is the exception in that set: P.T.'s logic was rewritten from observed behaviour in a new engine that reads the original archives, so no original binary executes. `TeamGDB/Yakumo` is again a different shape: the PSP machine code is translated ahead of time into C++ and compiled for the host, so neither an interpreter nor the original binary runs, while the PSP system software underneath it is reimplemented. The Windows distribution of the Bloodborne port is carried by the fork `Supermedo/bloodborne_pc`, whose contributor list includes the upstream author.

### Microsoft Xbox and Xbox 360

- [hedge-dev/UnleashedRecomp](https://github.com/hedge-dev/UnleashedRecomp) - Sonic Unleashed, Xbox 360 → Windows and Linux, "created through the process of static recompilation" of the disc build, GPL-3.0. ★ 5,201 · 429 forks · pushed 2026-06-29.
- [mchughalex/skate3recomp](https://github.com/mchughalex/skate3recomp) - Skate 3, Xbox 360 → Windows, Linux and macOS, native recompilation with its own Direct3D 12 and Vulkan renderer and no GPU emulation, **no license declared**. ★ 1,641 · 72 forks · pushed 2026-07-24.
- [OpenCommunityEdition/OpenCE](https://github.com/OpenCommunityEdition/OpenCE) - Halo: Combat Evolved, Xbox build 2342 → Windows, Linux, Android and the browser, decompilation of the Xbox binary, "You do not need the Xbox SDK", CC0-1.0. ★ 1,610 · 226 forks · pushed 2026-10-17.

### MS-DOS, Windows and Macintosh

- [OpenRA/OpenRA](https://github.com/OpenRA/OpenRA) - Westwood's Command & Conquer, Red Alert and Tiberian Sun engines, MS-DOS and Windows, clean-room. ★ 17,578.
- [OpenRCT2/OpenRCT2](https://github.com/OpenRCT2/OpenRCT2) - RollerCoaster Tycoon 2, Windows → Windows, macOS, Linux, BSD and Android, "an open-source re-implementation" that uses the original game data, GPL-3.0. ★ 16,447 · 1,948 forks · pushed 2026-10-17.
- [SFTtech/openage](https://github.com/SFTtech/openage) - Age of Empires II engine, MS-DOS and Windows, clean-room. ★ 14,510.
- [yairm210/Unciv](https://github.com/yairm210/Unciv) - Sid Meier's Civilization V, Windows → Android, Windows, macOS and Linux, an open-source "moddability-focused" remake in Kotlin on LibGDX that authors its own art and audio. ★ 11,452 · 1,977 forks · pushed 2026-10-16.
- [diasurgical/DevilutionX](https://github.com/diasurgical/DevilutionX) - Diablo and Hellfire, Windows → Linux, macOS, Android, iOS, Nintendo Switch, PlayStation, Xbox and Amiga, port of the `diasurgical/devilution` reconstruction with its own engine work, Sustainable Use License. ★ 9,875 · 1,071 forks · pushed 2026-10-15.
- [diasurgical/devilution](https://github.com/diasurgical/devilution) - Diablo, Windows, "a reconstructed form of Diablo's original source code", recovered from the Climax PlayStation symbol file and the debug build hidden inside `DIABDAT.MPQ`, Sustainable Use License. ★ 9,004 · 923 forks · pushed 2025-09-15.
- [OpenTTD/OpenTTD](https://github.com/OpenTTD/OpenTTD) - Transport Tycoon Deluxe engine, MS-DOS and Windows, clean-room. ★ 8,377.
- [OpenMW/openmw](https://github.com/OpenMW/openmw) - Morrowind engine, Windows, clean-room. ★ 6,641.
- [vcmi/vcmi](https://github.com/vcmi/vcmi) - Heroes of Might and Magic III engine, Windows → Windows, macOS, Linux, Android and iOS, recreation that requires the original data files, GPL-2.0. ★ 5,952 · 741 forks · pushed 2026-10-17.
- [OpenSC2K/OpenSC2K](https://github.com/OpenSC2K/OpenSC2K) - SimCity 2000, MS-DOS, Windows 3.x and Macintosh → Windows, Linux and macOS, "an independently written re-implementation" that names reverse engineering of the original executable among its methods, MIT. ★ 5,303 · 122 forks · pushed 2026-10-16. Its README declares LLM-assisted coding.
- [XProger/OpenLara](https://github.com/XProger/OpenLara) - Tomb Raider 1 engine, MS-DOS, BSD-2. ★ 5,124.
- [k4zmu2a/SpaceCadetPinball](https://github.com/k4zmu2a/SpaceCadetPinball) - 3D Pinball for Windows – Space Cadet, Windows → Windows, Linux and macOS, every subroutine decompiled and converted to compilable C++, MIT. ★ 4,707 · 338 forks · pushed 2024-08-21.
- [CorsixTH/CorsixTH](https://github.com/CorsixTH/CorsixTH) - Theme Hospital, MS-DOS and Windows → Windows, macOS, Linux and BSD, reimplementation with most game logic in Lua on the original data, MIT-style licence. ★ 4,595 · 437 forks · pushed 2026-10-13.
- [Interkarma/daggerfall-unity](https://github.com/Interkarma/daggerfall-unity) - The Elder Scrolls II: Daggerfall, MS-DOS → Windows, Linux and macOS, recreation in Unity that reads the original archives, MIT. ★ 3,528 · 424 forks · pushed 2026-09-14.
- [ihhub/fheroes2](https://github.com/ihhub/fheroes2) - Heroes of Might and Magic II engine, MS-DOS and Windows → Windows, macOS and Linux, recreation "written from scratch" on the original resources, GPL-2.0. ★ 3,508 · 506 forks · pushed 2026-10-16.
- [isledecomp/isle](https://github.com/isledecomp/isle) - LEGO Island, Windows, decompilation whose cold rebuild with the original MSVC 4.2 "reproduces all three retail binaries byte for byte", LGPL-3.0. ★ 3,491 · 147 forks · pushed 2026-09-18. It builds only for 32-bit Windows.
- [bvschaik/julius](https://github.com/bvschaik/julius) - Caesar III, Windows → Windows, Linux, macOS, PS Vita, Nintendo Switch, Android and the browser, reimplementation with "the same logic as the original", save-compatible in both directions, AGPL-3.0. ★ 3,398 · 453 forks · pushed 2026-09-12.
- [alexbatalov/fallout1-ce](https://github.com/alexbatalov/fallout1-ce) - Fallout, Windows → Windows, Linux, macOS, Android and iOS, "fully working re-implementation of Fallout, with the same original gameplay", built on the author's own reverse-engineered `alexbatalov/fallout1-re`, Sustainable Use License. ★ 2,947 · 239 forks · pushed 2025-01-15.
- [scummvm/scummvm](https://github.com/scummvm/scummvm) - SCUMM and roughly 250 further adventure-game engines, MS-DOS, Windows and Macintosh, GPL-3.0. ★ 2,856.
- [FWGS/xash3d-fwgs](https://github.com/FWGS/xash3d-fwgs) - Half-Life's GoldSrc engine, Windows → Linux, Android and handhelds, engine reimplementation that runs the reader's own installation, **no license declared**. ★ 2,852 · 521 forks · pushed 2026-10-16.
- [in0finite/SanAndreasUnity](https://github.com/in0finite/SanAndreasUnity) - Grand Theft Auto: San Andreas, Windows → Windows, Linux, macOS and Android, "an open source reimplementation of GTA San Andreas game engine in Unity" reading the original data, MIT. ★ 2,648 · 467 forks · last push 2023-06-16.
- [alexbatalov/fallout2-ce](https://github.com/alexbatalov/fallout2-ce) - Fallout 2, Windows → Windows, Linux, macOS, Android and iOS, the same model as `alexbatalov/fallout1-ce` on the author's reverse-engineered `alexbatalov/fallout2-re`, Sustainable Use License. ★ 2,459 · 220 forks · pushed 2025-02-17.
- [OpenXcom/OpenXcom](https://github.com/OpenXcom/OpenXcom) - UFO: Enemy Unknown and Terror from the Deep engines, MS-DOS and Windows, clean-room. ★ 2,232.
- [wheybags/freeablo](https://github.com/wheybags/freeablo) - Diablo 1.09, Windows → Windows, Linux and macOS, independent reimplementation of the engine, needing both `DIABDAT.MPQ` and `Diablo.exe` from the reader's copy, GPL-3.0. ★ 2,170 · 196 forks · archived, last push 2023-04-13.
- [sdlpal/sdlpal](https://github.com/sdlpal/sdlpal) - 仙剑奇侠传 / The Legend of Sword and Fairy, MS-DOS and Windows → Windows, Linux, macOS, Android, iOS, 3DS, Wii, PSP and the browser, cross-platform reimplementation built on the PAL Research Project's format documents, GPL-3.0. ★ 1,980 · 393 forks · pushed 2026-10-17.
- [OpenLoco/OpenLoco](https://github.com/OpenLoco/OpenLoco) - Chris Sawyer's Locomotion engine, MS-DOS, clean-room. ★ 1,939.
- [OpenDUNE/OpenDUNE](https://github.com/OpenDUNE/OpenDUNE) - Dune II engine, MS-DOS, clean-room. ★ 1,695.
- [OpenSAGE/OpenSAGE](https://github.com/OpenSAGE/OpenSAGE) - Command & Conquer: Red Alert 3 and Generals engines, Windows, clean-room. ★ 1,649.
- [Try/OpenGothic](https://github.com/Try/OpenGothic) - Gothic 2: Night of the Raven, Windows → Windows, Linux and macOS, re-implementation aiming at a client compatible with the original data and mods, MIT. ★ 1,622 · 143 forks · pushed 2026-10-13.
- [openblack/openblack](https://github.com/openblack/openblack) - Black & White, Windows → Windows, Linux and macOS, "open source reimplementation … written in modern C++" reading the original assets, GPL-3.0. ★ 1,584 · 104 forks · pushed 2026-10-17.
- [afritz1/OpenTESArena](https://github.com/afritz1/OpenTESArena) - The Elder Scrolls: Arena, MS-DOS → Windows, Linux and macOS, "replicate all aspects of the original game with a clean-room approach", MIT. ★ 1,431 · 87 forks · pushed 2026-10-08.
- [doukutsu-rs/doukutsu-rs](https://github.com/doukutsu-rs/doukutsu-rs) - Cave Story, Windows → Windows, macOS, Linux, Android and Nintendo Switch, Rust reimplementation of the engine as a drop-in for the shipped executable, MIT. ★ 1,313 · 82 forks · pushed 2026-10-13.
- [NagyD/SDLPoP](https://github.com/NagyD/SDLPoP) - Prince of Persia, MS-DOS → Windows, Linux, macOS and OS/2, "open-source port … based on the disassembly of the DOS version", GPL-3.0. ★ 1,299 · 174 forks · last push 2025-12-24.
- [gemrb/gemrb](https://github.com/gemrb/gemrb) - BioWare's Infinity Engine behind Baldur's Gate, Icewind Dale and Planescape: Torment, Windows → Windows, Linux, macOS, Android, iOS and consoles, reimplementation working from the data formats, GPL-2.0. ★ 1,262 · 227 forks · pushed 2026-10-17.
- [yvt/openspades](https://github.com/yvt/openspades) - Ace of Spades 0.75, Windows → Linux, Windows and macOS, compatible client: the voxel engine and the server protocol reimplemented from observation, GPL-3.0. ★ 1,246 · 233 forks · last push 2024-06-06.
- [dethrace-labs/dethrace](https://github.com/dethrace-labs/dethrace) - Carmageddon, MS-DOS → Windows, Linux and macOS, "replacing the original assembly code with equivalent C code, function by function", from the Watcom symbol file left on the Splat Pack CD, GPL-3.0. ★ 1,219 · 97 forks · pushed 2026-10-17.
- [xoreos/xoreos](https://github.com/xoreos/xoreos) - BioWare's Aurora engine and derivatives: Neverwinter Nights, Knights of the Old Republic, Jade Empire, The Witcher, Windows and Xbox → Windows, macOS and Linux, reimplementation of the resource and script formats with gameplay still partial, GPL-3.0. ★ 1,184 · 137 forks · pushed 2026-09-04.
- [TheForceEngine/TheForceEngine](https://github.com/TheForceEngine/TheForceEngine) - Star Wars: Dark Forces, MS-DOS → Windows, Linux and macOS, "reverse engineer and rebuild the Jedi Engine for modern systems", GPL-2.0. ★ 1,165 · 91 forks · pushed 2026-10-12.
- [RSDKModding/RSDKv4-Decompilation](https://github.com/RSDKModding/RSDKv4-Decompilation) - Sonic 1 and Sonic 2 (2013), the Retro Engine v4, Windows, Nintendo Switch and Android releases, "a complete decompilation" that will not run without the officially released assets, custom licence. ★ 1,146 · 261 forks · pushed 2026-09-06.
- [dpjudas/SurrealEngine](https://github.com/dpjudas/SurrealEngine) - Unreal Engine 1, Windows → Windows, macOS and Linux, self-described as a project that "aims to reimplement Unreal Engine 1", loading the reader's own original copies of Unreal, Unreal Tournament and Deus Ex, zlib-style licence. ★ 1,116 · 59 forks · pushed 2026-10-17.
- [collinsmith/riiablo](https://github.com/collinsmith/riiablo) - Diablo II, Windows → PC and Android, Java and LibGDX rebuild "from scratch" on the original MPQ assets, Apache-2.0. ★ 1,104 · 123 forks · last push 2025-01-13. The README states it is not playable yet.
- [gta-reversed/gta-reversed](https://github.com/gta-reversed/gta-reversed) - Grand Theft Auto: San Andreas, Windows, rewrite of the shipped 1.0 executable "function by function" that replaces the game's own routines at load time, **no license declared**. ★ 1,073 · 253 forks · pushed 2026-10-16. The README estimates "about 50-60% of the code is done".
- [isledecomp/isle-portable](https://github.com/isledecomp/isle-portable) - LEGO Island, Windows 9x → Windows, macOS, Linux, iOS, Android, Nintendo Switch, PS Vita and Xbox One, the `isledecomp/isle` C++ moved to modern hosts by replacing the Windows-only libraries, LGPL-3.0. ★ 1,071 · 100 forks · pushed 2026-10-15.
- [vladtrc/iw4L](https://github.com/vladtrc/iw4L) - Call of Duty: Modern Warfare 2 (2009), Windows → Windows, Linux and macOS, runtime reimplemented in Rust over the reader's own installation, Apache-2.0. ★ 1,071 · 130 forks · pushed 2026-10-16. Its README states "This whole project is written by an LLM."
- [dkfans/keeperfx](https://github.com/dkfans/keeperfx) - Dungeon Keeper, Windows → Windows, "the whole codebase of Dungeon Keeper is remade", begun as a decompilation of the original executables and since rewritten, GPL-2.0. ★ 1,020 · 133 forks · pushed 2026-10-16.
- [LostArtefacts/TRX](https://github.com/LostArtefacts/TRX) - Tomb Raider 1, 2 and 3, MS-DOS and Windows → Windows and Linux, reimplementation reached "through decompilation", keeping each classic engine's distinct mechanics, GPL-3.0. ★ 1,009 · 72 forks · pushed 2026-10-17.
- [lethal-guitar/RigelEngine](https://github.com/lethal-guitar/RigelEngine) - Duke Nukem II, MS-DOS → Windows, Linux, macOS, Steam Deck and Raspberry Pi, "based on reverse engineering (specifically, disassembly of the original binaries)", GPL-2.0. ★ 1,007 · 69 forks · pushed 2026-09-28.
- [TheAssemblyArmada/Thyme](https://github.com/TheAssemblyArmada/Thyme) - Three's Company full-motion-video game engine, MS-DOS, clean-room. ★ 696.
- [exult/exult](https://github.com/exult/exult) - Ultima VII engine, MS-DOS and Macintosh, GPL-2.0. ★ 693.
- [opentyrian/opentyrian](https://github.com/opentyrian/opentyrian) - Tyrian engine, MS-DOS, GPL-2.0. ★ 587.
- [nxengine/nxengine-evo](https://github.com/nxengine/nxengine-evo) - Cave Story engine, Windows, clean-room. ★ 551.
- [omf2097/openomf](https://github.com/omf2097/openomf) - One Must Fall 2097 by Diversions Entertainment, MS-DOS 1994 → Windows, Linux, macOS and BSD, engine remake started because the original's IPX networking "is a pain to set up", on the reader's own game resources, MIT. ★ 485 · 59 forks · pushed 2026-10-17.
- [AlisterT/openjazz](https://github.com/AlisterT/openjazz) - Jazz Jackrabbit engine, MS-DOS, GPL-2.0. ★ 409.
- [stefanhendriks/Dune-II---The-Maker](https://github.com/stefanhendriks/Dune-II---The-Maker) - Dune 2 by Westwood Studios, MS-DOS → Windows, Linux and macOS, SDL3 remake that carries its own campaign, map and shader resources in the tree and adds skirmish play, zooming and higher resolutions, MIT text in LICENSE.md where GitHub reports NOASSERTION. ★ 368 · 39 forks · pushed 2026-10-17.
- [IllegalCreed/type-pal](https://github.com/IllegalCreed/type-pal) - 《仙剑奇侠传》 (PAL, Softstar, 1995), DOS and Windows → the browser, written from scratch in TypeScript with its own MKF extractor, script virtual machine, palette renderer and visual editor, GPL-3.0. ★ 196 · 19 forks · created 2026-05-22 · pushed 2026-10-17. It keeps a copy of sdlpal's C source in reference/ as a specification only, and says plainly that the committed demo still holds a little PAL-derived art that is not cleared for release.
- [Pyrdacor/freeserf.net](https://github.com/Pyrdacor/freeserf.net) - The Settlers I by BlueByte, DOS and Amiga → Windows, Linux, macOS and Android, C# remake written as a port and extension of the freeserf clone, with added AI and local-network play, on the reader's original data files, GPL-3.0. ★ 173 · 18 forks · pushed 2026-10-17.
- [turican0/remc2](https://github.com/turican0/remc2) - Magic Carpet 2, MS-DOS → Windows and Linux, rebuilt from the shipped assembler into C/C++ and continued from the reverse engineering it credits, with a regression test suite and its own enhanced asset set, **no license declared**. ★ 151 · 19 forks · pushed 2026-10-16.
- [mytbk/rich4](https://github.com/mytbk/rich4) - Richman 4 (大富翁4), Windows, disassembly that re-links against MinGW and `msvcrt` into a runnable `rich4.exe`, GPL-3.0. ★ 146 · 20 forks · created 2018-09-27 · pushed 2026-10-08.
- [Wargus/war1gus](https://github.com/Wargus/war1gus) - WarCraft 1 as a strategy engine on top of Wargus, MS-DOS and Windows, GPL-2.0. ★ 134.
- [jhaizhou-ops/sts2-ios](https://github.com/jhaizhou-ops/sts2-ios) - Slay the Spire 2, Steam Windows and Linux build → iOS, "bring your own Steam copy". ★ 63 · created 2026-07-15.
- [N0zoM1z0/dx-ball](https://github.com/N0zoM1z0/dx-ball) - DX-Ball, MS-DOS: the 1996 shareware `DXBALL.EXE` reconstructed to C and C++, "exact reconstruction is in progress". ★ 62. A post claims a Steam build runs; the repository does not say so.
- [N0zoM1z0/th04](https://github.com/N0zoM1z0/th04) - Touhou 4, Windows: `MAIN.EXE` reconstructed to C++, with "2,139 matching bytes" claimed against the original. ★ 33.
- [oliverjessner/OpenEmperor](https://github.com/oliverjessner/OpenEmperor) - Emperor: Rise of the Middle Kingdom, real-time strategy, Windows → Apple Silicon macOS, clean-room reimplementation in C++20 and SDL3 that reads the original game files the player supplies and bundles no original assets. ★ 16 · 2 forks · created 2026-09-15 · pushed 2026-10-16. Early development by its own description, and its documentation separates observed source facts, supported interpretation and authored preview behaviour — the map format and graphics IDs are recorded there as reverse-engineering evidence.
- [lhr0909/richman4-remastered](https://github.com/lhr0909/richman4-remastered) - Richman 4 (大富翁4), Windows → macOS, Android and iOS, engine rewritten rule by rule against `mytbk/rich4`'s published disassembly rather than clean-room, GPL-3.0. ★ 10 · 3 forks · created and pushed 2026-10-06. Its NOTICE limits a built APK to the builder's own devices.
- [bradhannah/UltimaVRedux](https://github.com/bradhannah/UltimaVRedux) - Ultima V: Warriors of Destiny, MS-DOS → Windows, macOS and Linux, Go recreation that reads the player's own game files, keeps SAVED.GAM save compatibility through a command-line converter, and ships a developer Debug Workbench, MIT. ★ 11 · created 2026-10-06 · pushed 2026-10-16.
- [kichikuou/xsystem4](https://github.com/kichikuou/xsystem4) - AliceSoft System 4 visual novels, Windows titles rebuilt for unix-like systems, GPL-2.0. ★ 3 · pushed 2026-10-17.
- [wicanr2/softworld_san1_remake](https://github.com/wicanr2/softworld_san1_remake) - 《三國演義》 (Softworld, 1991), MS-DOS → Windows, Linux and macOS, engine rewritten in Go and Ebiten against the original's verifiable behaviour, keeping the confirmed rule differences of both releases, needs the reader's own game data. ★ 3 · created 2026-09-06 · pushed 2026-10-15. Rule restoration is signed off differentially: the project's own headless DOS runner executes the original executable and the remake is compared against variables and calls read out of it.

`xsystem4` keeps a public `game_compatibility.md`: 66 titles, 41 supported, 18 unknown, 7 unsupported, with 戦国ランス / Sengoku Rance, Rance VI, Rance 01 and Rance 02 marked supported and ランス・クエスト unsupported. The same author also maintains `xsystem35-sdl2`, `xsystem4-android`, `xsys35c` (under Formats, file systems and protocols), `system3-sdl2`, `sys4lang` and `libsys4`.

`mytbk/rich4` pins its target: `rich4.exe` v3.11, 588 KiB, SHA-256 `5a90aee28ee5f7a5c3ba5cb935c9e55751a529c25fcd91208748a66293569550`. Three months of work in 2018 produced the data-file unpacking algorithm and the save format; in 2021 the executable became re-linkable assembly via `mytbk/r2dumpbin`; in 2025 the Watcom C runtime was stripped far enough that MinGW and `msvcrt` link a runnable `rich4.exe`. The annotated split lives in `vimacs/rich4_asm` on Codeberg, and `tytannial/rich4-re` is a third attempt at the same title. `lhr0909/richman4-remastered` states in its own acknowledgements that every rule, screen and animation timing was rewritten against that published disassembly; the Steam release of 《大富翁4》 supplies the assets.

The Diablo line has three destinations and one origin: `diasurgical/devilution` reconstructed the 1996 code from the symbol file the Climax PlayStation port left behind and from a debug build hidden inside `DIABDAT.MPQ` as `D1221A.MPQ`, and it deliberately keeps the original bugs; `diasurgical/DevilutionX` is the SDL port of that reconstruction to about a dozen platforms; `d07RiV/diabloweb` builds a forked devilution to WebAssembly for browsers. All three carry the Sustainable Use License, the non-commercial licence GitHub reports as `NOASSERTION`. `wheybags/freeablo` reimplements the same engine by another route and needs `Diablo.exe` as well as the MPQ. Caesar III has the same fork relationship: `Keriew/augustus` is the fork of `bvschaik/julius` that adds gameplay changes and gives up the two-way save compatibility Julius holds to. The Fallout community editions state their own method chain — each is built on the author's matching reverse-engineered base rather than on any Interplay or Bethesda source release.

### Home computers

- [Pyrdacor/Ambermoon.net](https://github.com/Pyrdacor/Ambermoon.net) - Ambermoon, Amiga → Windows, Linux, macOS and Android, full rewrite in C# with the original data formats reimplemented in its Ambermoon.Data projects, played on the game files the reader obtains itself, GPL-3.0. ★ 541 · 34 forks · pushed 2026-10-16.
- [skoolkid/pyskool](https://github.com/skoolkid/pyskool) - Skool Daze (Microsphere, 1984) and Back to Skool (1985), Sinclair ZX Spectrum → any platform Python runs on, re-implementation in Python and Pygame with the schools, characters and behaviour rebuilt in its own source, GPL-3.0. ★ 19 · 4 forks · pushed 2026-10-16.

### Mobile

- [JoppieToppie/Galaxy-on-Fire-2-Unity-Remake](https://github.com/JoppieToppie/Galaxy-on-Fire-2-Unity-Remake) - Galaxy on Fire 2, Android and iOS → Windows, Linux and Android, Unity remake whose game logic is "ported from the decompiled game code", the original assets shipped in the tree, Apache-2.0 text in its LICENSE.md where GitHub reports NOASSERTION. ★ 148 · 16 forks · pushed 2026-10-17.

## Applications

Programs that are not games, reconstructed well enough to run the original content.

- [ruffle-rs/ruffle](https://github.com/ruffle-rs/ruffle) - Adobe Flash Player, AVM2 plus rendering, Rust, clean-room. ★ 18,695.
- [storytold/wordcraft](https://github.com/storytold/wordcraft) - Microsoft Word for Windows and Mac, consuming the original document formats, Apache-2.0, Rust. ★ 13,774. Its README states "Clean-room: built from public specifications and observation, with every asset original or openly licensed", so it is filed as clean-room work.
- [storytold/gridcraft](https://github.com/storytold/gridcraft) - Microsoft Excel, rebuilt clean-room in Rust with XLSX as its native format and XLSB and ODS worksheet data import, Apache-2.0. ★ 5,455 · 2,487 forks · created 2026-10-07 · pushed 2026-10-16. The repository publishes its own unfinished state: ROADMAP.md holds the stage, numbers and effort estimates and docs/gaps.md the ranked work left.
- [storytold/cadcraft](https://github.com/storytold/cadcraft) - Autodesk AutoCAD, rebuilt clean-room in Rust: the command line, object snaps, layers, dimensions, hatches, blocks and DXF drawings, Apache-2.0. ★ 5,451 · 2,407 forks · created 2026-10-07 · pushed 2026-10-16. Its README names the boundary itself: SHX fonts, including big fonts such as chineset.shx, are not read yet, so SHX-styled text is drawn with the project's own stroke font.
- [storytold/deckcraft](https://github.com/storytold/deckcraft) - Microsoft PowerPoint, rebuilt clean-room in Rust: opens and saves .pptx, exports PDF, PNG/JPEG and an animated GIF of the deck, Apache-2.0. ★ 3,603 · 2,032 forks · created 2026-10-07 · pushed 2026-10-16. The repository publishes its own unfinished state: it calls itself alpha heading for beta, and ROADMAP.md, docs/target-app-parity.md, docs/gaps.md and docs/parity-checklist.md carry the assessment.
- [storytold/soundcraft](https://github.com/storytold/soundcraft) - Avid Pro Tools, rebuilt clean-room in Rust as a multitrack DAW with fader automation, a MIDI score editor and MusicXML export, Apache-2.0. ★ 3,094 · 1,939 forks · created 2026-10-07 · pushed 2026-10-16. Parity with the target app is measured in the open: docs/target-app-parity.md holds the assessment and docs/parity-checklist.md compares the two menu by menu.
- [storytold/figcraft](https://github.com/storytold/figcraft) - Figma, rebuilt clean-room in Rust: SVG, PNG, JPG, WebP and PDF in and out, .fig files opened best-effort, Apache-2.0. ★ 2,219 · 805 forks · created 2026-10-09 · pushed 2026-10-17. Its own boundary statement is explicit — no proprietary code, file formats, icons or images, every icon drawn in code or made for the project — and the area-by-area picture is left to the roadmap and docs/target-app-parity.md.
- [ruvnet/open-claude-code](https://github.com/ruvnet/open-claude-code) - Anthropic's Claude Code CLI, rebuilt from an AI-assisted decompilation of the published npm bundle, mirroring its agent loop, tools, MCP transports and permission modes, MIT. ★ 535 · 165 forks · created 2025-02-24 · pushed 2026-10-17. The repository holds two descriptions of itself at once: head#118 says the rebuild is informed by ruDevolution's decompilation of the published npm package, while a later line insists it is clean-room with no leaked source. Its own link list calls the remainder a path to 100%, and the decompiler is a submodule (ruvnet/rudevolution), not part of this tree.
- [daijro/honeydew](https://github.com/daijro/honeydew) - FL Studio Mobile, rebuilt clean-room in Rust with browser and Android builds, opening FL Studio Mobile's .flm demo projects, GPL-3.0. ★ 10 · 2 forks · created 2026-10-14 · pushed 2026-10-17. Its own status: the first port supports playback and songs saved inside the app, while microphone recording, MIDI devices and Android file import/export are not available yet — and sounds and presets import from a copy of the app the reader owns.
- [soyrochus/mucrab](https://github.com/soyrochus/mucrab) - muCommander, a Java desktop application reimplemented in Rust from observed behaviour, with test reports. ★ 1.

## Runtimes and compatibility layers

The platform the program expects, rebuilt or shimmed: an API, a firmware interface, a runtime, an emulator, or the patch that unblocks one title on a new host.

- [doitsujin/dxvk](https://github.com/doitsujin/dxvk) - Direct3D 9/10/11 translated onto Vulkan for Windows and under Wine, Zlib. ★ 18,309.
- [reactos/reactos](https://github.com/reactos/reactos) - Windows NT on x86, from black-box observation, GPL-2.0. ★ 18,235.
- [azahar-emu/azahar](https://github.com/azahar-emu/azahar) - Nintendo 3DS, emulated on Windows, Linux and macOS; the active successor to Citra. ★ 8,380 · created 2024-03-04.
- [focus-creative-games/hybridclr](https://github.com/focus-creative-games/hybridclr) - Unity IL2CPP managed runtime on iOS, Android and desktop, MIT. ★ 7,995.
- [AsahiLinux/m1n1](https://github.com/AsahiLinux/m1n1) - Boot and firmware interfaces on Apple silicon, GPL-2.0. ★ 4,267.
- [HansKristian-Work/vkd3d-proton](https://github.com/HansKristian-Work/vkd3d-proton) - Direct3D 12 translated onto Vulkan under Wine and Proton, LGPL-2.1. ★ 3,006.
- [ExpansionPak/ModernGekko](https://github.com/ExpansionPak/ModernGekko) - Runtime that GameCube and Wii recompilations load into, built on the Dolphin codebase, with a code-mod ABI for `mod.so`, `mod.dll` and `mod.dylib` packages, GPL-3.0. ★ 171 · 18 forks · created 2026-06-25 · pushed 2026-09-17.
- [yuzuatri/Sengoku-Rance-Deck-Fix](https://github.com/yuzuatri/Sengoku-Rance-Deck-Fix) - Sengoku Rance on Proton and Linux: the executable-patch answer to the Wine codepage problem below — version-checked, SHA-256 gated, four bytes at two offsets, backup kept, optional user-supplied `simhei.ttf` installed into the game's Proton prefix. ★ 6 · MIT · created 2026-10-02.

Wine codepage gap: Wine 10.0 ships 76 `.nls` codepage tables, and GB18030 (`c_54936.nls`) is not one of them, so a Simplified-Chinese title that calls `MultiByteToWideChar(54936, …)` during process init hangs with no window. Two fixes exist: add the missing table to the prefix (under Proton it must land in `syswow64`, because Wine redirects a 32-bit process's `system32` lookups), or patch the executable to request CP936. ⚠ *Substituting the GBK table loses GB18030's 4-byte sequences, so either route is an approximation; what differs between them is invasiveness, not correctness.*

## Formats, file systems and protocols

File formats, file systems and network protocols reimplemented from observation, with no original implementation shipped.

- [librespot-org/librespot](https://github.com/librespot-org/librespot) - Spotify Connect and playback protocol, for Linux and other platforms, MIT. ★ 7,299.
- [sgan81/apfs-fuse](https://github.com/sgan81/apfs-fuse) - Apple File System read path on Linux and macOS, GPL-2.0; dormant. ★ 2,161.
- [LibreDWG/libredwg](https://github.com/LibreDWG/libredwg) - AutoCAD DWG, GPL-3.0; this is the official GitHub mirror. ★ 1,627.
- [tuxera/ntfs-3g](https://github.com/tuxera/ntfs-3g) - NTFS read and write on Linux, GPL-2.0. ★ 1,521.
- [f4pga/prjxray](https://github.com/f4pga/prjxray) - Xilinx 7-series FPGA bitstream format, ISC. ★ 925.
- [linux-apfs/linux-apfs-rw](https://github.com/linux-apfs/linux-apfs-rw) - APFS with write support inside the Linux kernel, GPL-2.0. ★ 804.
- [kichikuou/xsys35c](https://github.com/kichikuou/xsys35c) - AliceSoft System 3.x scripting bytecode on DOS and Windows: compiler and decompiler for the format, GPL-2.0. ★ 40 · pushed 2026-10-13.
- [gibbed/Gibbed.LetUsClingTogether](https://github.com/gibbed/Gibbed.LetUsClingTogether) - Tactics Ogre: Let Us Cling Together on PSP and its remaster Tactics Ogre: Reborn: format libraries with unpackers and exporters for the .pac and .pakd archives, the compiled .xlc spreadsheet tables, screenplay and event files and images, plus a cutscene script disassembler, Zlib. ★ 36 · 6 forks · pushed 2026-10-16.

LibreDWG is GPL-3, which is incompatible with the LGPL downstreams that would adopt it: a finished format reconstruction that its own ecosystem cannot absorb.

## Related lists

This list takes results only; these take tools or a wider net.

- [alphaSeclab/awesome-reverse-engineering](https://github.com/alphaSeclab/awesome-reverse-engineering) - Reverse-engineering resources across Windows, Linux and macOS, tool-heavy. ★ 5,131.
- [user1342/Awesome-Android-Reverse-Engineering](https://github.com/user1342/Awesome-Android-Reverse-Engineering) - Android RE training, tools and resources. ★ 2,740.
- [morluto/awesome-reverse-engineering](https://github.com/morluto/awesome-reverse-engineering) - Curated RE tools and learning resources for binaries; the tool list this list deliberately is not. ★ 647.
- [SubmitGame/awesome-decomp-games](https://github.com/SubmitGame/awesome-decomp-games) - Auto-refreshed, rated list of decompiled, recompiled and reverse-engineered games: 2,118 projects over 1,829 titles, regenerated daily from `data/games.json`. ★ 1,068 · CC0 · created 2026-10-09. It widens coverage automatically and scores playability.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) for how to add an entry, and `INTAKE.md` and `AGENTS.md` for how the list is classified, sourced and refreshed. The rules that decide most PRs: **file the entry under the kind of software it reconstructed, name the original platform and the method**, because "cool project, you should look at it" is not an entry; and **unverified claims get a ⚠ or stay out** — name the primary source you actually read, or write what you could not read.
