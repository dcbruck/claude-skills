---
name: ghost
description: Manual voice-locked content drafter. ONLY triggers when the user explicitly types /ghost followed by a content type and topic (e.g. "/ghost email to Acme confirming kickoff" or "/ghost newsletter section on AI brand voice"). Do NOT auto-fire on natural-language asks like "draft me an email" or "write a newsletter". /ghost is the explicit slash command for non-LinkedIn written content (emails, proposals, newsletters, scripts, page copy, pitch deck copy, podcast intros, general copy). It loads the user's voice profile and kill list, drafts from every voice dimension, runs a seven-step audit gate, and returns the clean draft only. Refuses to skip the audit. LinkedIn posts are out of scope; use /fleet for episode-derived posts or draft them directly. Not for auditing pasted text or remixing a long-form source.
license: MIT
metadata:
  version: 1.0.0
  author: Drew Brucker
  source: https://github.com/dcbruck/claude-skills
---

# /ghost: draft and audit in one non-skippable call

/ghost drafts a piece of written content in the user's voice, then runs it through a seven-step audit gate before anything leaves. The gate is invisible. The user pastes the slash command; the output is the clean draft. The one failure it exists to prevent: a draft that reads as machine-written because the voice was loaded but the tells were never hunted, or the tells were hunted so hard the voice got flattened.

## Setup

Two files, both at the project root by default. Paths below are the defaults; the user can point the skill elsewhere.

| File | What it is |
|---|---|
| `voice-profile.md` | Your voice profile. Build one with the template in `templates/voice-profile.md`. The template ships with these dimension slots: sentence patterns, vocabulary, verbal tics, pronoun strategy, emotional temperature, pacing and density, metaphor domains (and the ones you never use), transition logic, audience register, sign-offs. It should also carry a tone spectrum: which register each content type gets. |
| `kill-list.md` | Your list of writing tells to hunt, grouped by severity (soul-level, voice-level, structural, surface). A starter lives at `templates/kill-list.md`. |

Optional extras. If you keep an email playbook, a metaphor bank, a bio file, or a project design direction, load it here for the matching content type. If you keep project writing and formatting rules (CLAUDE.md or equivalent), they apply. Assume them.

Flags:

- `--no-voice`: if you have no voice profile yet, add this flag and the skill drafts in a clean, plain, first-person register and skips the voice-fidelity checks. The kill-list scan still runs. If `kill-list.md` is also missing, the skill uses the tells named in gate step four as its minimum list.

## Trigger

Fires only on the explicit slash form:

```
/ghost [content type] [topic / thesis / context]
```

Examples:

- `/ghost email to Acme confirming Monday kickoff and Net 15 terms`
- `/ghost proposal section: scope of work for the Q3 engagement`
- `/ghost newsletter: why a brand-voice plugin does not solve the personal-name problem`
- `/ghost script: 90-second keynote intro on the cost of voice drift at scale`
- `/ghost page copy: hero section for a consulting site`

Does NOT fire on "draft an email," "write a newsletter," or "put together copy." Those are ordinary requests, handled outside this skill.

LinkedIn posts are out of scope for /ghost; use /fleet for episode-derived posts or draft them directly. Auditing already-written text and remixing a long-form source are also out of scope.

## Step 1: load the required files (refuse if missing)

Before writing a word, confirm `voice-profile.md` and `kill-list.md` are in context. If either is missing and `--no-voice` was not passed, stop. Reply: "Missing `voice-profile.md` (or `kill-list.md`). Attach it, point me at it, or re-run with `--no-voice`." Do not draft.

Load any optional file that matches the content type (email playbook for emails, design direction for page copy, bio file for anything needing credentials).

## Step 2: route the content type

Identify the content type from the command. Each type gets a workflow:

| Content type | Workflow |
|---|---|
| Email (opportunity response, client update, group alignment, accept, decline, relationship maintenance, follow-up) | Email workflow |
| Pitch or proposal email | Email workflow AND the full gate, both |
| Proposal section, SOW prose, contract narrative | Email workflow AND the full gate, both |
| Newsletter | General workflow |
| Script (keynote, podcast intro, video, pitch deck) | General workflow |
| Page copy, landing page, hero, pricing page | Page-copy workflow |
| Anything else non-LinkedIn | General workflow |

The workflows:

- **General:** lock register, calibrate the opener, draft in full, run the gate.
- **Email:** lock register and temperature, identify the email archetype (response, update, alignment, pitch, quick accept, quick decline, maintainer, follow-up) and thread position, calibrate the opener, draft in full, run the gate plus the email checks in step 8.
- **Page copy:** lock register from the design direction if one exists, draft section by section against the page's job, draft in full, run the gate with the specificity scan weighted heaviest.

If the content type is unclear, ask the user before drafting. Do not guess.

## Step 3: match the register (mandatory)

Open `voice-profile.md`. Find the tone spectrum. Lock the register for this content type before writing anything. A client email and a newsletter sit at different slang levels. Get this right first.

For emails, also lock the temperature (warm, warm-to-hot, controlled warm, cool-to-warm, cool, or matches sender) and the planned sign-off from the profile's sign-off rules.

For page copy, pull register from the design direction if loaded. Measured visual direction means deliberate copy; sharp visual direction means faster rhythm.

## Step 4: calibrate the opener (hard gate)

Write the opening paragraph only. Do not draft past it yet.

Run the opener against eight checks:

1. Would the user actually say this?
2. Is there a single sentence they would be embarrassed by?
3. Does it sound like AI wrote it? Scan it against the kill list.
4. Is it too safe?
5. Is there unnecessary setup?
6. Is the temperature consistent?
7. Is there any lived experience bleeding through?
8. Are the human patterns earned, or performed?

If the opener fails any check, rewrite the opener. Do not draft past it until calibration passes. This catches voice drift before it contaminates the full draft.

For emails, also confirm: the warm opener matches relationship depth (or is skipped when there is nothing genuine to say), the greeting matches the profile's default, and the ask or deliverable is visible within the first three sentences.

## Step 5: draft the full piece

Draft using every dimension your `voice-profile.md` defines: sentence patterns, vocabulary, verbal tics, pronoun strategy, emotional temperature, pacing and density, metaphor domains (and the ones the profile forbids), transition logic, audience register, sign-offs. The specific values are the user's. The skill's job is to apply all of them, not a favorite few.

Rules that hold in any voice:

- Deploy tics during drafting, not as a retrofit. Mid-write placement reads natural; bolted-on placement reads like a checklist.
- Shift pronouns at least once. A uniform pronoun is a flat voice.
- Vary temperature. No more than three consecutive paragraphs at the same intensity.
- Density runs compressed opener, breathing middle, dense pivot, compressed closer.
- Zero moves is always acceptable. Forcing a signature move is the performative-human failure.

For emails, additionally apply the email archetype's shape and the profile's email-specific patterns (greeting, availability signal, friction removers, the strategic closing question). Thread position matters: first email carries the full archetype, second is shorter, third is firmer.

For page copy, layer standard copywriting principles under the voice: one job per section, the reader's problem before the offer, one call to action.

## Step 6: run the seven-step gate

Every step runs. None is skippable.

**One: opener calibration.** Re-run step 4 against the opener now that the full draft exists. Confirm it still passes in context.

**Two: full draft from the voice profile.** Confirm every dimension the profile defines shows up somewhere in the piece. A missing dimension means a thin draft, not a clean one.

**Three: kill-list scan, soul first.** Read `kill-list.md` top to bottom against the draft in severity order: soul-level tells (performed confidence, false vulnerability, unanchored authority), then structural tells, then surface tells. Fix in that order. A surface fix on a soul-level problem is polish on a corpse.

**Four: high-escape scan, named in words.** These slip past most reads because each one mimics a real writer's move. Hunt each one by name:

- Negate-then-assert, in every costume: "X isn't Y, it's Z," "not because A but because B," "didn't change, did," "stops being, becomes," the perspective pivot ("from where they sit X, from where I sit Y"), and the mirrored demonstration pair. Uncontracted forms count. Zero tolerance in any voice, earned or not. State the positive directly.
- Trio lists: always-three enumeration when the real count varies. The in-sentence variant counts too. Cut to two, render one fully specific, or break the parallel syntax.
- Concluding summary: a final paragraph that rephrases without adding, and its cousin the aphoristic-maxim closer. Land on a concrete instead.
- Post-insight explanation: an insight followed by its own explanation ("Which means..." "In other words...").
- Analogy overexplain: mapping the metaphor's parts back to the literal subject.
- Label-colon reveal: a bolded label, a colon, then the point.
- Restatement staircase: the same idea climbing through three phrasings.
- Command cascade: a run of imperatives standing in for an argument.
- Contraction avoidance: "cannot," "do not," "it is," "that is" where speech would contract. Contract every instance; one deliberate stress beat per piece maximum. It hides in sentence openers and modal negatives.

Also fragment stacks used for enumeration, sweeping-history openers, importance puffery, and superficial "-ing" analysis.

**Five: human-pattern check.** Two markers must appear: real paragraph-length variance (not metronomic long-short-long-short) and one specific odd detail that only a person who was there would include. Then scan the five failure modes: the guru (punchy and unanchored), the framework robot (a taxonomy where a thought should be), the safe contrarian (a take that costs nothing), the enthusiastic explainer (teaches cleanly, no stakes), the performative human (tics present, music missing). Specificity scan runs here too: every claim, metric, and time reference checked; "many years" becomes a number.

**Six: proportionality check.** The only step that pushes back. Every step above cuts, kills, or replaces. This one holds the post-audit draft against the pre-audit draft and asks: did any fix cost more than the tell did? Is any paragraph flatter, safer, or more generic than before the gate ran? Did every change trace to a named pattern, or did some happen for tidiness? Revert anything changed for polish alone. A draft that passes every pattern and sounds like nothing has failed.

**Seven: present clean.** No audit log. No notes on what was caught.

Three-strike rule inside the gate: if three or more tells survived any single scan, rewrite that section silently. Do not flag it. Fix it invisibly.

With `--no-voice`, steps one, two, and the voice-fidelity half of five are skipped. Three, four, six, and seven still run in full.

## Step 7: borrowed-voice and batch rules (when either applies)

**Borrowed voice.** If the request asks for a draft in another writer's voice (a named author, a house style, a client's brand voice), load that profile but never let it suspend the kill list. The emulated writer's own signatures are the highest-risk smuggling route for the exact tells this skill hunts, because the tell reads as faithful imitation. It is still a tell. Zero negate-then-assert regardless of how often that writer "really" does it. The maxim closer stays killed. No period-stacked trios in any voice. On any collision between the borrowed profile and the kill list, the kill list wins.

**Batch output (two or more pieces in one delivery).** Audit the set, not just each piece. Lay them side by side:

- Closer shape: no two pieces end on the same move.
- Skeleton: no two pieces run the same template (setup, same pivot, same close).
- Recurring framing: no phrase or structure recurs across three or more pieces. Let one piece own it; strip the rest.

A batch fails if any of these fire, even when every piece passes solo.

## Step 8: email checks (emails only)

After the gate, run these nine on any email:

1. Ask or deliverable visible in the first three sentences?
2. Clear next step at the close?
3. Sounds like the user?
4. Warm opener earned, matching relationship depth?
5. Sign-off matches temperature, per the profile?
6. Spot-check for over-formality ("Per our previous conversation," "Please don't hesitate to reach out," "I wanted to take a moment to"), negate-then-assert in email costume ("the challenge," "the issue," "the problem" framed as a negation then a correction), post-insight explanation, and the bullet flood (bullets for arguments instead of inventory)?
7. Length appropriate? Ultra-short is two to four sentences. Short is one paragraph. Medium is three to six paragraphs. Extended is for pitches and group emails only.
8. Thread position respected (first email full, second shorter, third firmer)?
9. Sign-off matches the profile, never a stock formal closer the user would not use?

Then scan the five email failure modes: the template robot (every sentence a stock phrase), the over-explainer (four paragraphs before the ask), the passive closer ("just wanted to check in," no next step), the overseller ("uniquely positioned to deliver"), and the hedge pile ("I was wondering if perhaps we might consider"). Rewrite any section that matches.

Pitches and proposals run both the email checks and the full gate. Not one or the other.

## Step 9: final self-verification

Before output, confirm internally: required files loaded (or `--no-voice` passed), workflow identified, register locked, opener passed all eight checks, full draft used every profile dimension, all seven gate steps ran, borrowed-voice and batch rules ran where they applied, email checks ran if email. If any item is unchecked, return to that step and re-run. Do not output until every item passes.

## Output

The clean draft only. Nothing else.

- No audit log
- No "Here's your draft" preamble
- No commentary on which move or structure was used, unless the user asked
- No mention of the workflow that ran
- No restatement of the topic

Just the draft.

## Boundaries

The skill refuses to proceed when:

1. **A required file is missing** and `--no-voice` was not passed. Stop, name the file, do not draft.
2. **"Skip the audit" is requested.** Refuse. The audit is the product. Without it the draft is just AI writing.
3. **"Just give me a quick draft" is requested.** Refuse. /ghost is the full-enforcement skill. Fast unaudited drafts happen outside it.
4. **Two rewrite cycles cannot pass the gate on the same section.** Surface the specific blocker (which gate step, which tell, which voice element). Do not ship a failing draft.
5. **The content type is a LinkedIn post.** Out of scope. Use /fleet for episode-derived posts or draft them directly.
6. **The request is audit-only on pasted text, or a remix of a long-form source.** Out of scope.

It never:

- Builds voice profiles (fill the template in `templates/voice-profile.md`)
- Modifies `voice-profile.md` or `kill-list.md`. Those are sources of truth. The skill loads and enforces them.
- Surfaces the gate. The user sees the draft.
