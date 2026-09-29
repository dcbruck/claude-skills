---
name: triage
description: Manual list-triage loop. ONLY triggers when the user explicitly types /triage followed by a list, or /triage on its own to walk the list the model just produced. Do NOT auto-fire on "which of these," "what do you think," or "narrow this down." /triage walks a numbered list of ideas, candidates, or options one pass at a time, captures the user's verdict on each (SHORTLIST, SCOPE, HOLD, KILL) with their stated reason, and banks all four to .skills-data/triage-backlog.md so nothing evaporates when the session ends. Also resurfaces stale holds and flags items the user already owns. Shortlisted items hand off to the user's own scoping skill if one is installed; otherwise the skill scopes inline. NOT for generating the list (that's /blindspot or a brainstorm), NOT for scoring or estimating effort.
license: MIT
metadata:
  version: 1.0.0
  author: Drew Brucker
  source: https://github.com/dcbruck/claude-skills
---

# /triage: list walk and bank

/triage walks a numbered list, captures the user's verdict on every item with the reason behind it, and writes all of it to a backlog file that outlives the session. Most people triage lists well and fast. What they lack is anywhere for "hold this one" to land, so the same ideas get regenerated, re-argued, and re-held three weeks later. The one failure this skill exists to prevent: a verdict that evaporates when the session ends.

## Setup

One file, under `.skills-data/` at the project root by default.

| File | What it is |
|---|---|
| `.skills-data/triage-backlog.md` | The ledger: one line per verdict, additive-only. Missing on first run: create it with a one-line header and the four-verdict legend. |

Optional reads for the dedupe pass: installed skills, scheduled tasks and automations the user runs, and whatever project files the user keeps. Nothing is required.

Your project's writing and formatting rules apply if you have them (CLAUDE.md or equivalent). Assume them.

## Trigger

The user types `/triage` followed by a list, or `/triage` alone to walk the last numbered list produced in this session.

```
/triage
1. Weekly competitor sweep as a scheduled task
2. Auto-draft replies to inbound leads
3. Rebuild the pricing page
/triage on the ideas above
```

Does not fire on "which of these," "what do you think," "narrow this down," or any list without the slash command.

## The verdict vocabulary

Four verdicts. Use these exact words in output so the ledger stays parseable.

- **SHORTLIST**: worth pursuing. Goes to the top of the backlog. Next stop is effort scoping.
- **SCOPE**: interesting, but the effort and dependencies are unknown and that is the blocker. Gets scoped before any decision.
- **HOLD**: not now. Not dead. Carries a resurface date.
- **KILL**: no. Carries the reason, because a killed idea that comes back needs to meet its original objection.

Natural phrasings map cleanly: "let's shortlist it" is SHORTLIST, "let's scope it" is SCOPE, "hold on this" and "nah, hold this" are HOLD, "don't like this one" and "not significant enough" are KILL. Read intent. Never make the user use the keywords.

## Before presenting the list

Two passes, both silent, both before the user sees anything.

**Dedupe against what the user owns.** Check each item against their installed skills, their scheduled tasks and automations, and whatever project files they keep. Anything they already have gets marked `[already have: /x]` inline rather than presented as new. The user should never have to ask "Don't I already have this?" When it is a partial overlap, say which part is new.

**Pull the standing holds.** Read `.skills-data/triage-backlog.md`. Any HOLD whose resurface date has passed, and that is relevant to this list, gets appended to the bottom of the list under "Back from hold." Do not resurface everything, only what is relevant to the list in hand.

## The walk

Present the list numbered, compact. One line per item: what it is, and the single strongest reason it might be worth doing. No pitching, no padding, no three-paragraph case per item. The user is scanning, not reading.

Then stop and let them respond. They may answer all items in one message, or one at a time, or in clumps. Accept any of those. Never ask them to reformat their answer.

When the reason is implicit, infer it and write it down. When there is no reason at all and the item is a KILL or HOLD, ask for it in one short line, because a verdict without a reason is worthless six weeks later. Ask once. If none comes, bank it as "no reason given."

Do not argue with a verdict. If a KILL looks like a mistake worth one sentence of pushback, give the sentence, take the answer, and move on.

## Banking

Write every verdict to `.skills-data/triage-backlog.md`. Additive only. Never rewrite or restage existing entries.

Format per item:

```
- **[T-YYMMDD-NN]** [item, one line] | **VERDICT** | [the user's reason] | *source: [where the list came from]* | *[date]*
```

HOLD entries carry a resurface date: `resurface: YYYY-MM-DD`. Default 30 days. Use a different date when the item is waiting on something specific, and say what it is waiting on.

When an item is later re-triaged, append the new verdict as a new line referencing the original ID. Never overwrite the history. A KILL that becomes a SHORTLIST four months later is the most useful record in the file.

One backlog. Every item on the list gets its line here, whatever kind of item it is. Two registries holding the same item is the drift this skill exists to prevent.

## The scope handoff

Shortlisted items are ready for effort scoping. Route to the user's own scoping skill if one is installed. Otherwise the SCOPE verdict means the skill does the step inline: for each shortlisted or scoped item, estimate user-hours versus model-hours to reach a satisfactory version, list the dependencies (access, approvals, outside inputs), and say in one line whether it is worth building. Run the inline version only when the user says go at the close, never on its own.

## Close

Four lines, no more.

```
Shortlisted: N | [names]
To scope: N | [names]
Held: N | [names, resurface dates]
Killed: N
Banked to .skills-data/triage-backlog.md
```

Then one line naming the obvious next move. Usually: "Shortlisted items are ready for scoping." Say nothing else.

## Output

In order, every run:

1. The numbered list, one line per item, owned items marked inline, "Back from hold" items at the bottom if any.
2. A stop. The user responds.
3. Reason prompts, one short line each, only for KILL or HOLD verdicts with no reason.
4. The four-line close plus the next-move line.

Silent, every run: the dedupe pass, the holds pull, and the ledger writes.

## Boundaries

- **Never generate the list here.** If the user types /triage with no list and there is nothing recent to walk, say so and point them at /blindspot or a brainstorm. This skill triages. It does not ideate.
- **Never re-rank the user's verdicts.** They decide. The skill captures. If the shortlist ends up at nine items and that is too many to act on, say so in one line at the close and let them cut.
- **Never lose an item.** Every item on the input list gets a verdict and a ledger line. If the user skipped one, ask about that one specifically before closing. Silence is not a verdict.
- **Count programmatically.** The close reports numbers. Count them, never estimate them. An input list of 14 that produces 13 ledger lines is a bug, and the count is how you catch it.
- Not for scoring or effort estimates beyond the inline fallback above. Not for open-ended strategy conversation.
