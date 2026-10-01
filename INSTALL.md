# Install

Every skill is one folder under `skills/` with a `SKILL.md` inside. Pick the route that matches where you use Claude.

## Claude Code: all twelve as a plugin

```bash
claude plugin marketplace add dcbruck/claude-skills
claude plugin install drewbrucker-skills@drewbrucker-claude-skills
```

Skills install namespaced as `drewbrucker-skills:triage` and so on. Type `/triage` (or the namespaced form if you have a collision) in any session.

To update later:

```bash
claude plugin marketplace update drewbrucker-claude-skills
claude plugin update drewbrucker-skills@drewbrucker-claude-skills
```

## Claude Code: one skill, no plugin

Copy the folder into your personal skills directory (all projects) or a project's `.claude/skills/` (that project only):

```bash
# personal
cp -r skills/triage ~/.claude/skills/triage

# one project
cp -r skills/triage /path/to/project/.claude/skills/triage
```

Restart the session. The skill shows up as `/triage`.

## Claude desktop app and claude.ai

Fastest route: download the skill's zip from the [latest release](https://github.com/dcbruck/claude-skills/releases/latest) and skip to step 2. Every release ships one ready-to-upload zip per skill.

1. Zip the skill folder so the zip contains the folder itself, not just its files:
   ```bash
   cd skills && zip -r ../triage.zip triage
   ```
2. Desktop app: **Settings > Capabilities**, add a skill, upload the zip.
   Web: **Settings > Customize > Skills**, upload the zip.
3. Type `/triage` in any chat.

Skills uploaded this way are per-account and do not sync back to Claude Code.

## After installing

Some skills read or write files. Each one says which in its `## Setup` section. Defaults:

| Path | Used by |
|---|---|
| `voice-profile.md` | post, ghost, fleet, mine (optional) |
| `kill-list.md` | post, ghost, fleet |
| `.skills-data/` | beastmode, triage, adopt, post, mine, fleet, youtube, redline (logs, ledgers, libraries) |

Start the two voice files from `templates/`. The `.skills-data/` folder is created on first use; add it to `.gitignore` if you don't want logs committed.

## Cross-skill routes

Some skills hand off to others (`/blindspot` ends with "Run /triage on these"). If the target is not installed, the skill says so and finishes the step inline. Nothing here requires another skill to run.

## Uninstall

Plugin: `claude plugin uninstall drewbrucker-skills@drewbrucker-claude-skills`.
Folder copy: delete the folder.
App upload: remove it from the same settings page.
