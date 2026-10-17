import json, subprocess, sys, time, csv, os

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
MEAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "measurement")
OUT = os.path.join(MEAS, "re_gh.tsv")

QUERIES = [
    ("topic-reverse-engineering", "topic:reverse-engineering"),
    ("topic-decompilation", "topic:decompilation"),
    ("topic-reimplementation", "topic:reimplementation"),
    ("clean-room", '"clean-room" reimplementation'),
    ("engine-reimpl", "game engine reimplementation"),
    ("decomp-project", "decompilation matching"),
    ("linux-port", "windows game linux port"),
    ("trainer", "trainer cheat table single-player"),
    ("wine-nls", "wine codepage nls"),
    ("asset-extract", "asset extractor unpackpak"),
]


def gh(q, per=50):
    import urllib.parse
    url = ("https://api.github.com/search/repositories?q=" + urllib.parse.quote(q) +
           f"&per_page={per}&sort=stars&order=desc")
    p = subprocess.run(["curl", "-s", "--compressed", "-m", "40", "-H", f"User-Agent: {UA}",
                        "-H", "Accept: application/vnd.github+json", url],
                       capture_output=True, text=True)
    try:
        return json.loads(p.stdout)
    except Exception:
        return {"_err": p.stdout[:200]}


rows, seen = [], set()
for label, q in QUERIES:
    d = gh(q)
    items = d.get("items") or []
    print(f"{label:24s} total_count={d.get('total_count')} returned={len(items)}"
          + (f" ERR={d.get('_err') or d.get('message')}" if not items else ""))
    for r in items:
        fn = r.get("full_name")
        if fn in seen:
            continue
        seen.add(fn)
        lic = (r.get("license") or {}).get("spdx_id") or "NONE"
        rows.append({
            "cat": label, "repo": fn, "stars": r.get("stargazers_count", 0),
            "forks": r.get("forks_count", 0), "pushed": (r.get("pushed_at") or "")[:10],
            "archived": "YES" if r.get("archived") else "", "license": lic,
            "lang": r.get("language") or "", "topics": ";".join(r.get("topics") or []),
            "desc": (r.get("description") or "").replace("\t", " ")[:160],
        })
    time.sleep(7)

os.makedirs(MEAS, exist_ok=True)
rows.sort(key=lambda r: -r["stars"])
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
    w.writeheader()
    w.writerows(rows)
print(f"\nwrote {len(rows)} rows -> {OUT}")

alive = [r for r in rows if not r["archived"] and r["pushed"] >= "2025-01-01"]
print(f"active (pushed 2025+, not archived): {len(alive)}/{len(rows)}")
print("\ntop 45 by stars:")
for r in rows[:45]:
    print(f"{r['stars']:>8,} {r['pushed']} {'ARCH' if r['archived'] else '    '} {r['license']:>12} "
          f"{r['lang'] or '-':>10}  {r['repo']:<34} {r['desc'][:58]}")
