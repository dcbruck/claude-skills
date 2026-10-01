# claude-skills

Twelve skills for Claude that I run every day as an independent AI creative consultant. I stripped out everything tied to my own setup so they work on yours.

A skill is a set of instructions Claude loads on command. Type `/post` and Claude runs my whole post workflow, start to finish. Each one lives in a folder with a `SKILL.md` and works in Claude Code, the Claude desktop app, and claude.ai. They only run when you type the command. Nothing fires on its own.

<table>
<tr>
<td width="33%" valign="top"><a href="skills/beastmode"><img src="media/beastmode.webp" alt="/beastmode"></a><br><b><code>/beastmode</code></b><br>Rewrites your rough request into the prompt you should've written, then hands it to the right skill.</td>
<td width="33%" valign="top"><a href="skills/blindspot"><img src="media/blindspot.webp" alt="/blindspot"></a><br><b><code>/blindspot</code></b><br>Hunts for the ideas you haven't thought to ask for, then throws out most of them on purpose.</td>
<td width="33%" valign="top"><a href="skills/domainjack"><img src="media/domainjack.webp" alt="/domainjack"></a><br><b><code>/domainjack</code></b><br>Steals a proven idea from a completely different industry and puts it to work on your problem.</td>
</tr>
<tr>
<td valign="top"><a href="skills/adopt"><img src="media/adopt.webp" alt="/adopt"></a><br><b><code>/adopt</code></b><br>Paste in advice from the internet and it checks every tip against what you've already built before you use any of it.</td>
<td valign="top"><a href="skills/post"><img src="media/post.webp" alt="/post"></a><br><b><code>/post</code></b><br>Drafts five versions of a LinkedIn post, cuts the weak ones, writes the hooks last, and lets you pick.</td>
<td valign="top"><a href="skills/ghost"><img src="media/ghost.webp" alt="/ghost"></a><br><b><code>/ghost</code></b><br>Writes emails and copy in your voice, then scans its own draft for AI tells and rewrites until it's clean.</td>
</tr>
<tr>
<td valign="top"><a href="skills/fleet"><img src="media/fleet.webp" alt="/fleet"></a><br><b><code>/fleet</code></b><br>Turns one podcast episode into a week of posts, threads, clips, and newsletters, with no two pieces saying the same thing.</td>
<td valign="top"><a href="skills/mine"><img src="media/mine.webp" alt="/mine"></a><br><b><code>/mine</code></b><br>Breaks every transcript into single ideas and files them in a library that starts spotting patterns across everything you've saved.</td>
<td valign="top"><a href="skills/youtube"><img src="media/youtube.webp" alt="/youtube"></a><br><b><code>/youtube</code></b><br>One episode transcript becomes a full YouTube upload, with every chapter timestamp checked.</td>
</tr>
<tr>
<td valign="top"><a href="skills/redline"><img src="media/redline.webp" alt="/redline"></a><br><b><code>/redline</code></b><br>Reads a contract before you sign and flags the risky terms, including protections that are missing entirely.</td>
<td valign="top"><a href="skills/graph"><img src="media/graph.webp" alt="/graph"></a><br><b><code>/graph</code></b><br>Reads how any skill actually works and draws it as a diagram, messy parts and all.</td>
<td valign="top"><a href="skills/triage"><b><code>/triage</code></b></a><br>Walks any list one item at a time, records your call and the reason, and banks it so the same idea never gets re-argued.</td>
</tr>
</table>

## Install

Claude Code, all twelve at once:

```bash
claude plugin marketplace add dcbruck/claude-skills
claude plugin install drewbrucker-skills@drewbrucker-claude-skills
```

Claude desktop app or claude.ai: grab a skill's zip from the [latest release](https://github.com/dcbruck/claude-skills/releases/latest) and upload it under **Settings > Capabilities** (desktop) or **Settings > Customize > Skills** (web).

One skill in Claude Code, no plugin:

```bash
cp -r skills/post ~/.claude/skills/post
```

Full details, updates, and uninstall live in [INSTALL.md](INSTALL.md).

## The skills in more detail

**Think**

| Skill | What it does |
|---|---|
| [`/beastmode`](skills/beastmode) | Rewrites a rough prompt into the prompt you should've written, checks the rewrite against what you actually asked, routes it to the skill that owns the job, and logs the run so rewrites compound. The front door to the rest. |
| [`/blindspot`](skills/blindspot) | Inventories what you already own, then generates the high-ceiling things you haven't thought to ask for. Kills everything below a stated bar rather than padding to ten. |
| [`/domainjack`](skills/domainjack) | Finds a proven mechanism in an unrelated field and transfers it to your problem. Scores the spread and guards against fake arbitrage. |
| [`/triage`](skills/triage) | Walks any list one item at a time, captures your verdict (shortlist, scope, hold, kill) with the reason, and banks it. |
| [`/adopt`](skills/adopt) | Evaluates outside content (a post, an article, a talk) against your actual setup. Returns adopt, adapt, or skip with a spec for each, and hunts for a better home before any skip stands. |

**Write**

| Skill | What it does |
|---|---|
| [`/post`](skills/post) | Five LinkedIn post bodies in five architectures, drafted blind and audited to clean. Twins die, hooks get written last, you pick from three finished posts. |
| [`/ghost`](skills/ghost) | Drafts emails, proposals, newsletters, scripts, and page copy in your voice, then runs a seven-step audit gate before anything leaves. |
| [`/fleet`](skills/fleet) | Turns one long-form transcript into a full content set (posts, short-platform companions, clips, newsletter sections), each piece self-audited and differentiated across the batch. |

**Podcast and video**

| Skill | What it does |
|---|---|
| [`/mine`](skills/mine) | Mines a transcript into a queryable idea library: claims, frameworks, stories, numbers, and the collisions between them. |
| [`/youtube`](skills/youtube) | Builds the whole upload package for an episode: target queries, titles, description, chapters, citable claims, pinned comment, caption fixes, cold open, tags, clip picks, and the promotion block. |

**Ops**

| Skill | What it does |
|---|---|
| [`/redline`](skills/redline) | Reads a contract you're about to sign, clause by clause, against your standard positions. Returns tiered risks, proposed redlines, and negotiation notes. Not legal advice. |
| [`/graph`](skills/graph) | Reads any SKILL.md or system doc and renders the real flow, branches included, as a self-contained HTML diagram. |

## How they fit together

```
/beastmode  ->  routes to the skill that owns the job
/blindspot  ->  /triage  ->  build
/domainjack ->  /triage
/adopt      ->  adopt / adapt / skip specs
idea        ->  /post (LinkedIn)  or  /ghost (everything else)
transcript  ->  /mine (library)  or  /fleet (content set)  or  /youtube (upload package)
/redline    ->  before you sign
/graph      ->  when you want to see what a skill actually does
```

Every skill runs alone. When a handoff target isn't installed, the skill says so and finishes the step inline.

## Bring your own voice

`/post`, `/ghost`, and `/fleet` write in *your* voice, so they read two files you own:

- `voice-profile.md`: how you write. Start from [`templates/voice-profile.md`](templates/voice-profile.md).
- `kill-list.md`: the tells you refuse to ship. Start from [`templates/kill-list.md`](templates/kill-list.md) and add the patterns you keep deleting.

No profile yet? Add `--no-voice` and they draft in a plain first-person register. The audit still runs.

## What isn't here

My own voice profile and full kill list stay private, along with the skills built around specific clients. Every skill here runs without them.

## License

MIT. Use them, fork them, ship them inside your own stack. Attribution is appreciated, never required.

Built by [Drew Brucker](https://drewcbrucker.com). I help brands create, operationalize, and scale on-brand creative with AI. Co-host of the [Fast Hours](https://www.youtube.com/channel/UCxkOnB_ojDRWywB2W1fGCdg) podcast.
