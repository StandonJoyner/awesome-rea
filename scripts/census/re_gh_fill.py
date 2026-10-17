import json, subprocess, sys, time, csv, os, urllib.parse

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
HERE = os.path.dirname(os.path.abspath(__file__))
TSV = os.path.join(HERE, "..", "..", "data", "measurement", "re_gh_curated.tsv")
PX = ["-x", "http://127.0.0.1:7892"]

TOKENS = ["system4", "alance", "rance", "nekopara", "illusion", "decomp", "recomp",
          "clean-room", "protocol", "extractor", "unpackpak", "il2cpp", "gamemaker",
          "undertale", "dxvk", "vkd3d", "prjtrellis", "me_cleaner", "openrgb", "monado",
          "apfs", "librespot", "gambatte", "citra", "yuzu", "pcsx2", "cheat-engine",
          "sfall", "openlierox", "openspades", "retrosoftonic", "disassembly",
          "nxengine", "sm64pc", "kkrieger", "privateer", "stardust", "freescout-help-desk"]

rows = list(csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t"))
seen = {r["repo"].lower() for r in rows}
cols = list(rows[0].keys())
added = 0


def gh(q, per=8):
    url = "https://api.github.com/search/repositories?q=" + urllib.parse.quote(q) + \
          f"&per_page={per}&sort=stars&order=desc"
    p = subprocess.run(["curl", "-s"] + PX + ["--compressed", "-m", "45",
                       "-H", f"User-Agent: {UA}", "-H", "Accept: application/vnd.github+json", url],
                       capture_output=True, text=True)
    try:
        return json.loads(p.stdout)
    except Exception:
        return {"message": "parse-fail"}


for t in TOKENS:
    d = gh(t)
    items = d.get("items") or []
    print(f"[{t:20s}] {len(items)} {('ERR ' + str(d.get('message'))[:60]) if not items else ''}", flush=True)
    for it in items[:6]:
        fn = it.get("full_name", "")
        if not fn or fn.lower() in seen:
            continue
        seen.add(fn.lower())
        rows.append({
            "cat": "fill:" + t, "repo": fn, "stars": str(it.get("stargazers_count", 0)),
            "forks": str(it.get("forks_count", 0)), "watchers": "",
            "created": (it.get("created_at") or "")[:10], "pushed": (it.get("pushed_at") or "")[:10],
            "archived": "YES" if it.get("archived") else "",
            "license": (it.get("license") or {}).get("spdx_id") or "NONE",
            "lang": it.get("language") or "",
            "desc": (it.get("description") or "").replace("\t", " ")[:170],
        })
        added += 1
    with open(TSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    time.sleep(6.4)

print(f"\nadded={added} total={len(rows)}")
