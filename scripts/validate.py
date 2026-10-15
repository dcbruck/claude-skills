#!/usr/bin/env python3
"""Checks every skill folder before it ships: frontmatter present, name matches
the folder, description within the 1024-character limit, and plugin JSON parses."""
import json, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
errors = []

for skill in sorted((root / "skills").iterdir()):
    if not skill.is_dir():
        continue
    md = skill / "SKILL.md"
    if not md.exists():
        errors.append(f"{skill.name}: missing SKILL.md")
        continue
    text = md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{skill.name}: no YAML frontmatter")
        continue
    fm = m.group(1)
    name = re.search(r"^name:\s*\"?([^\"\n]+)\"?\s*$", fm, re.M)
    desc = re.search(r"^description:\s*(.+)$", fm, re.M)
    if not name or name.group(1).strip() != skill.name:
        errors.append(f"{skill.name}: frontmatter name must equal folder name")
    if not desc:
        errors.append(f"{skill.name}: missing description")
    else:
        d = desc.group(1).strip().strip('"')
        if len(d) > 1024:
            errors.append(f"{skill.name}: description is {len(d)} chars (max 1024)")
    if not (skill / "README.md").exists():
        errors.append(f"{skill.name}: missing README.md")

for f in (root / ".claude-plugin").glob("*.json"):
    try:
        json.loads(f.read_text())
    except Exception as e:
        errors.append(f"{f.name}: invalid JSON ({e})")

# Version sync. Claude Code only ships an update to existing installs when the
# plugin version changes, so plugin.json, the marketplace entry, and the newest
# CHANGELOG heading must all carry the same number.
try:
    plugin_v = json.loads((root / ".claude-plugin/plugin.json").read_text())["version"]
    market = json.loads((root / ".claude-plugin/marketplace.json").read_text())
    market_v = next(p.get("version") for p in market["plugins"] if p["name"] == "drewbrucker-skills")
    log = re.search(r"^## v(\S+)", (root / "CHANGELOG.md").read_text(), re.M)
    log_v = log.group(1) if log else None
    if not (plugin_v == market_v == log_v):
        errors.append(f"version mismatch: plugin.json {plugin_v}, marketplace.json {market_v}, CHANGELOG {log_v}")
    tag = sys.argv[1] if len(sys.argv) > 1 else None
    if tag and tag != f"v{plugin_v}":
        errors.append(f"tag {tag} does not match plugin version v{plugin_v}")
except Exception as e:
    errors.append(f"version check failed ({e})")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("all skills valid")
