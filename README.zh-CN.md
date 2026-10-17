# Awesome REA [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

已完成的逆向成果：重写的引擎、逐字节匹配的源码还原、重实现的格式/协议/驱动/API、平台移植、兼容性补丁。

[English](README.md) | **简体中文**

本清单收录的是**成果**而不是仪器：别人真的拆开并且真的重建了哪些程序、格式和协议。条目按**被重建的软件类型**归档；在「游戏」一节里再按**它原来跑在什么平台**上分二级。每一行都写明那个平台（移植会写两端）以及它是**用哪种方法**重建的。调试器、反编译器、十六进制编辑器、修改器一类工具不在范围内，工具清单见文末「相关清单」。

本清单以 [`rea`](https://github.com/morluto/rea) 命名——一个 agent 驱动的逆向工具包。条目收的是重建物本身，无论是谁、用哪条工具链做出来的。

所有星标数与最近推送日期都读自 GitHub 的 `GET /repos/{owner}/{repo}` 接口，并由定时的 CI 作业重写。**数据刷新于 2026-10-17。** **⚠** 表示该说法没有读到一手来源，因此不算数据。本清单的维护规则写在 [AGENTS.md](AGENTS.md)。

## 目录

- [游戏](#游戏)
  - [任天堂](#任天堂)
  - [Sony PlayStation](#sony-playstation)
  - [Microsoft Xbox 与 Xbox 360](#microsoft-xbox-与-xbox-360)
  - [MS-DOS、Windows 与 Macintosh](#ms-doswindows-与-macintosh)
  - [移动端](#移动端)
- [应用程序](#应用程序)
- [运行时与兼容层](#运行时与兼容层)
- [格式文件系统与协议](#格式文件系统与协议)
- [相关清单](#相关清单)

## 游戏

出货作品的引擎、反编译产物与重编译版本。这些几乎都不带游戏文件，素材由用户以自己的合法副本提供；确实内置原版素材的条目会在行里写明。

### 任天堂

- [n64decomp/sm64](https://github.com/n64decomp/sm64) - Super Mario 64，任天堂 64，反编译成 C 之后能重新构建出与出货版本一致的 ROM，CC0-1.0。★ 8,889 · 1,652 fork · 推送于 2024-02-04。
- [Zelda64Recomp/Zelda64Recomp](https://github.com/Zelda64Recomp/Zelda64Recomp) - 塞尔达传说 姆吉拉的假面，任天堂 64 → Windows、Linux 与 macOS，对卡带二进制做静态重编译，自述"This is not an emulator"，GPL-3.0。★ 7,447 · 344 fork · 推送于 2026-09-25。
- [TwilitRealm/dusklight](https://github.com/TwilitRealm/dusklight) - 塞尔达传说 黄昏公主，GameCube → Windows、Linux、macOS、Android 与 iOS，自述"a reverse-engineered reimplementation"，建立在 `zeldaret/tp` 的反编译之上，CC0-1.0。★ 5,888 · 441 fork · 推送于 2026-10-11。
- [HarbourMasters/Shipwright](https://github.com/HarbourMasters/Shipwright) - 塞尔达传说 时之笛，任天堂 64 → Windows、Linux 与 macOS，把 `zeldaret/oot` 的反编译移植到 libultraship 上的源码移植，**未声明许可证**。★ 5,639 · 919 fork · 推送于 2026-10-15。
- [zeldaret/oot](https://github.com/zeldaret/oot) - 塞尔达传说 时之笛，任天堂 64，逐字节匹配的反编译。★ 5,595。符号匹配工作流的标杆项目。
- [pret/pokered](https://github.com/pret/pokered) - 精灵宝可梦 红/蓝，Game Boy，反汇编，可重新装配回原版 ROM。★ 4,996。
- [snesrev/zelda3](https://github.com/snesrev/zelda3) - 塞尔达传说 众神的三角力量，超级任天堂 → Windows、Linux 与 macOS，C 语言写的"a reverse engineered clone"，与原版机器码并行运行并在每帧之后比对 RAM，MIT。★ 4,865 · 453 fork · 推送于 2026-10-02。
- [bryanthaboi/gen1recomp](https://github.com/bryanthaboi/gen1recomp) - 精灵宝可梦 红一直到绿宝石，Game Boy 与 Game Boy Advance → Windows、Linux、macOS、iOS、Switch 与各主机，引擎与地图行为是照 pret 的反编译手写的 Lua，不是净室，GPL-3.0 加附加条款。★ 3,946 · 356 fork · 推送于 2026-10-15。
- [pret/pokeemerald](https://github.com/pret/pokeemerald) - 精灵宝可梦 绿宝石，Game Boy Advance，反编译，构建出的 ROM 通过 SHA-1 校验，**未声明许可证**。★ 3,602 · 4,826 fork · 推送于 2026-10-01。
- [jhaizhou-ops/d2r-mobile](https://github.com/jhaizhou-ops/d2r-mobile) - 暗黑破坏神 II：狱火重生，Nintendo Switch → iOS、iPad、Mac，静态重编译，底下是一套重实现的 NVN、系统调用、VFS、音频与输入接口面。★ 3,547 · 1,025 fork · MIT · 建库于 2026-10-12。
- [pret/pokecrystal](https://github.com/pret/pokecrystal) - 精灵宝可梦 水晶，Game Boy，反汇编。★ 2,528。
- [HarbourMasters/SpaghettiKart](https://github.com/HarbourMasters/SpaghettiKart) - 马里奥赛车 64，任天堂 64 → Windows、Linux、macOS 与 Nintendo Switch，libultraship 上的源码移植，要玩家自己的 ROM，**未声明许可证**。★ 2,418 · 153 fork · 推送于 2026-10-11。
- [doldecomp/melee](https://github.com/doldecomp/melee) - 任天堂明星大乱斗 DX，GameCube，对美版 1.02 的 `main.dol` 做匹配反编译，**未声明许可证**。★ 2,415 · 356 fork · 推送于 2026-10-16。
- [2ship2harkinian/2ship2harkinian](https://github.com/2ship2harkinian/2ship2harkinian) - 姆吉拉的假面，任天堂 64 → Windows、Linux 与 macOS，与 `HarbourMasters/Shipwright` 同一套 libultraship 的源码移植，CC0-1.0。★ 2,331 · 274 fork · 推送于 2026-10-14。
- [zeldaret/botw](https://github.com/zeldaret/botw) - 塞尔达传说 旷野之息，Switch 1.5.0，自述"experimental, WIP decompilation"，README 写明**不能**拿它玩游戏，**未声明许可证**。★ 2,246 · 140 fork · 推送于 2026-10-15。
- [HarbourMasters/Starship](https://github.com/HarbourMasters/Starship) - 星际火狐 64，任天堂 64 → Windows、Linux、macOS 与 Nintendo Switch，SF64 反编译的源码移植，CC0-1.0。★ 2,099 · 144 fork · 推送于 2026-09-15。
- [zeldaret/tp](https://github.com/zeldaret/tp) - 塞尔达传说 黄昏公主，GameCube，反编译，其 GameCube 代码自述"is completely matching"，CC0-1.0。★ 2,090 · 206 fork · 推送于 2026-06-23。
- [perfect-dark-pc-port/perfect_dark](https://github.com/perfect-dark-pc-port/perfect_dark) - 完美黑暗，任天堂 64 → Windows、Linux、macOS 与 Nintendo Switch，反编译的进行中移植，原始仓库已迁到 GitLab，MIT。★ 2,057 · 156 fork · 推送于 2026-08-13。
- [BanjoRecomp/BanjoRecomp](https://github.com/BanjoRecomp/BanjoRecomp) - 班卓熊大冒险，任天堂 64 → Windows、Linux 与 macOS，静态重编译，自述"not based on the source code provided by a decompilation"，GPL-3.0。★ 2,047 · 74 fork · 推送于 2026-09-25。
- [sm64pc/sm64ex](https://github.com/sm64pc/sm64ex) - Super Mario 64，任天堂 64 → Windows、Linux 与 macOS，`n64decomp/sm64` 反编译的源码移植，带增强包与镜头 mod，**未声明许可证**。★ 1,865 · 574 fork · 推送于 2024-12-17。
- [zeldaret/mm](https://github.com/zeldaret/mm) - 梅祖拉的假面，任天堂 64，与 `oot` 同一套工具链的逐字节匹配反编译。★ 1,744。
- [pret/pokefirered](https://github.com/pret/pokefirered) - 精灵宝可梦 火红/叶绿，Game Boy Advance，反编译，能构建六个具名 ROM 镜像，含 Switch 修订版，**未声明许可证**。★ 1,665 · 1,040 fork · 推送于 2026-09-26。
- [pmret/papermario](https://github.com/pmret/papermario) - 纸片马里奥，任天堂 64，进行中的反编译，按地区给出 SHA-1 进度，**未声明许可证**。★ 1,633 · 170 fork · 推送于 2026-09-26。
- [flyngmt/ACGC-PC-Port](https://github.com/flyngmt/ACGC-PC-Port) - 动物之森，GameCube → Windows，自述"a native PC port … built on top of the ac-decomp decompilation project"，自定义许可证。★ 1,493 · 126 fork · 推送于 2026-08-02。它的 README 记录 AI 工具只用在这个 PC 移植的代码上。
- [ACreTeam/ac-decomp](https://github.com/ACreTeam/ac-decomp) - 动物之森，GameCube，把美版 GAFE01 光盘反编译成 C，CC0-1.0。★ 1,413 · 93 fork · 推送于 2026-07-18。
- [n64decomp/mk64](https://github.com/n64decomp/mk64) - 马里奥赛车 64，任天堂 64，反编译，尚未匹配的汇编仍列在 `asm/non_matchings` 里，**未声明许可证**。★ 1,311 · 138 fork · 推送于 2026-08-16。
- [SMGCommunity/Petari](https://github.com/SMGCommunity/Petari) - 超级马里奥 银河，Wii，`main.dol` 的进行中反编译，README 写明本项目"not meant to be an effort to create a PC port"，CC0-1.0。★ 1,248 · 116 fork · 推送于 2026-10-14。
- [patchzyy/Wiicompiled](https://github.com/patchzyy/Wiicompiled) - 马里奥赛车 Wii，Wii → Windows、Linux 与 macOS，对 PAL 的 `RMCP01` 光盘镜像做静态重编译，自述"There's no emulator in the loop"，GPL-3.0。★ 1,169 · 110 fork · 推送于 2026-10-16。
- [zeldaret/tww](https://github.com/zeldaret/tww) - 风之杖，GameCube，逐字节匹配的反编译，CC0-1.0。★ 1,099 · 推送于 2026-10-14。
- [pret/pokeruby](https://github.com/pret/pokeruby) - 精灵宝可梦 红宝石/蓝宝石，Game Boy Advance，自述为反汇编，构建出匹配的 ROM，**未声明许可证**。★ 1,003 · 273 fork · 推送于 2026-09-29。
- [pret/pokeyellow](https://github.com/pret/pokeyellow) - 精灵宝可梦 黄，Game Boy，反汇编，可重新装配回 SHA-1 校验的原版 ROM，**未声明许可证**。★ 891 · 348 fork · 建库于 2015-05-10 · 推送于 2026-10-16。
- [pret/pokegold](https://github.com/pret/pokegold) - 精灵宝可梦 金/银，Game Boy 彩色版，两套发行各自用一个 SHA-1 钉住，**未声明许可证**。★ 727 · 205 fork · 建库于 2015-07-09 · 推送于 2026-10-06。
- [Kirby64Ret/kirby64](https://github.com/Kirby64Ret/kirby64) - 星之卡比64，任天堂 64，进行中的逐字节匹配反编译，**未声明许可证**。★ 234 · 21 fork · 推送于 2026-09-13。
- [tangosdev/sm64ds-decomp](https://github.com/tangosdev/sm64ds-decomp) - Super Mario 64 DS，任天堂 DS，由 agent 工作流产出的反编译。★ 202 · 建库于 2026-06-14。
- [jiangzhengwenjz/katam](https://github.com/jiangzhengwenjz/katam) - 星之卡比 镜之大迷宫，Game Boy Advance，进行中的反编译，**未声明许可证**。★ 158 · 21 fork · 建库于 2020-01-11 · 推送于 2026-09-17。
- [doldecomp/kar](https://github.com/doldecomp/kar) - Kirby Air Ride，GameCube，反编译，**未声明许可证**。★ 88 · 10 fork · 推送于 2025-02-26。
- [Swiftshine/key](https://github.com/Swiftshine/key) - 星之卡比 毛线传说，Wii，针对美版发行的逐字节匹配反编译，CC0-1.0。★ 52 · 4 fork · 推送于 2026-10-14。
- [Petexy/Tekken-Tag-2-Recompiled](https://github.com/Petexy/Tekken-Tag-2-Recompiled) - 铁拳 Tag Tournament 2，Wii U → Linux，静态重编译，MIT，不含游戏文件。★ 9 · 1 fork · 建库于 2026-10-05。

`d2r-mobile` 既不是模拟也不是重编译素材：游戏自己的 aarch64 程序直接执行，只有无法在苹果内核下运行的那部分指令被改写。它的目标是 Switch 版《暗黑破坏神 II：狱火重生》1.0.34.0，与 PC 的 3.3.94012 版对应。真正被逆向的是游戏预期的平台接口面——系统调用、VFS、在 Metal 上重实现的 NVN（着色器离线转换）、音频、输入。仓库不含任何游戏内容，并在 `docs/DERIVED.md` 里逐项列出自己的逆向产出（着色器接口描述、图形 API 函数表、程序内地址）；素材由用户用自己的 dump 通过 `nxdumptool` 取得。

上面四部星之卡比作品覆盖四个任天堂平台，而且都不附带 ROM：`Kirby64Ret/kirby64` 要读者自己把 `baserom.us.z64` 放进树里才能构建，并跟踪自己的反编译百分比；`jiangzhengwenjz/katam` 针对 Game Boy Advance 美版卡带；`doldecomp/kar` 针对 GameCube 光盘，出自做 Super Smash Bros. Melee 反编译的那个组；`Swiftshine/key` 针对 Wii 美版发行 `RK5E01`。`Kirby64Ret/Kirby64Recomp` 把 N64 镜像编译成 Windows、Linux 与 macOS 程序，`ExpansionPak/ModernGekko` 则是这类重编译载入进去的 GameCube 与 Wii 运行时。

Super Mario 64 这条线是一次重建、好几个去处：`n64decomp/sm64` 用读者提供的 `baserom.<VERSION>.z64` 构建出匹配的 ROM；`sm64-port/sm64-port` 是加上原生 Linux 与 Windows 目标的那个 GitHub fork；`sm64pc/sm64ex` 再 fork 一次，加入增强包与 Emill 的高速 3D 渲染器；`coop-deluxe/sm64coopdx` 在它上面接着做已归档的 `djoslin0/sm64ex-coop` 联机 mod。`HarbourMasters/Shipwright`、`2ship2harkinian/2ship2harkinian`、`HarbourMasters/SpaghettiKart` 与 `HarbourMasters/Starship` 属于同一个 libultraship 家族——四部作品、四份 ROM dump、不附带素材。两份反编译自己写明了边界：`zeldaret/tp` "is not, and will not, produce a port"，这段空缺正是 `TwilitRealm/dusklight` 补上的，而 `SMGCommunity/Petari` 直接拒绝"移植"这个标签。完美黑暗的反编译现在住在 GitLab，`n64decomp/perfect_dark` 只作为镜像保留。

### Sony PlayStation

- [open-goal/jak-project](https://github.com/open-goal/jak-project) - Jak & Daxter，PlayStation 2 → Windows、Linux 与 macOS，把游戏代码反编译回 GOAL 语言，并附带一个能为 x86-64 重新编译它的编译器，自述"It shouldn't be emulated, interpreted, or transpiled"，ISC。★ 3,576 · 252 fork · 推送于 2026-10-16。
- [deadinside28/bloodborne_pc](https://github.com/deadinside28/bloodborne_pc) - 血源诅咒，PS4 → Linux，游戏自己的 x86-64 代码跑在"a runtime written for this one game \[that\] replaces the PS4 system libraries"之上，图形转译到 Vulkan，GPL-2.0。★ 3,047 · 728 fork · 推送于 2026-10-15。
- [phoboslab/wipeout-rewrite](https://github.com/phoboslab/wipeout-rewrite) - wipEout，PlayStation → Windows、Linux、macOS 与浏览器，自述"a re-implementation of the 1995 PSX game"，**未声明许可证**。★ 2,977 · 264 fork · 推送于 2026-09-27。
- [FelipePrado0/gow3_pc](https://github.com/FelipePrado0/gow3_pc) - God of War III Remastered，PS4 → Windows 与 Linux，直接执行原版主机二进制的静态重编译，GPL-2.0，C++。★ 2,914 · 187 fork · 建库于 2026-10-08。
- [LoreanXavier/pt-pc](https://github.com/LoreanXavier/pt-pc) - P.T.，PS4 → Windows、Linux 与 macOS，自述"the game logic was rebuilt in C++ from the original's behaviour"，新引擎读原版归档，MIT。★ 1,871 · 122 fork · 推送于 2026-10-16。
- [OpenDriver2/REDRIVER2](https://github.com/OpenDriver2/REDRIVER2) - Driver 2，PlayStation → Windows、Linux 与浏览器，自述"completely disassembled and translated from MIPS back to C… no emulation involved"，MIT。★ 1,405 · 91 fork · 推送于 2026-09-22。
- [Xeeynamo/sotn-decomp](https://github.com/Xeeynamo/sotn-decomp) - 恶魔城X 月下夜想曲，PlayStation、PSP 与世嘉土星，自述"the code compiles byte-for-byte to the same binaries of the game"，AGPL-3.0。★ 1,148 · 111 fork · 推送于 2026-10-17。
- [TeamGDB/Yakumo](https://github.com/TeamGDB/Yakumo) - Monster Hunter Portable 3rd HD Ver.，PSP → Windows、Linux、macOS 与 Android，把 PSP 机器码提前翻译成 C++ 的静态重编译，跑在一套重实现的 PSP 系统软件上，自述"It is not an emulator — there is no interpreter or JIT at the heart of it — and it is not a decompilation"，MIT，不含游戏素材；安装器只接受 PS3 上的原版发行 `NPJB-40001`。★ 456 · 33 fork · 建库于 2026-09-18 · 推送于 2026-10-13。
- [crowded-street/3s-decomp](https://github.com/crowded-street/3s-decomp) - Street Fighter III: 3rd Strike，PlayStation 2，逐字节匹配的反编译，AGPL-3.0。★ 280 · 24 fork · 建库于 2024-09-28 · 最近推送 2026-04-03。
- [fabioap-cpu/Tekken3Recomp](https://github.com/fabioap-cpu/Tekken3Recomp) - 铁拳 3，PlayStation 1 → PC，静态重编译，**未声明许可证**。★ 139 · 3 fork · 建库于 2026-07-31。
- [zFitness/gow3_android](https://github.com/zFitness/gow3_android) - God of War III Remastered，PS4 → Android，自述"Native Android port of God of War III Remastered (PS4)"，GPL-2.0。★ 140 · 12 fork · 建库于 2026-10-14。
- [KIexster/god-of-war-recomp](https://github.com/KIexster/god-of-war-recomp) - God of War，PS2 → Windows PC，静态重编译，GPL-3.0。★ 97 · 4 fork · 建库于 2026-10-05。
- [gasparegas/tkdr-recomp](https://github.com/gasparegas/tkdr-recomp) - 铁拳 便携版（Dark Resurrection），PSP → 原生与 WebAssembly，静态重编译。★ 5 · 建库于 2026-10-11。

PlayStation 这一节背后是四种不同的重建。`Xeeynamo/sotn-decomp` 编译回去的字节和出货二进制一样。`OpenDriver2/REDRIVER2` 把 MIPS 代码翻成 C 并原生运行，不经过模拟。`FelipePrado0/gow3_pc` 与 `deadinside28/bloodborne_pc` 让原版主机代码继续执行，重建的是它底下的那一层系统。`LoreanXavier/pt-pc` 是这组里的例外：P.T. 的逻辑是按观测到的行为在新引擎里重写的，由新引擎去读原版归档，没有任何原版二进制在跑。`TeamGDB/Yakumo` 又是另一种形态：PSP 机器码被提前翻译成 C++ 并编译成宿主机程序，既没有解释器也没有原版二进制在运行，重建的是它底下的 PSP 系统软件。血源诅咒这个移植的 Windows 发行由 fork `Supermedo/bloodborne_pc` 承担，它的贡献者列表里包含上游作者。

### Microsoft Xbox 与 Xbox 360

- [hedge-dev/UnleashedRecomp](https://github.com/hedge-dev/UnleashedRecomp) - Sonic Unleashed，Xbox 360 → Windows 与 Linux，自述光盘构建"created through the process of static recompilation"，GPL-3.0。★ 5,200 · 429 fork · 推送于 2026-06-29。
- [mchughalex/skate3recomp](https://github.com/mchughalex/skate3recomp) - Skate 3，Xbox 360 → Windows、Linux 与 macOS，原生重编译，自带 Direct3D 12 与 Vulkan 渲染器，不做 GPU 模拟，**未声明许可证**。★ 1,640 · 70 fork · 推送于 2026-07-24。
- [OpenCommunityEdition/OpenCE](https://github.com/OpenCommunityEdition/OpenCE) - 光环 战斗进化，Xbox 2342 版 → Windows、Linux、Android 与浏览器，对 Xbox 二进制的反编译，自述"You do not need the Xbox SDK"，CC0-1.0。★ 1,596 · 225 fork · 推送于 2026-10-16。

### MS-DOS、Windows 与 Macintosh

- [OpenRA/OpenRA](https://github.com/OpenRA/OpenRA) - Westwood 的 Command & Conquer / Red Alert / Tiberian Sun 引擎，MS-DOS 与 Windows，净室重写。★ 17,579。
- [OpenRCT2/OpenRCT2](https://github.com/OpenRCT2/OpenRCT2) - 过山车大亨 2，Windows → Windows、macOS、Linux、BSD 与 Android，自述"an open-source re-implementation"，使用原版游戏数据，GPL-3.0。★ 16,445 · 1,947 fork · 推送于 2026-10-14。
- [SFTtech/openage](https://github.com/SFTtech/openage) - 帝国时代 II 引擎，MS-DOS 与 Windows，净室重写。★ 14,509。
- [diasurgical/DevilutionX](https://github.com/diasurgical/DevilutionX) - 暗黑破坏神 与 Hellfire，Windows → Linux、macOS、Android、iOS、Nintendo Switch、PlayStation、Xbox 与 Amiga，把 `diasurgical/devilution` 的重建移植过去并加上自己的引擎工作，Sustainable Use License。★ 9,873 · 1,071 fork · 推送于 2026-10-15。
- [diasurgical/devilution](https://github.com/diasurgical/devilution) - 暗黑破坏神，Windows，自述"a reconstructed form of Diablo's original source code"，从 Climax 的 PlayStation 符号文件与藏在 `DIABDAT.MPQ` 里的调试构建恢复出来，Sustainable Use License。★ 9,004 · 923 fork · 推送于 2025-09-15。
- [OpenTTD/OpenTTD](https://github.com/OpenTTD/OpenTTD) - Transport Tycoon Deluxe 引擎，MS-DOS 与 Windows，净室重写。★ 8,377。
- [OpenMW/openmw](https://github.com/OpenMW/openmw) - 晨风（Morrowind）引擎，Windows，净室重写。★ 6,640。
- [vcmi/vcmi](https://github.com/vcmi/vcmi) - 魔法门之英雄无敌 III 引擎，Windows → Windows、macOS、Linux、Android 与 iOS，重建，需要原版数据文件，GPL-2.0。★ 5,950 · 741 fork · 推送于 2026-10-17。
- [OpenSC2K/OpenSC2K](https://github.com/OpenSC2K/OpenSC2K) - 模拟城市 2000，MS-DOS、Windows 3.x 与 Macintosh → Windows、Linux 与 macOS，自述"an independently written re-implementation"，并把对原版可执行文件的逆向列在自己的方法里，MIT。★ 5,302 · 122 fork · 推送于 2026-10-16。它的 README 声明了 LLM 辅助编码。
- [XProger/OpenLara](https://github.com/XProger/OpenLara) - 古墓丽影 1 引擎，MS-DOS，BSD-2。★ 5,124。
- [k4zmu2a/SpaceCadetPinball](https://github.com/k4zmu2a/SpaceCadetPinball) - 3D Pinball for Windows – Space Cadet，Windows → Windows、Linux 与 macOS，每个子程序都被反编译并转成可编译的 C++，MIT。★ 4,706 · 338 fork · 推送于 2024-08-21。
- [CorsixTH/CorsixTH](https://github.com/CorsixTH/CorsixTH) - 主题医院，MS-DOS 与 Windows → Windows、macOS、Linux 与 BSD，重写，大部分游戏逻辑用 Lua 跑在原版数据上，MIT 风格许可证。★ 4,594 · 437 fork · 推送于 2026-10-13。
- [Interkarma/daggerfall-unity](https://github.com/Interkarma/daggerfall-unity) - 上古卷轴II 匕首谷，MS-DOS → Windows、Linux 与 macOS，Unity 里的重建，读原版归档，MIT。★ 3,527 · 423 fork · 推送于 2026-09-14。
- [ihhub/fheroes2](https://github.com/ihhub/fheroes2) - 魔法门之英雄无敌 II 引擎，MS-DOS 与 Windows → Windows、macOS 与 Linux，自述在原版资源上"written from scratch"的重建，GPL-2.0。★ 3,508 · 506 fork · 推送于 2026-10-16。
- [isledecomp/isle](https://github.com/isledecomp/isle) - LEGO Island，Windows，反编译，用原版 MSVC 4.2 冷构建"reproduces all three retail binaries byte for byte"，LGPL-3.0。★ 3,491 · 147 fork · 推送于 2026-09-18。它只能构建 32 位的 Windows。
- [bvschaik/julius](https://github.com/bvschaik/julius) - 凯撒大帝 III，Windows → Windows、Linux、macOS、PS Vita、Nintendo Switch、Android 与浏览器，重写，自述与原版"the same logic as the original"，存档双向兼容，AGPL-3.0。★ 3,398 · 453 fork · 推送于 2026-09-12。
- [alexbatalov/fallout1-ce](https://github.com/alexbatalov/fallout1-ce) - 辐射，Windows → Windows、Linux、macOS、Android 与 iOS，自述"fully working re-implementation of Fallout, with the same original gameplay"，建立在作者自己逆向出的 `alexbatalov/fallout1-re` 上，Sustainable Use License。★ 2,947 · 239 fork · 推送于 2025-01-15。
- [scummvm/scummvm](https://github.com/scummvm/scummvm) - SCUMM 以及约 250 个其他冒险游戏引擎，MS-DOS、Windows 与 Macintosh，GPL-3.0。★ 2,856。
- [FWGS/xash3d-fwgs](https://github.com/FWGS/xash3d-fwgs) - 半条金的 GoldSrc 引擎，Windows → Linux、Android 与掌机，能跑读者自己那份安装文件的引擎重写，**未声明许可证**。★ 2,851 · 521 fork · 推送于 2026-10-16。
- [in0finite/SanAndreasUnity](https://github.com/in0finite/SanAndreasUnity) - 侠盗猎车手 圣安地列斯，Windows → Windows、Linux、macOS 与 Android，自述"an open source reimplementation of GTA San Andreas game engine in Unity"，读原版数据，MIT。★ 2,648 · 467 fork · 最近推送 2023-06-16。
- [alexbatalov/fallout2-ce](https://github.com/alexbatalov/fallout2-ce) - 辐射 2，Windows → Windows、Linux、macOS、Android 与 iOS，与 `alexbatalov/fallout1-ce` 同一套模式，底子是作者逆向出的 `alexbatalov/fallout2-re`，Sustainable Use License。★ 2,459 · 220 fork · 推送于 2025-02-17。
- [OpenXcom/OpenXcom](https://github.com/OpenXcom/OpenXcom) - UFO: Enemy Unknown 与 Terror from the Deep 引擎，MS-DOS 与 Windows，净室重写。★ 2,232。
- [wheybags/freeablo](https://github.com/wheybags/freeablo) - 暗黑破坏神 1.09，Windows → Windows、Linux 与 macOS，引擎的独立重写，读者要同时提供 `DIABDAT.MPQ` 与 `Diablo.exe`，GPL-3.0。★ 2,170 · 196 fork · 已归档，最近推送 2023-04-13。
- [sdlpal/sdlpal](https://github.com/sdlpal/sdlpal) - 仙剑奇侠传，MS-DOS 与 Windows → Windows、Linux、macOS、Android、iOS、3DS、Wii、PSP 与浏览器，建立在 PAL Research Project 格式文档上的跨平台重写，GPL-3.0。★ 1,980 · 393 fork · 推送于 2026-10-05。
- [OpenLoco/OpenLoco](https://github.com/OpenLoco/OpenLoco) - Chris Sawyer's Locomotion 引擎，MS-DOS，净室重写。★ 1,939。
- [OpenDUNE/OpenDUNE](https://github.com/OpenDUNE/OpenDUNE) - Dune II 引擎，MS-DOS，净室重写。★ 1,695。
- [OpenSAGE/OpenSAGE](https://github.com/OpenSAGE/OpenSAGE) - Command & Conquer: Red Alert 3 与 Generals 引擎，Windows，净室重写。★ 1,649。
- [Try/OpenGothic](https://github.com/Try/OpenGothic) - 哥特王朝 2 乌鸦的复仇，Windows → Windows、Linux 与 macOS，重实现，目标是能吃原版数据与 mod 的客户端，MIT。★ 1,622 · 143 fork · 推送于 2026-10-13。
- [openblack/openblack](https://github.com/openblack/openblack) - 黑与白，Windows → Windows、Linux 与 macOS，自述"open source reimplementation … written in modern C++"，读原版素材，GPL-3.0。★ 1,583 · 104 fork · 推送于 2026-10-17。
- [afritz1/OpenTESArena](https://github.com/afritz1/OpenTESArena) - 上古卷轴 竞技场，MS-DOS → Windows、Linux 与 macOS，自述"replicate all aspects of the original game with a clean-room approach"，MIT。★ 1,431 · 87 fork · 推送于 2026-10-08。
- [doukutsu-rs/doukutsu-rs](https://github.com/doukutsu-rs/doukutsu-rs) - Cave Story，Windows → Windows、macOS、Linux、Android 与 Nintendo Switch，用 Rust 重写引擎，可直接替换出货的可执行文件，MIT。★ 1,313 · 82 fork · 推送于 2026-10-13。
- [NagyD/SDLPoP](https://github.com/NagyD/SDLPoP) - 波斯王子，MS-DOS → Windows、Linux、macOS 与 OS/2，自述"open-source port … based on the disassembly of the DOS version"，GPL-3.0。★ 1,298 · 174 fork · 最近推送 2025-12-24。
- [gemrb/gemrb](https://github.com/gemrb/gemrb) - BioWare 的 Infinity 引擎，也就是博德之门、冰风谷与异域镇魂曲背后的那一套，Windows → Windows、Linux、macOS、Android、iOS 与各主机，从数据格式入手的重写，GPL-2.0。★ 1,262 · 227 fork · 推送于 2026-10-12。
- [yvt/openspades](https://github.com/yvt/openspades) - Ace of Spades 0.75，Windows → Linux、Windows 与 macOS，兼容客户端：体素引擎与服务端协议都按观测重写，GPL-3.0。★ 1,246 · 233 fork · 最近推送 2024-06-06。
- [dethrace-labs/dethrace](https://github.com/dethrace-labs/dethrace) - Carmageddon，MS-DOS → Windows、Linux 与 macOS，自述"replacing the original assembly code with equivalent C code, function by function"，起点是 Splat Pack 光盘上留下的 Watcom 符号文件，GPL-3.0。★ 1,219 · 97 fork · 推送于 2026-10-17。
- [xoreos/xoreos](https://github.com/xoreos/xoreos) - BioWare 的 Aurora 引擎及其衍生作品：无冬之夜、旧共和国武士、翡翠帝国、巫师，Windows 与 Xbox → Windows、macOS 与 Linux，资源格式与脚本格式的重写，玩法部分仍不完整，GPL-3.0。★ 1,184 · 137 fork · 推送于 2026-09-04。
- [TheForceEngine/TheForceEngine](https://github.com/TheForceEngine/TheForceEngine) - 星球大战 黑暗力量，MS-DOS → Windows、Linux 与 macOS，自述"reverse engineer and rebuild the Jedi Engine for modern systems"，GPL-2.0。★ 1,165 · 91 fork · 推送于 2026-10-12。
- [RSDKModding/RSDKv4-Decompilation](https://github.com/RSDKModding/RSDKv4-Decompilation) - 索尼克 1 与索尼克 2（2013），Retro Engine v4，Windows、Nintendo Switch 与 Android 发行，自述"a complete decompilation"，没有官方放出的素材就跑不起来，自定义许可证。★ 1,145 · 260 fork · 推送于 2026-09-06。
- [dpjudas/SurrealEngine](https://github.com/dpjudas/SurrealEngine) - Unreal Engine 1，Windows → Windows、macOS 与 Linux，自述是一个"aims to reimplement Unreal Engine 1"的项目，读读者自己那份 Unreal、Unreal Tournament 与 Deus Ex 的原版安装，zlib 风格许可证。★ 1,116 · 59 fork · 推送于 2026-10-17。
- [collinsmith/riiablo](https://github.com/collinsmith/riiablo) - 暗黑破坏神 II，Windows → PC 与 Android，用 Java 与 LibGDX 在原版 MPQ 素材上"from scratch"重建，Apache-2.0。★ 1,104 · 123 fork · 最近推送 2025-01-13。README 写明还不能玩。
- [gta-reversed/gta-reversed](https://github.com/gta-reversed/gta-reversed) - 侠盗猎车手 圣安地列斯，Windows，把出货的 1.0 可执行文件"function by function"重写，在加载时替换游戏自己的例程，**未声明许可证**。★ 1,073 · 253 fork · 推送于 2026-10-16。README 估计"about 50-60% of the code is done"。
- [isledecomp/isle-portable](https://github.com/isledecomp/isle-portable) - LEGO Island，Windows 9x → Windows、macOS、Linux、iOS、Android、Nintendo Switch、PS Vita 与 Xbox One，把 `isledecomp/isle` 的 C++ 搬到现代宿主，办法是换掉只能跑 Windows 的那些库，LGPL-3.0。★ 1,071 · 100 fork · 推送于 2026-10-15。
- [vladtrc/iw4L](https://github.com/vladtrc/iw4L) - 使命召唤 现代战争 2（2009），Windows → Windows、Linux 与 macOS，在读者自己的安装之上用 Rust 重写运行时，Apache-2.0。★ 1,069 · 130 fork · 推送于 2026-10-16。它的 README 写明"This whole project is written by an LLM."
- [dkfans/keeperfx](https://github.com/dkfans/keeperfx) - 地下城守护者，Windows → Windows，自述"the whole codebase of Dungeon Keeper is remade"，起点是对原版可执行文件的反编译，之后一路重写，GPL-2.0。★ 1,020 · 133 fork · 推送于 2026-10-16。
- [LostArtefacts/TRX](https://github.com/LostArtefacts/TRX) - 古墓丽影 1、2、3，MS-DOS 与 Windows → Windows 与 Linux，重实现是"through decompilation"得来的，保留每一代引擎各自的机制，GPL-3.0。★ 1,009 · 72 fork · 推送于 2026-10-16。
- [lethal-guitar/RigelEngine](https://github.com/lethal-guitar/RigelEngine) - 毁灭公爵 II，MS-DOS → Windows、Linux、macOS、Steam Deck 与树莓派，自述"based on reverse engineering (specifically, disassembly of the original binaries)"，GPL-2.0。★ 1,007 · 69 fork · 推送于 2026-09-28。
- [TheAssemblyArmada/Thyme](https://github.com/TheAssemblyArmada/Thyme) - Three's Company 全动态影像游戏的引擎，MS-DOS，净室重写。★ 696。
- [exult/exult](https://github.com/exult/exult) - 创世纪 VII 引擎，MS-DOS 与 Macintosh，GPL-2.0。★ 693。
- [opentyrian/opentyrian](https://github.com/opentyrian/opentyrian) - Tyrian 引擎，MS-DOS，GPL-2.0。★ 586。
- [nxengine/nxengine-evo](https://github.com/nxengine/nxengine-evo) - Cave Story 引擎，Windows，净室重写。★ 551。
- [AlisterT/openjazz](https://github.com/AlisterT/openjazz) - Jazz Jackrabbit 引擎，MS-DOS，GPL-2.0。★ 409。
- [mytbk/rich4](https://github.com/mytbk/rich4) - 大富翁4，Windows，反汇编之后改用 MinGW 与 `msvcrt` 重新链接成可运行的 `rich4.exe`，GPL-3.0。★ 146 · 20 fork · 建库于 2018-09-27 · 推送于 2026-10-08。
- [Wargus/war1gus](https://github.com/Wargus/war1gus) - 把 WarCraft 1 做成建立在 Wargus 上的即时战略引擎，MS-DOS 与 Windows，GPL-2.0。★ 134。
- [jhaizhou-ops/sts2-ios](https://github.com/jhaizhou-ops/sts2-ios) - 杀戮尖塔 2，Steam 的 Windows/Linux 构建 → iOS，"自带 Steam 副本"。★ 63 · 建库于 2026-07-15。
- [N0zoM1z0/dx-ball](https://github.com/N0zoM1z0/dx-ball) - DX-Ball，MS-DOS：1996 年的共享软件 `DXBALL.EXE` 重建为 C 与 C++，自述"完全重建仍在进行"。★ 61。有帖子声称 Steam 版能跑，仓库里并没有这么写。
- [N0zoM1z0/th04](https://github.com/N0zoM1z0/th04) - 东方 4，Windows：`MAIN.EXE` 重建为 C++，自述与原程序有 2,139 个逐字节匹配。★ 33。
- [lhr0909/richman4-remastered](https://github.com/lhr0909/richman4-remastered) - 大富翁4，Windows → macOS、Android、iOS，引擎按 `mytbk/rich4` 公开的反汇编逐条重写，不是净室，GPL-3.0。★ 9 · 3 fork · 建库与推送于 2026-10-06。它的 NOTICE 把编译出的 APK 限制在构建者自己的设备上。
- [kichikuou/xsystem4](https://github.com/kichikuou/xsystem4) - AliceSoft System 4 视觉小说，把 Windows 上的作品重建到类 unix 系统，GPL-2.0。★ 3 · 推送于 2026-10-15。

`xsystem4` 带一份公开的 `game_compatibility.md`：66 部作品，41 支持、18 未知、7 不支持，其中 戦国ランス / Sengoku Rance、Rance VI、Rance 01、Rance 02 标为支持，ランス・クエスト 标为不支持。同一作者还维护 `xsystem35-sdl2`、`xsystem4-android`、`xsys35c`（见下文「格式、文件系统与协议」）、`system3-sdl2`、`sys4lang` 和 `libsys4`。

`mytbk/rich4` 把自己的目标钉得很死：`rich4.exe` v3.11、588 KiB，SHA-256 `5a90aee28ee5f7a5c3ba5cb935c9e55751a529c25fcd91208748a66293569550`。2018 年三个月的工作做出了数据文件的解包算法与存档格式；2021 年借助 `mytbk/r2dumpbin` 把可执行文件变成可重新链接的汇编；2025 年 Watcom C 运行时被剥离到 MinGW 与 `msvcrt` 能链接出可运行的 `rich4.exe`。带注释的拆分放在 Codeberg 上的 `vimacs/rich4_asm`，`tytannial/rich4-re` 是同一部作品的第三个尝试。`lhr0909/richman4-remastered` 在自己的致谢里写明：每条规则、每个界面与动画时序都是照着那份公开反汇编重写的；素材来自 Steam 上架的《大富翁4》。

暗黑破坏神这条线是一个起点、三个去处：`diasurgical/devilution` 从 Climax 的 PlayStation 移植留下的符号文件、以及藏在 `DIABDAT.MPQ` 里名为 `D1221A.MPQ` 的调试构建，重建出 1996 年的代码，并且刻意保留原版的 bug；`diasurgical/DevilutionX` 是这份重建的 SDL 移植，覆盖十几个平台；`d07RiV/diabloweb` 把 fork 过的 devilution 构建成浏览器里跑的 WebAssembly。三者的许可证都是 Sustainable Use License，也就是 GitHub 报成 `NOASSERTION` 的非商用许可证。凯撒大帝 III 也是同样的 fork 关系：`Keriew/augustus` 是 `bvschaik/julius` 的 fork，加了玩法改动，代价是放弃 Julius 一直坚持的双向存档兼容。辐射社区版写明了自己的方法链——每一个都建立在作者自己匹配出来的逆向底子上，而不是 Interplay 或 Bethesda 放出的源码。

### 移动端

- [JoppieToppie/Galaxy-on-Fire-2-Unity-Remake](https://github.com/JoppieToppie/Galaxy-on-Fire-2-Unity-Remake) - Galaxy on Fire 2，Android 与 iOS → Windows、Linux 与 Android，Unity 重制，游戏逻辑自述"ported from the decompiled game code"，原版素材随仓库内置，LICENSE.md 是 Apache-2.0 全文而 GitHub 报成 `NOASSERTION`。★ 145 · 16 fork · 推送于 2026-10-17。

## 应用程序

不是游戏、但重建到能吃原版内容的程序。

- [ruffle-rs/ruffle](https://github.com/ruffle-rs/ruffle) - Adobe Flash Player，AVM2 加渲染，Rust，净室重写。★ 18,695。
- [storytold/wordcraft](https://github.com/storytold/wordcraft) - 面向 Windows 与 Mac 的 Microsoft Word，直接吃原版文档格式，Apache-2.0，Rust。★ 13,694。它的 README 写着"Clean-room: built from public specifications and observation, with every asset original or openly licensed"，因此按净室成果归档。
- [soyrochus/mucrab](https://github.com/soyrochus/mucrab) - muCommander，一个 Java 桌面应用按观测到的行为用 Rust 重写，附测试报告。★ 1。

## 运行时与兼容层

程序所预期的那一层平台被重建或被垫片化：一个 API、一个固件接口、一个运行时、一台模拟器，或者让某部作品在新宿主上跑起来的补丁。

- [doitsujin/dxvk](https://github.com/doitsujin/dxvk) - 把 Direct3D 9/10/11 转译到 Vulkan，供 Windows 与 Wine 使用，Zlib。★ 18,305。
- [reactos/reactos](https://github.com/reactos/reactos) - x86 上的 Windows NT，由黑盒观测得出，GPL-2.0。★ 18,235。
- [azahar-emu/azahar](https://github.com/azahar-emu/azahar) - Nintendo 3DS，在 Windows、Linux 与 macOS 上模拟；Citra 的活跃后继。★ 8,377 · 建库于 2024-03-04。
- [focus-creative-games/hybridclr](https://github.com/focus-creative-games/hybridclr) - iOS、Android 与桌面上的 Unity IL2CPP 托管运行时，MIT。★ 7,995。
- [AsahiLinux/m1n1](https://github.com/AsahiLinux/m1n1) - Apple 芯片上的引导与固件接口，GPL-2.0。★ 4,268。
- [HansKristian-Work/vkd3d-proton](https://github.com/HansKristian-Work/vkd3d-proton) - 把 Direct3D 12 转译到 Vulkan，跑在 Wine 与 Proton 下，LGPL-2.1。★ 3,005。
- [ExpansionPak/ModernGekko](https://github.com/ExpansionPak/ModernGekko) - GameCube 与 Wii 重编译作品载入进去的运行时，以 Dolphin 代码库为基础，并带一套 `mod.so`、`mod.dll`、`mod.dylib` 包的 code-mod ABI，GPL-3.0。★ 171 · 18 fork · 建库于 2026-06-25 · 推送于 2026-09-17。
- [yuzuatri/Sengoku-Rance-Deck-Fix](https://github.com/yuzuatri/Sengoku-Rance-Deck-Fix) - 战国ランス跑在 Linux 的 Proton 下：下面那个 Wine 代码页问题的"改可执行文件"解法——校验版本、SHA-256 门禁、两个偏移各改四字节、保留备份、可选把用户自备的 `simhei.ttf` 装进游戏的 Proton prefix。★ 6 · MIT · 建库于 2026-10-02。

Wine 的代码页缺口：Wine 10.0 自带 76 个 `.nls` 代码页表，GB18030（`c_54936.nls`）不在其中，所以一个在进程初始化时调用 `MultiByteToWideChar(54936, …)` 的简体中文作品会不开窗口地卡死。两种修法：把缺的表补进 prefix（在 Proton 下必须放进 `syswow64`，因为 Wine 自己会把 32 位进程对 `system32` 的查询重定向），或者改可执行文件让它请求 CP936。⚠ *换成 GBK 表都会丢掉 GB18030 的 4 字节序列，因此两条路都是近似；两者的实际区别是侵入程度，不是正确性。*

## 格式、文件系统与协议

靠观测重实现的二进制格式、文件系统与网络协议，不附带原版实现。

- [librespot-org/librespot](https://github.com/librespot-org/librespot) - Spotify Connect 与播放控制协议，面向 Linux 等平台，MIT。★ 7,299。
- [sgan81/apfs-fuse](https://github.com/sgan81/apfs-fuse) - Apple File System 的读取路径，Linux 与 macOS，GPL-2.0；已停更。★ 2,161。
- [LibreDWG/libredwg](https://github.com/LibreDWG/libredwg) - AutoCAD DWG，GPL-3.0；这是官方 GitHub 镜像。★ 1,627。
- [tuxera/ntfs-3g](https://github.com/tuxera/ntfs-3g) - Linux 上的 NTFS 读写，GPL-2.0。★ 1,521。
- [f4pga/prjxray](https://github.com/f4pga/prjxray) - Xilinx 7 系列 FPGA 的比特流格式，ISC。★ 925。
- [linux-apfs/linux-apfs-rw](https://github.com/linux-apfs/linux-apfs-rw) - Linux 内核里带写入支持的 APFS，GPL-2.0。★ 804。
- [kichikuou/xsys35c](https://github.com/kichikuou/xsys35c) - DOS 与 Windows 上的 AliceSoft System 3.x 脚本字节码：同一套格式的编译器与反编译器，GPL-2.0。★ 40 · 推送于 2026-10-13。

LibreDWG 是 GPL-3，与本应采用它的 LGPL 下游不兼容：一个技术上已经完成的格式重建，自己的生态却吸收不了。

## 相关清单

本清单只收成果，下面这些收工具或撒更大的网。

- [alphaSeclab/awesome-reverse-engineering](https://github.com/alphaSeclab/awesome-reverse-engineering) - 覆盖 Windows / Linux / macOS 的逆向资源，以工具为主。★ 5,131。
- [user1342/Awesome-Android-Reverse-Engineering](https://github.com/user1342/Awesome-Android-Reverse-Engineering) - Android 逆向的训练、工具与资源。★ 2,739。
- [morluto/awesome-reverse-engineering](https://github.com/morluto/awesome-reverse-engineering) - 面向二进制文件的逆向工具与学习资源；正是本清单刻意不做的那份工具清单。★ 631。
- [SubmitGame/awesome-decomp-games](https://github.com/SubmitGame/awesome-decomp-games) - 自动刷新、带打分的反编译/重编译/逆向游戏清单：1,829 部作品共 2,118 个项目，每天从 `data/games.json` 重新生成。★ 1,039 · CC0 · 建库于 2026-10-09。它靠自动扩覆盖并给可玩性打分。

## 参与

新增条目的规则见 [CONTRIBUTING.md](CONTRIBUTING.md)，清单如何分类、核验与刷新写在 `AGENTS.md`。决定大多数 PR 的两条：**按它重建的是哪一类软件归档，写明原始平台与重建方法**，"这个项目很牛，值得看"不构成一条条目；**核不实的说法加 ⚠，或者不写**——写出你真的读过的一手来源，或者写出你没读到什么。
