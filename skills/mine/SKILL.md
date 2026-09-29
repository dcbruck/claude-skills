---
name: mine
description: Manual transcript miner, idea-library builder, and library query tool. ONLY triggers when the user explicitly types /mine followed by a source reference (transcript file path, pasted transcript, a meeting or video URL, multiple URLs, an episode reference such as "ep 12" resolved through a connected recording tool, or "this session"), /mine ask followed by a question, or /mine pin followed by quotes to anchor. Do NOT auto-fire on "summarize this transcript," "what did they say," or content-creation asks. /mine deposits sources into a permanent idea library, runs collision, disagreement, and architecture passes against everything already banked, answers questions from the library with receipts, and auto-runs a synthesis (emergent thesis, trajectory, consume/publish gap) every five deposits.
license: MIT
metadata:
  version: 1.0.0
  author: Drew Brucker
  source: https://github.com/dcbruck/claude-skills
---

# /mine: every transcript becomes a permanent, cross-referenced deposit

/mine turns a transcript into an atomized deposit in an idea library, then collides that deposit against everything already banked. The library answers questions later, with timestamps, so the user can pull the receipt. The one failure it exists to prevent: reading a transcript once, taking two notes, and never seeing it again. /mine banks and retrieves; drafting skills pull from what it banked.

## Setup

Files, project root by default:

| File | What it is |
|---|---|
| `.skills-data/transcripts/` | The library. One deposit file per source. |
| `.skills-data/transcripts/index.md` | The library's spine. Four blocks: Positioning, Theme vocabulary, Deposits (one row per deposit), Anchors (pinned lines), Synthesis (dated entries). Created on first run if missing. |
| `.skills-data/transcripts/mine-log.md` | One row per run: date, source, lane, deposit slug, source id. Drives the re-mine guard. |
| `voice-profile.md` | Your voice profile. Optional. Used for D versions in `/mine pin` and the Self-lane voice pass. Template in `templates/voice-profile.md`. |
| `kill-list.md` | Your list of writing tells to hunt. Optional. Starter in `templates/kill-list.md`. |
| `.skills-data/content-seeds.md` | Where approved content seeds get banked. Optional. |

Positioning block. Fill it once at the top of `index.md`, 3 to 6 lines: what you do, who you sell to, the audience you publish for, the claim you want to own. Every collision pass reads it. Without it, collisions get generic.

If you keep a hook library or a file per prospect, the skill offers to append to them. If you keep project writing and formatting rules (CLAUDE.md or equivalent), they apply. Assume them.

Integrations, all optional. If a recording or transcript tool is connected (Riverside, Fathom, Granola, or similar), resolve "ep 12," a meeting URL, or a recording title there; otherwise the user attaches or pastes the transcript. A video URL needs transcribing first; if no transcription tool is available, ask for the transcript.

## Trigger

Fires only on the explicit slash forms:

```
/mine <source, or several sources>
/mine ask <question>
/mine pin <quotes, numbers, or "these">
```

Examples:

- `/mine transcripts/acme-founder-interview.txt`
- `/mine ep 12`
- `/mine ask what does the library say about pricing creative work by outcome`
- `/mine pin "the first three sentences decide the whole thing"`

Does NOT fire on "summarize this transcript," "what did they say about X," "make posts from this," or any content-creation ask.

## Three commands

**`/mine <source(s)>`**: deposit pipeline, Steps 1 to 9. Multiple sources queue through the same pipeline in one run; deliver one combined report, one section per source.

**`/mine ask <question>`**: query mode. No deposit. Read the Anchors block first (the user's curated canon outranks raw deposits), then the latest Synthesis entry (above raw deposits, below anchors), then the Deposits rows. Open every deposit whose themes touch the question and answer from banked claims with attribution: each point cites deposit slug plus timestamp so the user can pull the receipt. If the library is thin on the topic, say so in one line and name which kind of source would fill the gap. Use it before talks, posts, pitches, and calls.

**`/mine pin <quotes, numbers, or "these">`**: anchor mode. The user flags lines they attach themselves to, from a /mine report, a quote pull, or a paste. For each pinned line, append to the Anchors block of `index.md` three paragraphs: V (the verbatim quote with true attribution and timestamp), D (the same idea rebuilt in the user's voice, unique wording, no borrowed phrasing), and Use (post / talk / one-liner / framework). Before writing D versions, load `voice-profile.md` and `kill-list.md` and audit every D against the full kill list, plus banned words, em dashes, negate-then-assert structures, and hedges. If either file is missing, write D in a clean first-person register and flag that a voice pass is owed. One surviving machine pattern defeats a D version's purpose. Attribution accuracy is non-negotiable: if the speaker was quoting someone else (a tweet, a comedian, a circulating aphorism), the anchor says so. The Anchors block carries two usage rules at its top; keep them intact: spoken verbatim gets a "there's a saying that..." preface; written use is the D version only.

## Step 1: load the source and pick the lane

Parse everything after /mine:

- File path: read it
- Meeting or recording URL, recording id, episode reference: resolve through the connected tool
- Video URL: transcribe first, then mine
- Pasted text: use as-is
- "this session" or a past session the user names: pull the conversation transcript

**Resolving through a recording tool.** Match on title, participants, and recording date; when two recordings could fit, confirm the match in one line first. Pull the speaker-labeled transcript. Timestamps often arrive as `m:s` with no hour rollover (`63:20` means 1:03:20); convert to `HH:MM:SS`. If the harness saves a long result to a file, read it in chunks until the whole thing is covered. Save the raw transcript to `.skills-data/transcripts/<show>-<episode>.md` as an append-only block with the recording id on the source line, so sibling skills (/fleet, /youtube) share one ground truth. Record the recording id in the deposit header and the index row so the re-mine guard can key on it.

Then route by source type. The back half of the pipeline (Step 6) changes by lane:

- **Inspiration** (default): thinkers, operators, podcasts, talks the user wants as idea fuel
- **Prospect**: the speaker is someone the user might sell to or is preparing to meet
- **Self**: the user's own tape: their episodes, keynotes, interviews
- **Session**: the user's thinking captured in an AI chat session: ideas, reframes, decisions born in conversation

If the lane is ambiguous, pick the most likely one and name it in the report's first line; the user redirects if wrong.

## Step 2: locate the library and check for a prior deposit

The Theme vocabulary block in `index.md` is the controlled list of allowed tags. Each Deposits row reads: slug | speakers | source | mined | themes. Tags come from the vocabulary; add a new tag only when nothing existing fits, and add it to the vocabulary in the same edit. Freeform tags fragment ("volume" vs "reps") and quietly break collision lookup. The vocabulary is what keeps the library queryable at 50 deposits.

**Re-mine guard.** Check `mine-log.md` and the Deposits rows for this source before extracting. If it is already banked, do not create a duplicate: tell the user, then extend the existing deposit (new passes, updated collisions) instead of re-extracting. Session-lane deposits key on session id. Tool-sourced deposits key on the recording id as well as the episode number, since titles do not always carry the number.

If `.skills-data/` is not writable this session, build the deposit in the working directory, deliver it as a file, and flag that it needs filing. Never skip the deposit.

## Step 3: extraction pass (atomize)

Extract from the full transcript, never a skim. For sources over about 15K words, fan out subagents over segments and merge if the environment supports them; otherwise work segment by segment.

Capture every distinct:

- **Claim**: the idea in one tight sentence, with timestamp
- **Quote**: best verbatim line for that claim (1 to 3 sentences, filler stripped)
- **Framework**: named or unnamed repeatable models (acronyms, step sequences, operational definitions)
- **Story/number**: concrete anecdotes and specific figures worth citing later

Completeness beats curation here. The deposit is raw material; curation happens in the passes below. A claim that seems weak today collides into something sharp six deposits from now.

**Attribution and accuracy guard.** Caption-derived and non-diarized transcripts have no speaker labels. Attribute by context (">>" turn markers, names, who is interviewing); mark uncertain attributions "(likely X)". If a passage looks loopy or repetitive (ASR hallucination), flag it instead of banking it as fact. Wrong attributions poison every future quote pulled from the library.

## Step 4: write the deposit

One file: `.skills-data/transcripts/<speaker>-<source-slug>.md` (Session lane: `session-YYYY-MM-DD-<slug>.md`)

```markdown
# <Source title>
**Speaker(s):** | **Source:** <show, URL, recording id> | **Date:** <published> | **Mined:** <today>
**Themes:** 3-6 tags from the index vocabulary

## Claims
- [HH:MM:SS] Claim sentence. Q: "verbatim quote"

## Frameworks
- Name: one-line description [timestamp]

## Stories / Numbers
- [HH:MM:SS] One-line summary

## Collisions logged
(Step 5; future runs append here when they collide with this deposit)

## Angles
(Step 6 output: disagreement, outreach, voice, or thinking, per lane)

## Architectures
(Step 7: rhetorical structures worth stealing)
```

Add the Deposits row to `index.md` and the run row to `mine-log.md`.

## Step 5: collision pass

Every run collides against BOTH of these, always:

1. **The user's positioning**, from the Positioning block in `index.md`
2. **Prior deposits**: read the Deposits rows, skim the claims of any deposit sharing a theme

**Collision = claims meeting across sources inside the user's domain.** [Source A claim] x [Source B claim or the user's lived experience] x [the user's field] = a take nobody else can write. Single-source application is quotation; collisions are a point of view.

Log collisions in BOTH colliding deposit files so the connection is findable from either end. Skip any collision already logged.

## Step 6: angle pass (by lane)

**Inspiration lane: disagreement pass.** Find 3 to 5 places the source is wrong, incomplete, or breaks when applied to the user's world. "Where this breaks" outperforms "how this applies"; the user's strongest content lives in the gap between a famous claim and their contrarian field experience. For each: the claim, why it breaks, the one-line version of the user's counter.

**Prospect lane: outreach pass.** Replace disagreement with: their stated priorities, pain language worth quoting back, openings for the user's offer (from the Positioning block), and one first-line draft that engages with something they actually said. If the user keeps a file per prospect, offer to append a dated summary there.

**Self lane: voice pass.** The user disagreeing with themselves is useless. Instead: extract voice patterns (recurring phrases, sentence rhythms, metaphor habits, how they land a point) as proposed updates to `voice-profile.md`, and list the 3 to 5 most clip-worthy moments with timestamps as drafting candidates. Their own tape is the purest voice data they will ever get. Ask before writing to the voice profile.

**Session lane: thinking pass.** The source is the user thinking with an AI, so skip disagreement and voice. Extract: net-new ideas and frameworks born in the session, reframes that changed a decision's direction, decisions with their reasoning, and language sharp enough to reuse. Mark provenance on every claim: (user) for their own articulations, (session) for co-developed framing. The synthesis weights user-marked claims higher, and nothing marked (session) gets pinned as the user's own words without a rewrite they approve. Sessions have no timestamps; use message positions ([msg 14]).

## Step 7: architecture pass

Extract 2 to 4 rhetorical structures worth stealing: the shape of how the speaker lands points, never the points themselves. Example shape: vague label, then operational definition, then concrete example. Write each as a reusable pattern. If the user keeps a hook library, propose each as an addition and ask before writing; otherwise they live in the deposit's Architectures section. Session lane: skip unless the session produced a genuinely reusable shape.

## Step 8: publish bar, seeds, and report

**Publish bar.** Before anything reaches the user, every collision and angle passes three gates: Would it stop the scroll? Can only the user write it? Does it have a receipt (quote, number, timestamp)? Fail one, cut it silently. A short report where every line survives the bar beats a complete one that makes the user do the filtering.

**Seeds.** Propose the 2 to 3 strongest survivors as content seeds: core insight, hook angle, architecture suggestion, source tag. Ask before banking to `.skills-data/content-seeds.md`. Do not draft posts. Drafting belongs to the user's content skills.

**Report**, in chat, dense, this order:

1. **Deposit**: lane, filename, claim count, themes (one line)
2. **Collisions**: the survivors, one short paragraph each
3. **Angles**: disagreement / outreach / voice / thinking, per lane, two lines each
4. **Architectures**: the patterns, one line each, with the ask
5. **Seeds**: with the ask to bank
6. **Synthesis**: only when Step 9 fired: one-sentence headline of the strongest read
7. **Pulse**: one closing line: deposits in library, collisions total, which theme is heating up

No summary of the transcript itself. The user wants the angles, never a recap.

## Step 9: synthesis (auto)

Deposits record what the user consumed; the Synthesis block in `index.md` records what the accumulated curation reveals about them. Everything the user mines is pre-filtered through "this resonates," so the library is a pattern of attraction. The synthesis reads that pattern back.

**Firing rule, no manual lever.** After the report on every deposit run, read the State line at the top of the Synthesis block. If deposits added since the last synthesis are 5 or more, or no entry exists yet, run the synthesis in the same run and update the State line. There is no command to invoke it. If `index.md` is unreachable, note one line in the report that a synthesis is owed.

**Inputs.** The full library plus behavioral signals, weighted acted-on over merely banked: the Anchors block (what they pinned), approved seeds, then raw deposits. If the user keeps a log of published pieces, it ranks first. Resonance is inferred from behavior, never self-reported.

**Append one dated entry, three reads:**

1. **Emergent thesis.** What the curation reveals the user believes, articulated as tight claims. Every claim cites deposit slugs or anchor lines. Where a prior entry's thesis moved, name the delta explicitly. The delta is itself content.
2. **Trajectory.** What recent deposits signal about where the user is heading. Selection is aspirational: what they mine points at who they are becoming, before they have said it out loud. Name the direction plainly, no hedging.
3. **Consume/publish gap.** Themes with deposit density but thin or zero published work. If the user keeps a log of published pieces, classify them by library theme; otherwise ask once for the themes they have published on recently, or skip this read and say so. Each gap line: theme, deposit evidence, publish evidence, one-line read on the dormancy (next content lane, next business move, or noise).

**Receipts rule.** Any line without a receipt gets cut before it lands in the file. A synthesis of generic insight is worse than no synthesis at all.

Entries are additive, never rewritten. The report's Synthesis line carries the strongest read's headline; the full entry lives in the file.

## Output

Deposit runs: the deposit file, `index.md` and `mine-log.md` updated, the seven-part report in chat. Query runs: the answer with a slug plus timestamp receipt on every point. Pin runs: V, D, and Use paragraphs appended to the Anchors block and shown in chat.

## Boundaries

- Never extracts from a partial read. Never fabricates a timestamp, a quote, or an attribution.
- Never creates a duplicate deposit. The re-mine guard extends the existing one.
- Never drafts posts, emails, or scripts. Seeds only.
- Angles are commitments: "this breaks because X," never "this might not fully apply." If an angle would not survive the user asking "so what?", the publish bar should have caught it.
- A borrowed line never gets presented as the user's own.
- Not for summarizing a transcript, answering "what did they say," or any content-creation ask.
