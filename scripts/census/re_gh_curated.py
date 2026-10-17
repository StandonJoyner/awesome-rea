import json, subprocess, sys, time, csv, os, urllib.parse

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
HERE = os.path.dirname(os.path.abspath(__file__))
MEAS = os.path.join(HERE, "..", "..", "data", "measurement")
OUT = os.path.join(MEAS, "re_gh_curated.tsv")

# confident owner/name, queried in chunks of 8 (GitHub truncates long repo: OR-lists)
CANON = [
    "openmw/openmw", "OpenRCT2/OpenRCT2", "OpenTTD/OpenTTD", "OpenRA/OpenRA",
    "scummvm/scummvm", "SFTtech/openage", "exult/exult", "XProger/OpenLara",
    "OpenDUNE/OpenDUNE", "zeldaret/oot", "zeldaret/mm", "zeldaret/tww",
    "zeldaret/altt", "RPCS3/rpcs3", "DolphinEmulator/Dolphin", "melonDS/melonDS",
    "byuu/bsnes", "hrydgard/ppsspp", "AsahiLinux/m1n1", "f4pga/prjxray",
    "reactos/reactos", "ruffle-rs/ruffle", "tuxera/ntfs-3g", "LibreVR/Revive",
    "xenia-project/xenia", "OpenRW/OpenRW", "xPaw/ReDev", "morluto/rea",
    "mrexodia/ida-pro-mcp", "rehan-remade/universal-modder", "Dryxio/reagent",
    "i12bp8/decomp.wtf", "tangosdev/sm64ds-decomp", "MG1937/ASC",
    "OpenLoco/OpenLoco", "opentyrian/opentyrian", "doitsdx/DXVK", "ValveSoftware/source-sdk-2013",
]

# single-token searches: GitHub ANDs every free term, so one token per query
TOKENS = [
    "openjazz", "openxcom", "deepdark", "opensage", "freescout", "privateer",
    "kkrieger", "nxengine", "sm64pc", "retrosoftonic", "disassembly", "dxvk",
    "vkd3d", "prjtrellis", "me_cleaner", "openrgb", "monado", "apfs", "librespot",
    "gambatte", "citra", "yuzu", "pcsx2", "cheat-engine", "sfall", "openlierox",
    "openspades", "stardust", "war1gus", "freespace", "system4", "alance",
    "rance", "nekopara", "decomp", "recomp", "clean-room", "protocol",
    "extractor", "unpackpak", "il2cpp", "gamemaker", "undertale",
]

rows, seen = [], set()


def gh(q, per=50):
    url = "https://api.github.com/search/repositories?q=" + urllib.parse.quote(q) + \
          f"&per_page={per}&sort=stars&order=desc"
    p = subprocess.run(["curl", "-s", "--compressed", "-m", "45", "-H", f"User-Agent: {UA}",
                        "-H", "Accept: application/vnd.github+json", url],
                       capture_output=True, text=True)
    try:
        d = json.loads(p.stdout)
    except Exception:
        return {"message": "parse-fail"}
    return d if isinstance(d, dict) else {"message": "not-dict"}


def ingest(item, cat, n=8):
    fn = item.get("full_name")
    if not fn or fn.lower() in seen:
        return
    seen.add(fn.lower())
    rows.append({
        "cat": cat, "repo": fn, "stars": item.get("stargazers_count", 0),
        "forks": item.get("forks_count", 0), "watchers": item.get("subscribers_count", ""),
        "created": (item.get("created_at") or "")[:10], "pushed": (item.get("pushed_at") or "")[:10],
        "archived": "YES" if item.get("archived") else "",
        "license": (item.get("license") or {}).get("spdx_id") or "NONE",
        "lang": item.get("language") or "",
        "desc": (item.get("description") or "").replace("\t", " ")[:170],
    })


def flush(rows):
    os.makedirs(MEAS, exist_ok=True)
    rows.sort(key=lambda r: -r["stars"])
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(rows)


found = set()
for i in range(0, len(CANON), 8):
    chunk = CANON[i:i + 8]
    d = gh(" ".join("repo:" + c for c in chunk), per=40)
    items = d.get("items") or []
    for it in items:
        found.add(it["full_name"].lower())
        ingest(it, "canon")
    print(f"[canon {i//8}] asked={len(chunk)} got={len(items)} miss={[c for c in chunk if c.lower() not in found]}", flush=True)
    time.sleep(7)

for t in TOKENS:
    d = gh(t, per=8)
    items = d.get("items") or []
    print(f"[{t:14s}] {len(items)} {d.get('message') or ''}", flush=True)
    for it in items[:6]:
        ingest(it, "tok:" + t)
    flush(rows)
    time.sleep(6.6)

print(f"\nwrote {len(rows)} -> {OUT}")
