---
name: fleet
description: "Manual episode-to-content fleet. ONLY triggers when the user explicitly types /fleet with a transcript (attached .txt, pasted text, a file path) or an episode reference such as \"ep 12\" resolved through a connected recording tool. Do NOT auto-fire on \"make content from this,\" \"remix this,\" or general content asks. Takes one long-form spoken-word source and fans it out into a configurable content set (LinkedIn posts, short-platform companions, ranked clips, a subscriber newsletter section, a show-page newsletter, and optional long-form editions), each piece drafted in the user's voice, self-audited against the kill list, and differentiated across the batch. Speaker-aware. POV ownership: personal-channel pieces never name co-hosts or guests. Stops and asks before touching anything that looks like a private or client call."
license: MIT
metadata:
  version: 1.0.0
  author: Drew Brucker
  source: https://github.com/dcbruck/claude-skills
---

# /fleet: one episode in, a full content set out

/fleet takes one spoken-word source (a podcast episode, a talk, a recorded conversation) and fans it out into a full slate of on-voice, audited content. Every piece is drafted from real seed material, gated against the kill list on its own, then scanned against the rest of the batch. The one failure it exists to prevent: ten posts that are one idea in ten outfits, each of which passes solo and all of which read the same.

## Setup

Files, project root by default:

| File | What it is |
|---|---|
| `voice-profile.md` | Your voice profile. Build one with the template in `templates/voice-profile.md`. |
| `kill-list.md` | Your list of writing tells to hunt. A starter lives at `templates/kill-list.md`. |
| `.skills-data/transcripts/` | Saved raw transcripts. Optional. |

If you keep a hook library, a short-platform playbook, or an AI-search optimization guide, load it here. If you keep project writing and formatting rules (CLAUDE.md or equivalent), they apply. Assume them.

Names. Fill once:

| Name | Value |
|---|---|
| Author name (the personal-channel voice) | |
| Show name | |
| Show brand page (LinkedIn or equivalent), if any | |
| Long-form newsletter name, if any | |

Output set. Edit the counts. Mode A default:

| Output | Default |
|---|---|
| LinkedIn posts | 10 |
| Short-platform companions (X or equivalent), one per post | 10 |
| Ranked short-form clips with timestamps | 10 |
| Subscriber newsletter section | on |
| Show-page newsletter | on |
| Long-form editions (A: thesis essay, B: operator piece) | off |

Override at call time: "/fleet just posts," "/fleet 6 posts, no clips," "/fleet with editions."

Integrations, all optional. If a recording or transcript tool is connected (Riverside, Fathom, Granola, or similar), resolve "ep 12" there; otherwise the user attaches the transcript.

Flags:

- `--no-voice`: no voice profile yet. Drafts in a clean, plain, first-person register and skips voice-fidelity checks. The kill-list gate still runs.

## Trigger

Fires only on the explicit slash form:

```
/fleet [transcript, file path, or episode reference] [overrides]
```

Examples:

- `/fleet ep 12`
- `/fleet transcripts/2024-q3-panel.txt`
- `/fleet [pasted transcript] 6 posts, no editions`

Does NOT fire on "make content from this," "remix this," "turn this into posts," or any general content ask.

## Input

A transcript: attached .txt, pasted text, a file path, or an episode reference. Nothing else is required.

**Episode reference.** If a recording or transcript tool is connected, resolve "ep 12," a title, or a URL there. Match on title, participants, and date; when two recordings could fit, confirm the match in one line first. Pull the speaker-labeled transcript. Timestamps often arrive as `m:s` with no hour rollover; convert to `H:MM:SS` before writing any clip timestamp. If a long transcript lands in a file, read it in chunks until the whole thing is covered. Never work from a partial read.

If no tool is connected, the user attaches the transcript. Speaker labels drive the origin tags in Step 2. If there are none, ask which speaker the user is before drafting.

Save the raw transcript to `.skills-data/transcripts/<show>-<episode>.md` as an append-only block so repeat runs and sibling skills (/mine, /youtube) share one ground truth.

Clip timestamps verify at word level when the tool exposes an aligned transcript; otherwise against the transcript text. State the method in the delivery.

## Step 0: read the source and classify it (never skip)

Skim the transcript first and pick the mode. This sets the framing and the output slate.

**Mode A: the user's own show (default).** The user is a speaker: their own podcast, a solo episode, or a guest spot they did on someone else's show. Draft first-person, their takes, their channels. Full slate.

**Mode B: third-party source.** The user is NOT a speaker (someone else's podcast, a talk, a video they are mining for ideas). Draft as the user's COMMENTARY on the source. Credit the source by name. Never put another person's insight in the user's mouth; frame it as "I heard X make this point, here's my angle." Drop the clip package and the show-page newsletter (those belong to the source's channels). Deliver posts, companions, a subscriber newsletter angle, and a long-form edition only if the material earns a thesis. POV ownership below does NOT apply to Mode B. Credit there is ethics.

**Mode C: private or client call (STOP).** If it reads like a business meeting or anything confidential (named clients, deal terms, internal strategy), stop. Do not draft. Surface one line: "This looks like a private or client call, not publishable material. Want internal notes instead, or is this meant to be public?" Wait for the user.

## Step 1: load the voice chain

Load `voice-profile.md` and `kill-list.md`. If either is missing and `--no-voice` was not passed, stop and say which one. Load any optional playbook named in Setup.

## POV ownership on personal channels

Every personal-channel piece (posts, companions, long-form editions) is written from the user's perspective and owns its angle outright. No named third parties: not the co-host, not guests, not "my co-host." When an idea originated with someone else on the show, the ceiling is ONE nameless allusion per piece ("this came up on the podcast"). Most pieces should skip even that, and the allusion may appear in at most three pieces per batch. A recurring allusion is its own sameness tell.

**The honesty line underneath it: perspective becomes the user's, facts stay honest.** Never present someone else's lived experience, stat, or story as the user's own. If a seed's spine IS someone else's story, reframe it to the user's angle on the topic at the seed stage or cut it. A one-line supporting beat may survive anonymized ("a creator friend with a large following"). Compressing a name to an allusion is style. Absorbing someone's experience is theft.

**Exempt:** the subscriber newsletter and the show-page newsletter (the show talking about itself, full names, full credit) and all Mode B output.

## Step 2: mine the source (two-pass extraction)

Read the full transcript. Pull the strongest seeds: verbatim quotes, timestamps, the angle each supports, why it stops the scroll. **Tag each seed's origin: mine / co-host / guest / shared.** Co-host and guest seeds get converted to the user's angle inside the seed brief, before any draft begins. If the brief never contains the third party, the draft cannot either. Seeds that cannot be honestly reframed get cut.

Assign each post-seed a distinct hook shape and structure (from your hook library if you keep one; otherwise vary deliberately: question, claim, scene, number, confession). Funnel balance across the post count: roughly half education, a third awareness, the rest conversion. If editions are on, also tag the episode's strongest THESIS material (feeds Edition A) and strongest ACTIONABLE segment (feeds Edition B).

**Seed depth guard.** Ten posts requires ten genuinely distinct seeds. If the episode only carries seven (including after POV-rule cuts), ship seven and say so. Eight clean seeds beat ten with two borrowed spines. Same for editions: an episode that carries only one long-form piece ships Edition A alone, flagged in delivery. Never pad.

## Step 3: fan out

If the environment supports subagents, run this as a graph. Otherwise run it sequentially in the same order, auditing each piece before starting the next.

- **Draft (fan out):** one agent per post-seed, each loading the voice chain and drafting against its assigned hook and structure, building ONLY from real seed material (no invented facts, stats, names, events). Each drafting contract includes the POV ownership rule. In parallel: one agent extracts and ranks clips with verified timestamps (Mode A only), one drafts the subscriber newsletter section, one drafts the show-page newsletter, and if editions are on, two draft Editions A and B (Step 3c).
- **Audit (per piece):** each draft flows straight into its own gate against `kill-list.md`. Soul-level tells first, then the high-escape scans: negate-then-assert in every costume, concluding summary and the maxim closer, trio lists, fragment stacks, contraction avoidance, label-colon reveal, restatement staircase, command cascade. Returns the cleaned piece.
- **Companions (after post audits):** once the posts clear their gates, draft one companion per post (rules in Step 3a), then gate them as a batch.
- **Batch scan (barrier):** one agent reads the whole set and flags shared closers, shared skeletons, and any framing, word, or attribution recurring across three or more pieces. No companion may share its hook line verbatim with its parent post. POV scan: zero third-party names across personal-channel pieces; podcast allusions at most one per piece and present in no more than three pieces. Edition scan: Editions A and B may not share a thesis, skeleton, or closer shape with each other or with any post. Pet vocabulary counts toward recurrence limits like any other framing. This catches the sameness individual audits miss.

## Step 3a: short-platform companions

One per post, native to the short platform, never a compression of the parent:

- Hard cap 40 words. Aim under 25.
- One idea per companion: the sharpest single claim from the seed.
- No hashtags. No "thread below" energy. No links in the body.
- The hook does all the work: the first seven words decide the impression. Questions and open loops earn replies; specific numbers earn bookmarks; one-liners the reader would post to speak for themselves earn reposts.
- Write for the community the user lives in on that platform. Domain-specific terms are a feature.
- Full kill-list gate still applies: zero negate-then-assert, zero em dashes, contractions throughout, no maxim bows. A 25-word piece can still bow.
- POV ownership applies at this length: no names. Skip even the podcast allusion and own the claim outright.

## Step 3b: show-page newsletter

Written as the show's brand page. Third person on the hosts and guest, with a real editorial point of view and traces of self-deprecating humor about the hosts. Structure: the episode's most salient ideas, what each means, why it matters. Never a press release. POV-exempt: full names and credit stay.

## Step 3c: long-form editions (when on)

Two editions of the user's long-form newsletter per Mode A run.

**Edition A: the thesis essay.** One novel, defensible claim about what is happening in the user's field, built from the episode's strongest material but standing alone. The piece someone links to explain the shift. 1,000 to 1,800 words. Invisible spine.

**Edition B: the operator piece.** The exact system, setup, or play, from inside, born from the episode's most actionable segment. The piece someone bookmarks and works through. 800 to 1,200 words. Prose throughout with exactly ONE labeled anchor, a bolded "**Steal this:**" tag on the stealable block. Nothing else labeled.

**Both share the five-beat anatomy:** cold-open thesis in the first 100 words (citable claim before the fold), receipts block (a lived anchor: system, number, client moment), the build (deep middle), the stealable (one artifact the reader takes), hard-stop closer (image or fact, no summary, no bow).

**Rules for both:**

- **Entity discipline:** the newsletter name and the author name appear together in the first paragraph of every edition. This is how a contested name string gets owned.
- **Attribution under POV ownership:** attribute to the show, never to people. Guest- or co-host-owned stats carry show-level attribution or an anonymized one-line beat, or they get cut.
- **Sibling link:** each edition ends with one line pointing at the other.
- **Scheduling:** staggered, A early week, B later the same week. Never both in one notification cycle. Label target slots in delivery.

## AI-search checklist (show-page newsletter and both editions must pass all of these)

The goal is being quoted by LLMs and AI search engines. Extractability comes from claims, never scaffolding:

1. **One named, defined concept per piece** that an LLM can lift whole. The definition lands in the first third, in one clean sentence.
2. **Standalone citable sentences:** claim plus number plus attribution in a single sentence. Four to six per piece. Each must survive being quoted with zero surrounding context. On personal-channel pieces the attribution entity is the author, the newsletter, or the show.
3. **Entity consistency:** full names on first use, consistent naming after. Host and guest names apply to the show-page newsletter only.
4. **Question-shaped section turns rendered as prose,** never FAQ headers. The turn a reader would search for gets answered in the next sentence.
5. **Statistics carry dates and sources.** A number without attribution is a rumor to a retrieval system.
6. **Fluency beats density.** Citation, statistics, and clarity drive visibility; keyword stuffing is actively negative.
7. **The tension rule:** retrieval structure and the kill list collide at scaffolding (headers-as-questions, listicle bones, definition boxes). The resolution is always extractable CLAIMS woven into narrative prose. The single sanctioned exception is Edition B's "Steal this:" anchor.

## Step 4: differentiate (the final cut, always)

The batch scan almost always finds collisions. Fix them so the set reads as N distinct pieces: break twinned skeletons, let one piece own each recurring word or thesis, vary closer textures, thin any over-used device (a repeated hand-off phrase, a recurring podcast allusion, emphasis formatting in more than half the pieces). Companions get their own pass: no two may share a grammatical hook shape. This is the editorial pass. Do not skip it even when each piece passes solo.

## Step 5: verify (read-through plus factual)

Re-read every piece against `kill-list.md` once more after differentiation moved things. Fix what surfaced. Then verify every clip timestamp and every quote against the transcript (word level when the tool exposes an aligned transcript). No fabricated timestamps, no fabricated quotes. Retrieval pieces get one extra pass: read each citable sentence alone, out of context; if it needs the paragraph around it to be true, tighten it. Final POV pass: search the personal-channel pieces for third-party names, and confirm both editions carry the newsletter name and author name in the first paragraph.

## Step 6: deliver

Present the pieces; the user picks. Show the full set in the chat, verbatim, and deliver one handoff .md file.

## Output

1. Every post, in full, labeled: hook shape / structure / funnel stage / source timestamp
2. Each companion directly under its parent post
3. Subscriber newsletter section
4. Show-page newsletter
5. Editions A and B (when on), each labeled with its publish slot
6. Ranked clips with `H:MM:SS` in and out points and the verification method
7. Flags: a post that needs one real metric, two posts to space apart on the calendar, a citable claim worth reusing, seeds cut by the POV rule, a one-edition run and why
8. One handoff .md file containing all of the above

## Boundaries

- Every factual anchor comes from the transcript. Voice and framing are the user's; facts are the source's.
- POV ownership on personal channels: no named third parties, one nameless podcast allusion max per piece, allusions in at most three pieces per batch. Show-channel pieces and Mode B keep full credit. Never absorb someone else's lived experience as the user's.
- Entity discipline on editions: newsletter name plus author name in the first paragraph, no exceptions.
- Full kill-list gate on every piece, including the 25-word ones. Zero negate-then-assert, zero em dashes, zero banned words, contractions throughout, no maxim closers.
- The batch is audited as a batch, not just each piece alone.
- Retrieval structure never wins a collision with voice.
- Stops on anything that reads as a private or client call. Asks; does not draft.
- Never pads to hit the configured counts. Ships what the episode carries and says so.
- Not for general content asks or drafting a single piece from a brief.
