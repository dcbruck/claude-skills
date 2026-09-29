# claude-skills

Eleven skills for Claude that I run every day as an independent AI creative consultant, stripped of everything specific to my setup so they work on yours.

Each skill is a folder with a `SKILL.md`. Install one or all of them in Claude Code, the Claude desktop app, or claude.ai. They are slash commands: they fire only when you type `/name`, never on their own.

## The skills

**Think**

| Skill | What it does |
|---|---|
| [`/beastmode`](skills/beastmode) | Rewrites a rough prompt into the prompt you should have written, checks the rewrite against what you asked, routes to the right skill, and logs the run so the rewrites compound. Front door to the rest. |
| [`/blindspot`](skills/blindspot) | Inventories what you already own, then generates the high-ceiling things you have not thought to ask for. Kills everything below a stated bar instead of padding to ten. |
| [`/domainjack`](skills/domainjack) | Finds a proven mechanism in an unrelated field and transfers it to your problem. Scores the spread and guards against fake arbitrage. |
| [`/triage`](skills/triage) | Walks any list one item at a time, captures your verdict (shortlist, scope, hold, kill) with the reason, and banks it so the same idea never gets re-argued. |
| [`/adopt`](skills/adopt) | Evaluates outside content (a post, an article, a talk) against your actual system. Returns adopt / adapt / skip with a spec for each, and hunts for a better home before any skip stands. |

**Write**

| Skill | What it does |
|---|---|
| [`/ghost`](skills/ghost) | Drafts emails, proposals, newsletters, scripts, and page copy in your voice, then runs a seven-step audit gate before anything leaves. Bring your own voice profile and kill list. |
| [`/fleet`](skills/fleet) | Turns one long-form transcript into a full content set (posts, short-platform companions, clips, newsletter sections), every piece self-audited and differentiated across the batch. |

**Podcast and video**

| Skill | What it does |
|---|---|
| [`/mine`](skills/mine) | Mines a transcript into a queryable idea library: claims, frameworks, stories, numbers, and the collisions between them. |
| [`/youtube`](skills/youtube) | Builds the whole upload package for an episode: target queries, titles, description, chapters, citable claims, pinned comment, caption fixes, cold open, tags, clip picks, and the promotion block. |

**Ops**

| Skill | What it does |
|---|---|
| [`/redline`](skills/redline) | Reads a contract you are about to sign, clause by clause, against your standard positions. Returns tiered risks, proposed redlines, and negotiation notes. |
| [`/graph`](skills/graph) | Reads any SKILL.md or system doc and renders the real flow, branches included, as a self-contained HTML diagram. |

## How they fit together

```
/beastmode  ->  routes to the skill that owns the job
/blindspot  ->  /triage  ->  (scope)  ->  build
/domainjack ->  /triage
/adopt      ->  adopt / adapt / skip specs
transcript  ->  /mine (library)  or  /fleet (content set)  or  /youtube (package)
/ghost      ->  drafts anything that is not a LinkedIn post
/redline    ->  before you sign
/graph      ->  when you want to see what a skill actually does
```

## Install

See [INSTALL.md](INSTALL.md). Short version:

```bash
# Claude Code, everything at once
claude plugin marketplace add dcbruck/claude-skills
claude plugin install drewbrucker-skills@drewbrucker-claude-skills

# Claude Code, one skill, no plugin
cp -r skills/triage ~/.claude/skills/triage

# Claude app / claude.ai
# Settings > Capabilities (desktop) or Settings > Customize > Skills (web), upload the skill folder or a zip of it.
```

## Bring your own voice

`/ghost` and `/fleet` write in *your* voice, which means they need two files you own:

- `voice-profile.md`: how you write. Start from [`templates/voice-profile.md`](templates/voice-profile.md).
- `kill-list.md`: the tells you refuse to ship. Start from [`templates/kill-list.md`](templates/kill-list.md) and add your own.

Without them, pass `--no-voice` and the skills draft in a clean first-person register and skip the voice checks. The audit still runs.

## What is not here

The mechanics are public. The taste is not. My own voice profile, my full kill list, and the client-specific skills stay private. Every skill here runs without them.

## License

MIT. Use them, fork them, ship them inside your own stack. Attribution is appreciated, not required.

Built by [Drew Brucker](https://drewcbrucker.com). I help brands create, operationalize, and scale on-brand creative with AI. Co-host of the [Fast Hours](https://www.youtube.com/channel/UCxkOnB_ojDRWywB2W1fGCdg) podcast.
