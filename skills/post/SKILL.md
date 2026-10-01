---
name: post
description: "Manual LinkedIn post generator. ONLY triggers when the user explicitly types /post followed by a raw idea or topic. Do NOT auto-fire on related-sounding asks like \"write me a post\" or \"I want to post about X.\" Takes the raw idea, drafts five post bodies in five different architectures (in parallel where the environment supports subagents, blind to each other), loops each against the user's kill list until clean, kills twins and failures, writes the hooks LAST across the survivors, and presents up to three finished posts for the user to pick. Voice comes from the user's voice-profile.md; the audit comes from kill-list.md. Not for emails, newsletters, or page copy (/ghost), or for turning a transcript into a content set (/fleet)."
license: MIT
metadata:
  version: 1.0.0
  author: Drew Brucker
  source: https://github.com/dcbruck/claude-skills
---

# /post: five shapes drafted blind, the hook comes last

/post turns one raw idea into finished LinkedIn posts. It drafts five bodies in five different shapes, each on its own, audits each one until it's clean, kills the twins and the failures, and only then writes the opening lines. The user picks from up to three finished posts. The one failure it exists to prevent: a post built around a hook written first, so the body bends to serve a line that sounded good in isolation, and every option reads like the same post in a different shirt.

## Setup

Files, project root by default:

| File | What it is |
|---|---|
| `voice-profile.md` | Your voice profile. Build one with the template in `templates/voice-profile.md`. Its tone spectrum should carry a LinkedIn register. |
| `kill-list.md` | Your list of writing tells to hunt. A starter lives at `templates/kill-list.md`. |
| `.skills-data/post-log.md` | Optional performance log. Created on first use if the user wants it. See Step 2. |

Optional extras. If you keep a hook library, a list of post architectures you like, or a lint script for drafts, load them here; they replace or extend the defaults below. If you keep project writing and formatting rules (CLAUDE.md or equivalent), they apply. Assume them.

Flags:

- `--no-voice`: no voice profile yet. Drafts in a clean, plain, first-person register and skips the voice-fidelity checks. The kill-list scan still runs. If `kill-list.md` is also missing, the high-escape list in Step 6 is the minimum.
- `--hooks`: hooks-only mode. Three hook lines for the idea, nothing else. The user picks one and the skill writes the full post around it (body drafted first, hook refit last).
- `--one`: deliver only the strongest finished post instead of three.

## Trigger

Fires only on the explicit slash form:

```
/post [raw idea, topic, story, or half-formed take]
```

Examples:

- `/post the client who asked for "more AI" and meant "fewer meetings"`
- `/post why my best-performing post took 11 minutes to write`
- `/post I stopped writing hooks first and my replies doubled`

Does NOT fire on "write me a post" or "I want to post about X." Those are ordinary requests, handled outside this skill.

If the idea is too thin to draft against (one word, no angle), ask one targeted question before generating. One question, not a questionnaire.

## Step 1: load the files (refuse if missing)

Confirm `voice-profile.md` and `kill-list.md` are in context. If either is missing and `--no-voice` was not passed, stop. Reply: "Missing `voice-profile.md` (or `kill-list.md`). Attach it, point me at it, or re-run with `--no-voice`." Do not draft.

Load any optional files the user keeps (hook library, architecture list, performance log, lint script).

## Step 2: read the performance log (optional)

If `.skills-data/post-log.md` exists, read it before picking shapes. It's a running list of shipped posts: date, architecture, hook mechanism, and whatever result the user records (reactions, comments, replies, profile views, "felt flat"). Use it two ways:

- **Earning:** any architecture and hook pairing that shows up 3+ times with strong results is a candidate for one of the five slots.
- **Fatigued:** any architecture used 4 times in the last 10 posts rotates out unless the idea plainly wants it. If it does, use it and say why in the header.

Surface the data. Don't hardwire it. No log means no constraint; skip this step.

After the user picks a post, offer once to append it to the log. Never write to the log without the user's yes.

## Step 3: pick five architectures

Pick five different architectures for this idea and name them. Defaults below; a user-supplied architecture list replaces them.

| Architecture | Shape |
|---|---|
| Story | One scene, told in order, landing on what it changed. |
| List | Numbered items, each a title line plus one or two short paragraphs. Uneven lengths. |
| Teardown | One real thing (a post, an ad, a deck, a workflow) taken apart piece by piece. |
| Before and after | The old way, the specific moment it broke, the new way, the number that moved. |
| Confession | A mistake the writer made, what it cost, what they do now. |
| Wall | One dense, unbroken argument. Few line breaks. Earns attention by refusing to perform. |
| Punch | Under 80 words. One observation, no setup, out. |
| Receipts | A claim, then the evidence stacked under it: screenshots described, numbers, dates. |
| Field note | Something the writer noticed this week, why it stuck, what they're doing about it. |
| Bet | A plainly stated prediction with the reasoning and what would prove it wrong. |

At least two of the five should be shapes the log shows earning, if there's a log. At most one fatigued shape.

## Step 4: fan out the bodies (hook last is law)

Draft five bodies, one per architecture. No body gets a real opening line. Each starts with the placeholder `[HOOK]`.

**Where subagents are available** (Claude Code and similar), spawn five in the same turn, one per architecture, fresh context each. Every branch gets: the raw idea, its assigned architecture, the paths to `voice-profile.md` and `kill-list.md` (paths, not summaries), the performance-log read if there is one, and this brief:

> Draft ONE post body in this architecture, in the user's voice, with `[HOOK]` as the opener placeholder. One specific insight, not three vague ones. At least one concrete detail only someone who was there would know: a number, a name the user has cleared, a time, an object. End on a line that earns a re-read or a reply: a stake, a scene, a number, or a plainly stated bet, never a summary or a portable life lesson. Then loop: scan the body against `kill-list.md` soul-level first, then the high-escape list in the skill's Step 6. If the user keeps a lint script, run it too. Fix every hit. Re-scan. Repeat until clean, max three laps. Return: the body, the lap count, and a short receipt of what got flagged each lap. If it still fails after three laps, return it marked FAILED with the last flags. Never return a flagged body as if it were clean.

Branches don't see each other. Independence is what produces five different attempts instead of one attempt five times.

**Where subagents aren't available** (the Claude app, claude.ai), draft the five in sequence and keep them blind by rule: before each body, set the previous ones aside and don't reuse a sentence, an example, or a closing move from any of them. Run the same three-lap loop on each body before starting the next.

## Step 5: merge, kill twins, cut to three

Collect the five. Drop any FAILED branch.

Run the set-level scan across the survivors. Two bodies are twins if they share any of these: the same closing move, the same skeleton (same setup, same turn, same landing), the same central example, or the same opening rhythm. When two collide, keep the one with the cleaner receipt and the shape the log favors. The other dies.

Cut to the three strongest by the quality bar: would a reader stop scrolling, would the user put their name on it, does it read like a person. Fewer than three survivors: say so and deliver what survived. Never pad with a body that failed.

## Step 6: write the hooks last

With the surviving bodies in hand, write 8 to 10 opening-line candidates across the set. This is the only place an opener gets written. Defaults for hook mechanisms below; a user-supplied hook library replaces them.

| Mechanism | What it does |
|---|---|
| Specific number | Opens on a figure only this story has. "11 minutes." |
| Scene drop | Starts mid-moment, no setup. |
| Confession | The writer admits the thing first. |
| Stated bet | A prediction plainly made, with something at stake. |
| Overheard line | A real quote from a real person the user can name or describe. |
| Odd object | One concrete, slightly strange detail that demands the next line. |
| Reader's own words | The outcome the reader wants, in the words they'd use for it. |

Run every candidate through the next-line test. A hook passes only if all five hold:

1. **Open loop.** The reader can't predict the second line.
2. **Concrete anchor.** At least one specific: a number, a name, an object, a time.
3. **Read-aloud.** It sounds like a person said it across a table.
4. **No template smell.** It doesn't match a hook formula the reader has seen a hundred times.
5. **Load-bearing.** Delete it and the body loses its first beat, not just its decoration.

Kill anything that fails. Assign the best surviving hook to each body and fit the body's first line to it so the seam disappears.

**High-escape list.** Hunt these by name in every body and hook, even if `kill-list.md` misses them:

- Negate-then-assert in every costume: "X isn't Y, it's Z," "not because A but because B," "stops being X, becomes Y," and the mirrored pair. Zero tolerance. State the positive directly.
- Trio lists when the real count isn't three.
- Concluding summary and the aphoristic-maxim closer.
- Post-insight explanation ("Which means..." "In other words...").
- Label-colon reveal ("The fix: shorter.").
- Restatement staircase and command cascades.
- Fragment stacks used to enumerate ("The prompts. The workflows. The systems.").
- Contraction avoidance where speech would contract.
- Em dashes, if the user's kill list bans them.
- Invented people, invented numbers, invented quotes. Every specific has to be real or come from the user.

## Step 7: final audit and delivery

Run the full kill-list scan on each assembled post (hook plus body), then the set-level scan again across the three: no two finished posts share a closer shape, a skeleton, or a framing.

Then a proportionality check: compare each post to its pre-audit body. Revert any change made for tidiness alone. A post that passes every pattern and sounds like nothing has failed.

Deliver all three (or one with `--one`), each with a one-line header:

```
## [Architecture] · hook: [mechanism] · laps to clean: [n] · log: [earning / neutral / fatigued / no log]

[Full post]
```

No preamble. No ranking commentary. No audit log. The user picks one, edits one, or takes all three.

## Boundaries

The skill refuses to proceed when:

1. **A required file is missing** and `--no-voice` wasn't passed.
2. **"Skip the audit" is requested.** The audit is the product.
3. **The idea involves a client, an employer, or anything under NDA** and the user hasn't said it's cleared. Flag it and ask before drafting. Uncleared names become roles ("a fintech CMO").
4. **The content isn't a LinkedIn post.** Emails, newsletters, scripts, and page copy go to /ghost. A whole transcript goes to /fleet.

It never:

- Writes a hook before the bodies exist (except `--hooks`, where the body is still drafted before the hook is refit).
- Invents a character, a quote, or a result to make a hook land.
- Modifies `voice-profile.md` or `kill-list.md`.
- Writes to the performance log without the user's yes.
