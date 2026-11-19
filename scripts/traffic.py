#!/usr/bin/env python3
"""Archives GitHub traffic and release downloads so they outlast GitHub's 14-day window.

Usage: python3 scripts/traffic.py OUT_DIR

Env:
  REPO           owner/name (set by the workflow)
  TRAFFIC_TOKEN  fine-grained token with Administration: read on this repo.
                 Traffic needs it; without it only release downloads are recorded.
  GH_TOKEN       any token, used for release download counts.

Writes CSVs plus a README.md summary into OUT_DIR. Safe to run any number of times
a day: daily rows are replaced, never duplicated."""
import csv, datetime, json, os, pathlib, re, sys, urllib.error, urllib.request

REPO = os.environ.get("REPO", "dcbruck/claude-skills")
API = f"https://api.github.com/repos/{REPO}"
TODAY = datetime.date.today().isoformat()
out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "traffic-data")
out.mkdir(parents=True, exist_ok=True)


def get(path, token):
    req = urllib.request.Request(API + path, headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        **({"Authorization": f"Bearer {token}"} if token else {}),
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def read(name):
    f = out / name
    if not f.exists():
        return []
    with f.open(newline="") as fh:
        return list(csv.DictReader(fh))


def write(name, fields, rows):
    with (out / name).open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def upsert_daily(name, items):
    """GitHub returns the last 14 days. The newest day is partial, so a fresh value
    always replaces the stored one for the same date."""
    rows = {r["date"]: r for r in read(name)}
    for it in items:
        d = it["timestamp"][:10]
        rows[d] = {"date": d, "count": it["count"], "uniques": it["uniques"]}
    write(name, ["date", "count", "uniques"], [rows[k] for k in sorted(rows)])


def replace_snapshot(name, fields, new_rows):
    rows = [r for r in read(name) if r["snapshot"] != TODAY] + new_rows
    rows.sort(key=lambda r: tuple(str(r[f]) for f in fields[:2]))
    write(name, fields, rows)


# 1. Traffic (needs TRAFFIC_TOKEN)
traffic_token = os.environ.get("TRAFFIC_TOKEN")
traffic_ok = False
if traffic_token:
    try:
        upsert_daily("clones.csv", get("/traffic/clones?per=day", traffic_token)["clones"])
        upsert_daily("views.csv", get("/traffic/views?per=day", traffic_token)["views"])
        replace_snapshot("referrers.csv", ["snapshot", "referrer", "count", "uniques"], [
            {"snapshot": TODAY, "referrer": r["referrer"], "count": r["count"], "uniques": r["uniques"]}
            for r in get("/traffic/popular/referrers", traffic_token)])
        replace_snapshot("paths.csv", ["snapshot", "path", "count", "uniques"], [
            {"snapshot": TODAY, "path": p["path"], "count": p["count"], "uniques": p["uniques"]}
            for p in get("/traffic/popular/paths", traffic_token)])
        traffic_ok = True
    except urllib.error.HTTPError as e:
        print(f"::warning::Traffic API returned {e.code}. Check that TRAFFIC_TOKEN has Administration: read on {REPO}.")
else:
    print("::warning::TRAFFIC_TOKEN secret is not set. Recording release downloads only.")

# 2. Release downloads (public, never reset)
releases = get("/releases?per_page=100", os.environ.get("GH_TOKEN"))
replace_snapshot("downloads.csv", ["snapshot", "tag", "asset", "downloads"], [
    {"snapshot": TODAY, "tag": rel["tag_name"], "asset": a["name"], "downloads": a["download_count"]}
    for rel in releases for a in rel["assets"]])

# 3. Summary
clones, views = read("clones.csv"), read("views.csv")
by_asset = {}
for r in read("downloads.csv"):
    if r["snapshot"] == TODAY:
        by_asset[r["asset"]] = by_asset.get(r["asset"], 0) + int(r["downloads"])
latest_paths = [r for r in read("paths.csv") if r["snapshot"] == TODAY]
skill_views = {}
for r in latest_paths:
    m = re.search(r"/skills/([^/]+)", r["path"])
    if m:
        skill_views[m.group(1)] = skill_views.get(m.group(1), 0) + int(r["count"])

lines = [f"# Traffic archive for {REPO}", "", f"Last updated {TODAY}.", ""]
if clones:
    lines += [
        f"**Clones since {clones[0]['date']}:** {sum(int(r['count']) for r in clones)}. "
        "Each `claude plugin marketplace add` is one clone.",
        f"**Views since {views[0]['date'] if views else '-'}:** {sum(int(r['count']) for r in views)}.",
        "",
        "Daily uniques are kept in the CSVs. They can't be added across days, because the same person counts once per day.",
        "",
    ]
elif not traffic_ok:
    lines += ["Traffic isn't recorded yet. Add the `TRAFFIC_TOKEN` secret to start.", ""]
lines += ["## Release zip downloads (all releases, all time)", "", "| Zip | Downloads |", "|---|---|"]
lines += [f"| {k} | {v} |" for k, v in sorted(by_asset.items(), key=lambda kv: (-kv[1], kv[0]))]
lines += ["", f"**Total:** {sum(by_asset.values())}", ""]
if skill_views:
    lines += ["## Skill page views (rolling 14 days, top paths only)", "", "| Skill | Views |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(skill_views.items(), key=lambda kv: -kv[1])]
    lines.append("")
(out / "README.md").write_text("\n".join(lines))
print("\n".join(lines))
