---
name: blindspot
description: "Manual high-ceiling idea generation against the user's actual system. ONLY triggers when the user explicitly types /blindspot followed by a domain, a question, or nothing at all. Do NOT auto-fire on \"any ideas,\" \"what should I do,\" \"give me suggestions,\" or \"what am I missing\" in normal conversation. /blindspot answers the ask people keep making in different words: what are the most powerful things I have yet to ask for, what should I be asking for that I don't know to ask, what would you strongly recommend adding given my current setup. It inventories what the user already owns before generating, holds every candidate to a stated power bar, scores survivors on an inline rubric, kills everything below the floor rather than padding to a round number, and hands survivors to /triage. NOT for scoring effort or estimating hours, NOT for capturing verdicts (/triage), NOT for open-ended strategy conversation."
license: MIT
metadata:
  version: 1.0.0
  author: Drew Brucker
  source: https://github.com/dcbruck/claude-skills
---

# /blindspot: what the user has not thought to ask for

/blindspot produces ideas the user does not already own, at a ceiling high enough to be worth their attention. It fails in two ways, both preventable before the user sees a single line. It returns something they already have, and they ask "Don't I already have this?" Or it returns competent, obvious suggestions, and they say "not bad, but not powerful either." The prevention is the skill.

## Setup

Reads only. Nothing is written.

| Source | What it is |
|---|---|
| Installed skills | The full list, names and descriptions. |
| Scheduled tasks and automations the user runs | Whatever the environment exposes, or whatever the user lists in CLAUDE.md or equivalent. |
| Project files | Whatever the user keeps: CLAUDE.md, project notes, a pipeline file. |
| `decisions.md` (optional) | If the user keeps a decisions log, check candidates against it. |
| `.skills-data/triage-backlog.md` (optional) | What has already been proposed, held, or killed. Written by /triage. |

Nothing is required. A thin inventory lowers confidence in the "already owns it" cut, so say so in one line when the inventory is thin.

Your project's writing and formatting rules apply if you have them (CLAUDE.md or equivalent). Assume them.

## Trigger

The user types `/blindspot` followed by a domain, a question, or nothing. Nothing means the whole system.

```
/blindspot
/blindspot my content pipeline
/blindspot what should a solo consultant with my setup automate next
```

Does not fire on "any ideas," "what should I do," "give me suggestions," or "what am I missing" without the slash command.

## The bar

Things that 5-10x. Things with serious bite, forethought, depth, and creativity. Ideas the user would not have reached alone.

Read that before generating and hold it during the kill pass. Competent is a fail. Obvious is a fail. Something a generic consultant would say about a generic operator is a fail.

## Step 1: Inventory first, silently

Never generate before knowing what exists. Read, do not assume:

- The user's installed skills. The full list, names and descriptions.
- The scheduled tasks and automations the user runs.
- Whatever project files the user keeps, for what is live and what is in motion.
- `decisions.md`, if one exists, for standing constraints. A recommendation that violates an active decision is dead on arrival.
- `.skills-data/triage-backlog.md`, if one exists, for what has already been proposed, held, or killed.

An idea that was killed before comes back only with a reason the original objection no longer holds. Say that reason out loud when it happens.

## Step 2: Generate wide, privately

Produce roughly three times what the user asked for. None of this is shown.

Generate from the user's actual system state, never from best practices. The useful ideas come from the seams: a place where two of their systems should touch and do not, a loop that produces output nothing reads, a manual step sitting between two automated ones, an asset they own and do not exploit, a measurement they never take.

Push past the first tier deliberately. The first five ideas on any topic are the obvious five. The ones worth the user's time start after that.

## Step 3: Kill pass

Cut every candidate that hits any of these. This runs before the user sees anything.

**Already owns it.** Full overlap with an existing skill, task, or system. Cut silently. Partial overlap survives only if you can name precisely what is new, and the new part has to carry the idea on its own.

**Generic.** True of anyone in the user's role. If the idea survives swapping the user's name for someone else's, it is not about them.

**Low ceiling.** Saves minutes, not hours. Improves something already working. Nice to have.

**Cannot hold the context.** Depends on information the model cannot reliably get: cold outsiders, unrecorded relationships, off-channel nuance. The rubric penalizes these for a reason.

**Violates a standing decision.** Check against `decisions.md` before it reaches the list.

## Step 4: Score the survivors

One rubric. Do not invent a second one.

- **Value axes, 1-5 each:** Power (how much it changes what the user can do), Value (what it is worth in hours or money if it works), Significance (whether it touches something central or peripheral), Leverage (how much output per unit of setup, and whether it compounds).
- **Cost axes, 1-5 each:** Effort (hours to a satisfactory version, user plus model) and Risk (what breaks, leaks, or drifts if it goes wrong).
- **Score:** the sum of the value axes minus the sum of the cost axes. Range -6 to 18.
- **Perishability discount:** subtract 1 to 3 when the idea's value decays fast (a window closes, a platform changes, a trend passes).
- **Context-feasibility penalty:** subtract 1 to 3 when the idea depends on context the model cannot reliably hold or fetch.

**Discard floor: 8.** Anything scoring below it is not presented, no matter how few survive.

**Never pad to the number.** If the user asked for 10 and 4 clear the floor, present 4 and say "4 cleared, the other 6 were obvious or you already have them." Filler is the failure mode users call out by name. A short honest list is the deliverable.

## Step 5: Present

Ranked by score, highest first. Per idea, three lines and no more:

**[Name]**: what it does, one sentence.
*Why it is not obvious:* the specific thing about the user's setup that makes this available to them and not to everyone.
*What they structurally cannot do by hand:* the fan-out, the exhaustive sweep, the parallel adversarial pass, the thing that only exists because a machine runs it. If there is no answer here, the idea probably belonged in the kill pass.

No pitching. No paragraph per idea. The user is scanning.

Close with two lines: the count that cleared versus the count generated, and "Run /triage on these." Nothing else.

## Continuations

When the user asks for more on the same topic ("now give me 10 more"), exclude everything already shown this session and everything already in the backlog. Repeating a candidate they just saw reads as not listening.

Later rounds get harder, not easier. The bar does not drop because the easy ideas are gone. If round three produces two survivors, present two.

## Output

1. The ranked list, three lines per idea, score not shown.
2. Two closing lines: cleared versus generated, and "Run /triage on these."

Silent, every run: the inventory, the wide generation, the kill pass, the scoring.

## Boundaries

- **Never open with clarifying questions.** The user gave a domain or they did not. Take the strongest reading, generate, and let them redirect. Firing a question instead of a list is how these sessions die.
- **Name the seam, not the trend.** "You should use AI agents more" is noise. "Your content system produces at volume and measures nothing after it ships" is a finding.
- **One idea, one line of why.** If it takes three paragraphs to explain why an idea is good, it is not obvious enough to be good.
- **Count programmatically.** Generated, killed, cleared. Report real numbers.
- Not for effort estimates. Not for capturing verdicts (that is /triage). Not for open-ended strategy conversation.
