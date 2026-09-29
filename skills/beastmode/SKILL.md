---
name: beastmode
description: "Manual prompt amplifier and front door to the user's skill stack. ONLY triggers when the user explicitly types /beastmode followed by a raw prompt (typed or dictated). Do NOT auto-fire on related asks like \"make this prompt better\" or \"amplify this.\" Takes everything after /beastmode in the user's most recent message, rewrites it into the prompt the user SHOULD have written, checks that rewrite against what they actually asked for, routes to the dedicated skill that owns execution, then banks the run so amplifications compound. Every run shows the amplified prompt before executing, no flag needed. Every substantive run ends with five next-move routes. Flags: --review (show the rewrite, then hold until the user says go), --deep (fan out across independent angles, then synthesize). Saying \"fast\" cancels an auto --deep."
license: MIT
metadata:
  version: 1.0.0
  author: Drew Brucker
  source: https://github.com/dcbruck/claude-skills
---

# /beastmode: prompt amplifier and router

/beastmode takes the prompt the user typed and writes the prompt they should have typed: real goal named, context pulled, constraints locked, output shape fixed, failure modes pre-loaded. It proves the rewrite still matches the ask, hands execution to the skill that owns the job, and logs what changed so the next amplification starts smarter. The one failure it exists to prevent: a rewrite that quietly drops a constraint the user stated, or adds scope they never asked for, and produces a polished answer to the wrong question.

## Setup

One file, under `.skills-data/` at the project root by default.

| File | What it is |
|---|---|
| `.skills-data/beastmode-log.md` | The run log: a **Standing moves** block at the top (amplification moves promoted to defaults), then append-only run entries. Missing on first run: create it with this header: |

```
# beastmode log

## Standing moves
(none yet)

## Runs
```

Optional integrations. If a source tool is connected (meeting recorder, calendar, email, document store, chat log), the skill resolves references there. Otherwise the user pastes or attaches the source. Nothing is required.

Your project's writing and formatting rules apply if you have them (CLAUDE.md or equivalent). Assume them.

Flags:

- `--review`: show the rewrite and what changed, then stop and wait for "go."
- `--deep`: fan out across independent angles before synthesizing. Auto-sets on exhaustive asks; "fast" cancels it.

Two flags is the ceiling.

## Trigger

The user types `/beastmode` followed by a raw prompt: everything after the command in their most recent message, typed or dictated.

```
/beastmode write the follow-up email to Acme after yesterday's kickoff, they want the timeline by Friday
/beastmode --review what should the pricing page say for the new tier
/beastmode --deep compare the three vendors we looked at for transcription and pick one
```

Does not fire on "make this prompt better," "amplify this," or any request without the slash command.

Design bar: Steps 4 through 7 (the amplifier) must work with no other skills installed. Step 3 (the router) uses whatever is installed. Never make the prompt longer for its own sake.

## Step 0: Flags

Scan for `--review` and `--deep`. Note them, strip them before amplifying.

Auto-set `--deep` when the raw prompt says every / exhaustive / comprehensive / think hard / all of them, or when the class is strategy or research and a wrong answer costs real money or reputation. "Fast" cancels it.

## Step 1: Read the session before reading the world

The last twenty turns of this session are free and denser than any file. Read them first. An amplified prompt that contradicts something decided four messages ago is the cheapest avoidable failure in this skill. If the raw prompt leans on something older than that window, go find it.

**Revision rounds.** If this /beastmode targets the same deliverable as a prior run in this session and the class has not changed, skip Steps 3, 6, and 7, run 8 through 10, and bank it as a `ROUNDS` increment on the existing log entry (Step 11). A new deliverable or a class change is a new run.

## Step 2: Gather live context

If the prompt names a date, call, meeting, person, deal, project, or doc, go get the real thing. If a source tool is connected, resolve it there. If nothing is connected, ask the user to paste or attach it before amplifying. Amplifying without the source means inventing it. Self-contained prompt: skip this step.

## Step 3: Classify, then route

Pick the class. It decides who executes. Trivial prompts (lookup, quick edit, yes/no) skip the table: answer directly, note the downgrade (Step 10).

| Class | Signal | Who executes |
|---|---|---|
| Content the user signs | email, newsletter, script, page copy, proposal copy | `/ghost` |
| Idea generation | "what am I missing," "what should I add," "what should I be asking for" | `/blindspot`, survivors to `/triage` |
| Capturing verdicts | a list of candidate ideas plus "which of these," "keep or kill" | `/triage` |
| Cross-domain transfer | a donor domain plus a target, "what could X borrow from Y" | `/domainjack` |
| Outside content evaluation | pasted post, article, URL, repo plus "any value for me" | `/adopt` |
| Source material | transcript, episode, URL, long-form input | `/mine` to bank, then `/fleet` to draft the content set |
| Episode packaging | a recorded episode plus titles, description, chapters, thumbnail | `/youtube` |
| Contract to sign | inbound MSA, SOW, NDA, vendor or content agreement | `/redline` |
| Skill or system visual | "show me how X works," a skill name plus "diagram" | `/graph` |
| Anything else | strategy, research, build, instructions, negotiation, audits | Execute inline in this conversation |

Three rules over the table:

- **Hybrid prompts get a primary and a secondary, run in order.** "Analyze this deal and draft the email" is strategy then content. Name the sequence in the rewrite.
- **The table is a map, not the territory.** If the user has an installed skill the table missed, invoke it and flag the table as stale. Never rebuild a chain that exists.
- **Beastmode owns amplification. The matched chain owns execution.**

**Inline execution.** When the class lands on the last row, carry the class's own discipline into the run. Research: cite sources, state confidence, label claims fact / inference / assumption. Strategy: name what must be true, separate reversible from irreversible. Build or config: state what exists, what changes, what breaks if wrong, before touching anything. Negotiation and pricing: draft only.

## Step 4: Amplify

**Reconstruct first if the input is dictated or disordered.** Strip filler. Collapse repeats to their strongest statement. Where the user pivoted mid-thought ("actually, scratch that"), the last version wins. When the real ask lands at the end after a wind-up, it is the primary ask. Put out-of-order points in logical order. Names, numbers, and dollar figures that look mis-transcribed get flagged under Assumed, never guessed. Nothing gets dropped silently; anything you interpreted goes under Assumed (Step 7).

**Lossless rule.** The prompt may get shorter; the content may not. Compress phrasing freely. Never drop a constraint, a fact, an exclusion, a named audience, or anything the Step 2 source carried that bears on the answer. Shortening how it reads is the goal. Shortening what it carries is the failure.

Then read the **Standing moves** block at the top of `.skills-data/beastmode-log.md` (escalated defaults, not suggestions) and rewrite into the precision version:

- **Name the real goal.** What the user is trying to accomplish, not what they typed. One line, in your head.
- **Raise the ambition, against a ceiling.** Amplify precision and hit rate. Never amplify scope. A lazy prompt is a floor for quality, not an invitation to triple the deliverable. If the amplified version costs roughly 10x the raw ask, surface the fork in one line and let the user pick.
- **Honor their seeds and gates.** An example of their thinking is a pattern to extend, not copy. A decision point ("I'll tell you which to start") means generate up to it and STOP there.
- **Name one anti-goal.** What this output must not become.
- **Pre-load the failure modes.** Name the top two ways this flops (generic framing, AI tells, wrong audience, off-voice, ignoring the context you just pulled) and design around them.
- **Lock the output shape** before writing: format, length, structure, ranking.

Then two more calls:

**Pull from the clause bank.** Take at most three clauses from the Clause bank (bottom of this file) that match the class and would materially raise the ceiling of this run. Fold them into the block's Constraints or Avoid lines and carry them into execution. Skip any clause the matched chain already enforces: `/domainjack` owns mechanism transfer, `/blindspot` owns the power bar on ideas, `/ghost` and `/fleet` own writing. Zero clauses is a fine answer. Clause-bank filler is the failure this rule exists to prevent.

**Pick the working method.** Most runs are one-pass; say nothing. Force **research-first** when a consequential factual claim could have changed since training, or the raw prompt leans on a source Step 2 has not pulled: research completes before drafting starts. Force the **rubric loop** when the deliverable is scoreable, the stakes are real, and no audit skill owns it: derive a five-dimension weighted rubric from the success criteria, draft, score against it, revise the material failures once. Never run the rubric loop on content headed to `/ghost` or `/fleet`; their audit gates are the rubric. Name a forced method inside the block's Output line ("via rubric loop," "research-first"). The six sections do not change.

## Step 5: Intent-fidelity gate

The amplifier is the only step that can silently ruin a run, so it does not grade itself on the output alone. Diff the amplified prompt against **two** things: the raw prompt, and whatever Step 2 pulled.

1. **What did I add that the user did not imply?** Scope creep. Cut it, or surface it under Assumed.
2. **What did the user say that my rewrite dropped?** Constraints, exclusions, gates, tone, a named audience. The expensive failure, invisible without the check. Restore it.
3. **What did the source carry that my Context line dropped?** When Step 2 pulled a transcript, deal file, or thread, the compression into one Context line is where a load-bearing detail vanishes unwatched. Diff the line against the source; restore anything that bears on the answer.

Anything the rewrite or the Context line dropped wins over anything the rewrite added.

## Step 6: Scope questions (high stakes only, before the block)

Fire only when all three are true: the class is high stakes, the work is expensive or irreversible to redo, and the answer changes what gets built.

Ask as multiple choice, recommended option first, 2-3 questions. Use the environment's question tool if it has one. Never open prose questions; the user takes those offline and the session dies. Clickable gets answered.

This runs before the block so the rewrite carries their answers instead of going stale.

## Step 7: Show the rewrite (every run)

Every run surfaces the amplified prompt before execution. Fixed sections, same order every time, prose inside each:

````
## Beast-Mode Prompt
**Goal:** [the real objective, one or two lines]
**Context:** [what this rests on: sources pulled, session decisions, constraints inherited from the deal or project]
**Constraints:** [what must hold: gates, exclusions, audience, tone, scope ceiling]
**Output:** [format, length, structure, ranking, and done-when: what makes this complete]
**Avoid:** [the anti-goal and the top failure modes]
**Assumed:** [choices made on the user's behalf that they did not specify, incl. reconstruction calls on dictated input and any source rerouting. Omit when empty.]
````

The skeleton is the receipt: a missing section is visible at a glance, and the block pastes into any LLM as a standalone prompt. If the fidelity gate surfaced a fork, append it in one line under the block.

- **Default (no flag):** show the block, then move straight into execution. The block is a receipt, not a gate. The user interrupts if the rewrite is off.
- **`--review`:** show the block plus What changed (Step 10), then STOP and wait for "go."

Skip the block only on trivial prompts answered directly. Never echo the raw prompt; the user can see it directly above. No diagram, map, or visual accompanies the block; the block is the whole receipt.

## Step 8: Execute

Run the matched chain off the **full context**: the raw prompt, the reconstructed dictation, and everything Step 2 pulled. The Beast-Mode Prompt block is a compressed receipt, not the execution input. Executing off the block instead of the full picture is how context that never fit the six sections gets silently lost.

Under `--deep`, fan out first: independent agents on independent angles, each blind to the others, then synthesize. No agent spawning available: run each angle as a separate pass. Never deliver raw agent output. One synthesized answer, always.

## Step 9: Self-critique (always, silent)

Read the draft once as an adversary. Find the single weakest part. Fix it. Never skip, even under `--review`.

## Step 10: Deliver

**Delivery law:** the final deliverable appears in the chat, verbatim, every time. A file path is not delivery. Save the file too when it makes sense, and still paste it.

**If `--review`:** the Step 7 block plus this, then stop and wait for "go":

````
## What changed
[one or two lines: what you sharpened, what context you pulled, what the fidelity gate caught. So the user learns to write it themselves next time.]
````

**Otherwise:** the block already appeared (Step 7). After it, deliver only the final answer. No narration of the chain between the block and the answer.

**Downgrade note:** when the raw prompt did not need amplification, say so in one line after the answer: "This one didn't need beastmode." Teaches the user when to spend the command.

## Step 10b: Next-moves tail (every substantive run)

Beastmode holds both the answer and the shape of the run: what it routed to, what it held at a gate, what it deferred, which skills sit adjacent. So every substantive run ends with five routes, three parts thinking, two parts pathway.

**Hard rules for the five.** One sentence each. Specific to the answer above. No service questions ("want me to expand this?"). No hedges. No restating the ask. Numbered, no preamble, nothing after them.

```
R1. [Deeper dig: the next-layer question if you kept following this exact thread]
R2. [Adjacent route: the skill or move next to this one you did not run, named concretely]
R3. [Pressure test: the load-bearing assumption in the answer, and what breaks it]
R4. [The path not taken: what this run held, deferred, or forked away from, as a route you could still take]
R5. [Leverage or inversion: the smallest move that changes the most, or the frame flipped]
```

R2 and R4 use the routing table and the run's own structure, so they name real next invocations, not abstractions. R1, R3, R5 are thinking angles.

**When it fires:** every run that surfaced a Beast-Mode Prompt block. **When it does not:** trivial or downgraded runs, refusals, pure file confirmations, mid-flow clarifying turns. If a slot cannot be filled with a sharp, run-specific line, skip the tail rather than pad it. If another skill in the session already appends closing routes, this tail replaces it on beastmode responses. Never print two.

## Step 11: Bank the run (silent, always)

The log is `.skills-data/beastmode-log.md`.

**Read before you write.** Read the last 10 entries (Standing moves were read at Step 4), then append:

```
## YYYY-MM-DD | [3-6 word slug]
RAW: [raw prompt, one line]
AMPLIFIED: [what the rewrite actually changed, one or two lines]
ROUTE: [class -> skill(s) used]
ROUNDS: 1
OUTCOME: pending
```

**Backfill.** Once the user's next message reveals it, set OUTCOME to `accepted`, `redirected`, or `abandoned`, followed by `User changed: [what they altered, cut, or corrected]` or `User changed: none`. That clause is the learning signal. Edit only the entry this session wrote, anchored on its exact `## date | slug` header. Never match a bare `OUTCOME: pending`; a global replace corrupts every prior entry. Silence past the following exchange stays `pending`. Revision rounds increment `ROUNDS` on the existing entry.

**Escalation.** If the move you just logged appears in 3+ of the last 10 entries and is not already in Standing moves, propose it as a standing default: one line in chat, after the answer. Propose, never apply. On the user's yes, add it to Standing moves with the date and tag the triggering entries `[escalated]`. Never prune entries.

This log is the only read on whether the skill earns its keep: what the user changes after accepting, tracked over time.

## Clause bank

Modular instructions that change outputs by forcing a behavior rather than requesting a quality. Injection rule in Step 4: at most three per run, only where they raise the ceiling, never where the matched chain owns the behavior. Writing clauses are deliberately absent; the content skills own that lane.

**Research / analysis**

- Trace repeated claims to their earliest accessible source; publications repeating one source are not independent corroboration.
- Distinguish when something happened from when it was reported.
- Search deliberately for credible counterevidence before concluding.
- Name what the available sources cannot establish.
- Stop when another search is unlikely to materially change the answer.

**Strategy / decision**

- Identify the few variables most capable of changing the outcome.
- State what must be true for this to work.
- Distinguish reversible decisions from irreversible commitments.
- Test whether the choice can be staged, hedged, or converted into a cheap experiment.
- Show which changed assumption would reverse the recommendation.
- Find the actual bottleneck rather than optimizing adjacent activity.

**Idea generation**

- Identify the predictable answer clusters first and treat them as an exclusion list.
- Novelty must live in the mechanism, not the presentation.
- Do not average several familiar ideas into one.
- Reject any idea whose novelty disappears when renamed plainly.
- Include one idea that sounds wrong until its mechanism is explained.

**Creative direction / visual**

- Begin with the meaning the work must communicate before selecting aesthetics.
- Translate abstract adjectives into observable visual decisions.
- Define what must remain invariant across every execution.
- Judge the concept at thumbnail size and at full resolution.
- Keep a kill-list of elements that would make the work generic.

## Output

In order, every substantive run:

1. Scope questions, if Step 6 fired.
2. The `## Beast-Mode Prompt` block, six sections, plus a one-line fork if one surfaced.
3. Under `--review`: the `## What changed` block, then stop.
4. The final deliverable, verbatim in chat.
5. The downgrade note, if the prompt did not need amplification.
6. R1 through R5.

Silent, every run: the self-critique pass and the log entry.

## Boundaries

- Manual invocation only. Never auto-fire on "improve this prompt" or any unslashed ask.
- Amplify precision, never scope. A 10x version is a fork the user picks, never a default.
- Respect every decision gate the user set in the raw prompt. Generate to it, stop at it.
- Any action on the user's behalf (send, post, schedule, publish, share): draft only. Never execute without an explicit yes in the current message.
- Before proposing a change to files, config, or systems: state what exists today, what changes, and what breaks if wrong. Propose, never apply.
- Quality bar before delivery: would the user stop scrolling, does it read AI, is this the simplest version that lands, would they sign it.
- Flag uncertainty before stating it. Label non-trivial claims fact, inference, or assumption when challenged.
- Never deliver raw fan-out output. Never narrate the chain between the block and the answer.
