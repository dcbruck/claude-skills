---
name: youtube
description: "Manual YouTube episode packaging. ONLY triggers when the user explicitly types /youtube with a new episode transcript (attached file, file path, pasted text, or an episode reference such as \"ep 12\" resolved through a connected recording tool). Do NOT auto-fire on \"write a YouTube description\" or similar. Produces the full upload package, in order: anchor themes and target queries, theme-anchored titles in two lanes plus one recommended hybrid, layered description, chapters, citable claims, pinned comment, caption fix list, cold-open pick, hashtags and tags, 10 ranked short-form clips with a bench, the upload Category/Type/Problems decision, and a paste-ready Promote targeting block (goal, locations, age, interests). Everything traces to the transcript, with timestamps verified at word level when the recording tool exposes an aligned transcript and flagged as sentence-level otherwise."
license: MIT
metadata:
  version: 1.0.0
  author: Drew Brucker
  source: https://github.com/dcbruck/claude-skills
---

# /youtube: one transcript in, the whole upload package out

/youtube takes a finished episode transcript and produces every field YouTube Studio asks for, plus the clips and the paid-promotion targeting, all anchored to the theme that spans the episode. The one failure it exists to prevent: a title that promises the episode's newsiest 15 minutes, a description that teases instead of answers, and chapter stamps that land two minutes from the words they name.

## Setup

Files, project root by default:

| File | What it is |
|---|---|
| `.skills-data/channel-profile.md` | Show facts. Read on every run. Template below. |
| `.skills-data/youtube-log.md` | One row per Promote campaign. Created on first run if missing. |
| `.skills-data/youtube-packages/` | Where each finished package is saved. |
| `.skills-data/transcripts/` | Saved raw transcripts, shared with /mine and /fleet. Optional. |

Fill `channel-profile.md` once. Copy this in and replace every bracket:

```markdown
# Channel profile

Show name: [name]
Hosts: [host names, as spoken and as spelled]
Audience: [who watches, in one sentence: e.g. marketers, creatives, and founders trying to use AI image tools]
Tone: [three words]
Canonical description: [the 2-3 sentence show blurb that closes every description]
Standard links: [site, newsletter, socials, one per line]
Brand terms for tags: [show name, host names, recurring segment names]
Garble-prone terms: [names and jargon captions get wrong, with the correct spelling]

## Audience baseline (from YouTube Studio's Audience tab, refresh quarterly)
Top countries by watch time: [country: percent]
Top countries by subscribers gained: [country: percent]
Age split: [bracket: percent]
Gender split: [percent]

## Confirmed Promote interest labels
[exact label as shown in the Promote picker, with (in-market) or (affinity)]
```

If you keep project writing and formatting rules (CLAUDE.md or equivalent), they apply to all written output. Assume them.

Integrations, all optional. If a recording or transcript tool is connected (Riverside, Fathom, Granola, or similar), resolve "ep 12," a recording title, or a URL there; otherwise the user attaches or pastes the transcript.

## Trigger

Fires only on the explicit slash form:

```
/youtube [transcript, file path, or episode reference]
```

Examples:

- `/youtube ep 12`
- `/youtube transcripts/ep12-agent-workflows.txt`
- `/youtube [pasted transcript]`

Does NOT fire on "write a YouTube description," "give me some title ideas," or any similar ask.

## Step 0: ingest

Locate the transcript. If /youtube was typed with no transcript attached, pathed, pasted, or resolvable through a connected tool, ask for it and stop.

**Resolving through a recording tool.** Match on title, participants, and recording date; when two recordings could fit, confirm the match in one line first. Pull the speaker-labeled transcript. Timestamps often arrive as `m:s` with no hour rollover (`63:20` means 1:03:20); convert to `H:MM:SS` before writing any chapter or clip timestamp. Save the raw transcript to `.skills-data/transcripts/<show>-<episode>.md` as an append-only block so /mine, /fleet, and this skill share one ground truth.

Read the FULL transcript before producing anything. For long transcripts, read in chunks (offset/limit) until the entire file is covered. Never work from a partial read.

Note whether the transcript carries timestamps. If it does not, every timestamp-dependent section below (Chapters, Cold-Open, Clips, Problems) must flag that instead of guessing.

## Step 0b: word-level timestamp verification

A prose transcript stamps each sentence, so a chapter or clip boundary taken from it can land two or three minutes from the words it names (a chapter stamped 1:03:24 when the phrase is first spoken at 1:00:42). Verification means the following, never a re-read of the prose.

1. If the connected tool exposes the episode's full-length edit and an aligned (word-timed) transcript, find that edit: the longest non-deleted one whose duration matches the episode (a clip edit runs under two minutes; the episode edit runs over an hour). If no full-length edit or aligned transcript exists, say so and fall back to prose stamps, flagged as sentence-level in the delivery.
2. For every chapter (Section 4), the cold open (Section 8), and every clip segment boundary (Section 10): read the aligned transcript on a window of about 90 seconds around the candidate stamp. The chapter or segment must start at the row where the named phrase, tool, or idea is actually first spoken. If the named phrase is not inside the window, widen it once, then move the stamp to where the phrase lives. Chapter stamps snap to the start of that row, floored to the second. Clip segment boundaries additionally use word-level detail on the exact first and last words in the segment table, so the in and out points are the true word times.
3. Aligned times are on the edit's playable timeline. Before trusting them as the published video's timeline, spot-check two rows against the prose transcript; if the playable times and prose times match within a second, the edit is a straight render and the chapters will match the upload. If they drift, the published video has cuts, and every stamp must come from the aligned transcript, never the prose.
4. State in the delivery which method verified the stamps: "word-level, edit <title>" or "sentence-level prose (no aligned transcript)". Never write "verified against the transcript" without naming the method.

Keep aligned-transcript data as working data. Report only the selected stamps and a few words of evidence per stamp; never paste transcript rows into the package.

**Audience for everything below:** the Audience line in `channel-profile.md`.

**Global rules:**

- Never fabricate timestamps, stats, or quotes. Everything traces to the transcript.
- When cleverness and search intent conflict, search intent wins.
- Theme beats timeliness. The anchor for titles, description Line 1, and the cold open is the episode's spine: the theme spanning the most runtime, never its newsiest or most searchable segment.
- Verify every timestamp per Step 0b before delivery. A wrong timestamp costs more edit time than no timestamp.
- The user's voice and formatting rules apply to all written output (titles, description, pinned comment, captions).

Deliver the outputs below, in order, in the chat.

## 1. Anchor themes and target queries

Before anything else, name the episode's 1 to 2 anchor themes: threads that span multiple large segments or a third-plus of the runtime. A news drop, a rant, or one sharp quote is a segment, never a theme, no matter how timely or searchable. Two tests, both must pass:

1. Would a regular listener say "that's what this episode was about"?
2. Would a cold viewer who clicked a title promising this theme feel the episode delivers on it for most of the runtime?

State each anchor theme with the segments and timestamps that prove its coverage, so the user can redirect the anchor before any titles get drafted. The bar is coverage, never category: if a news topic genuinely dominates the episode, it qualifies as the anchor.

Then extract the 3 to 5 real search queries this episode can answer, phrased exactly how someone would type them into YouTube or ask an AI assistant. The top 1 to 2 queries must map to the anchor themes. Segment-level queries are fine below that; they feed chapters, clips, and tags. List each with a one-line rationale.

## 2. Titles (10, two lanes)

Every title draws from the anchor themes in Section 1.

**Lane A, search titles (5):** each is a query people actually type ("How to...", "X vs Y", "Why X"). Under 60 characters. Name the target query next to each.

**Lane B, click titles (5):** punchy, hard-hitting, curiosity-driven. Best-in-class hook frameworks from YouTube, TikTok, Reels. At most 2 may be segment-level hooks (a news drop, platform drama, a single quote). Label those "segment title" so the user knows they trade honesty of scope for heat.

Then recommend ONE hybrid title: search phrasing with a click-worthy edge. The recommendation must be theme-anchored, never a segment title, however timely or high-volume its query. A viewer who gets 15 minutes of payoff on a 100-minute promise is a churned viewer. Defend the pick in one sentence, including which anchor theme it carries.

## 3. Description (layered, this exact order)

- **Line 1 (max 150 characters):** a direct, complete answer to the anchor theme's core query, the same theme the recommended title promises. No teasing, no "in this episode..." This is what shows above the fold and what AI engines extract.
- **Hook paragraph:** unique, punchy, self-deprecating, third person, built on the most surprising takeaways.
- **Coverage block (40 to 60 words):** plainly states what is covered using full names of tools and concepts. No pronouns. Each sentence must make sense standalone.
- **Canonical description and standard links** from `channel-profile.md`, verbatim.

Verify the Line 1 character count and coverage block word count programmatically before presenting.

## 4. Chapters

Timestamps 100 percent accurate to the transcript, verified per Step 0b: each chapter starts on the aligned-transcript row where the idea its name promises is first spoken, never on a nearby sentence stamp. Chapter names phrased as the sub-question each segment answers ("What are style references", "How to build a reusable prompt library"). Under 55 characters. No hyperlinks. If the transcript lacks a reliable timecode for a segment, flag it; never guess. Close the section with the verification method line from Step 0b.

## 5. Citable claims (3 to 5)

Standalone quotable claims from the episode: specific, numbers where possible, understandable with zero context. These feed the pinned comment and future written content.

## 6. Pinned comment

2 to 3 sentences: restate the anchor theme's core answer, add one insight not in the description, end with a question to viewers.

## 7. Caption fix list

Every term YouTube auto-captions will likely garble (tool names, model names, jargon, the show name, host and guest names), formatted as find → replace, so the user can correct the caption file in one pass. Start from the Garble-prone terms list in `channel-profile.md`, then pull the actual garble-prone terms from THIS transcript. Never a generic list.

## 8. Cold-open pick

The single strongest 15 to 30 second passage that pays off the recommended title's promise with a clean, self-contained answer. It must belong to an anchor theme: the cold open is the title's first proof, never just the episode's best standalone moment. Quote it with its timestamp (word-level in and out per Step 0b), so it can be moved to the front of the edit. If a segment-level moment is clearly stronger on tape, offer it as a flagged alternate, never as the pick.

## 9. Hashtags and tags

3 to 5 hashtags max. 10 to 12 video tags: exact target queries with theme queries listed first, then tool names and the brand terms from `channel-profile.md`. No filler.

## 10. Video clips

Mine the episode for the 10 strongest short-form clips (30 to 60 seconds assembled runtime) for the show's audience. Clips are segment-level by design; the theme anchor does NOT constrain them.

**A clip qualifies on one of these hooks:**

- A contrarian or counterintuitive claim
- A specific number or before/after result
- A named tool plus a concrete workflow move someone can steal today
- A lived-experience story with a payoff
- A sharp reframe of something the audience already believes

**Reject:** anything that needs more than 3 seconds of missing context to land, anything that is setup without payoff, and anything where the insight is generic enough that any podcast in the category could have said it.

**Multi-segment cuts are encouraged:** pull 2 to 4 non-contiguous pieces per clip when the connective tissue is filler. Every segment boundary must cut on a completed sentence or natural breath so the edit is invisible. Flag any segment where the join might feel jumpy and suggest the bridge fix (jump cut, b-roll moment, or text overlay).

**Deliver as a ranked top 10, best first.** Each entry gets:

- A working title (the hook, phrased like an on-screen caption)
- Total assembled runtime
- The segment table: segment number, start-end timestamp, first 5 to 8 words spoken plus last 5 to 8 words spoken so the edit points are findable without scrubbing. Start and end come from the word-level read in Step 0b (the true first and last word), so the same table can drive a cut in the editing tool later without re-timing.
- Who is speaking
- One line on why it clips (which hook type, and who it stops mid-scroll)
- A suggested opening frame (which segment leads; sometimes the punchline from later is the cold open)

**After the top 10, add a short bench:** 3 to 5 near-misses with one line each on why they did not make the cut, in case the edit reveals a top-10 pick does not work on video.

Verify every timestamp per Step 0b before delivery.

## 11. Upload Category, Type, Problems

YouTube Studio asks for all three on upload. Decide each from the transcript and give one line of reason per field. Category and the anchor theme are the same decision: the theme that spans the runtime picks the category, never the newsiest segment.

**Category (every episode).** One pick from YouTube's fixed list. For a teaching-led show only two are live; the rest never fit.

- **Education** (default): the anchor theme teaches a method, workflow, or mental model a viewer could apply. Most episodes.
- **Science & Technology**: the anchor is a model or tool release, platform news, or a capability comparison, and the teaching layer is thin.
- **People & Blogs**, **Entertainment**, **Howto & Style**: never. The first two are unsorted bins; the third is lifestyle DIY and beauty, and it signals the wrong neighborhood to the recommender.

Mechanism, labeled. Category is a weak signal on YouTube itself (inference; YouTube's own copy says only "so viewers can find it more easily"). Its real leverage: Education is the only category that exposes the Type and Problems fields, and those map to Google's learning-video structured data, which feeds Search's learning features (fact: Google's LearningResource documentation lists the same Type values the dropdown shows). A tie between Education and Science & Technology goes to Education.

**Type (every Education episode).** Options in the dropdown: Concept overview, Problem walkthrough, Real life application, Activity, Experiment, Lecture, How-to, Tips, Other. Pick the one describing the largest block of runtime, mapped from the anchor theme:

- **How-to**: the spine is a step-by-step build or workflow.
- **Concept overview**: the spine is a framework, a reframe, or "how this actually works."
- **Tips**: a grab-bag of moves with no single build.
- **Real life application**: the hosts show their own production use of a tool end to end.
- **Lecture**: single-speaker talk or a recorded webinar only. A two-host conversation is never a Lecture.

None is a fallback for a pure news or interview episode, never a default. Google's documentation says a Type that does not fit means the metadata may not be used at all, so a wrong Type is worth less than no Type.

**Problems (only when it earns it).** The field maps to Google's "problem walkthrough" clip markup: a timestamp plus the question answered at that point, one per line, surfaced as jump-to points in Search. Fill it only when all three hold:

1. The episode answers at least three concrete, self-contained questions someone would actually type.
2. Each answer lives in one bounded segment with a Step 0b verified stamp.
3. Type is How-to, Problem walkthrough, Concept overview, or Tips.

Source the lines from the Section 4 chapter table (already phrased as questions, already verified). 3 to 6 lines, question form, `M:SS` or `H:MM:SS`, one per line, in the format YouTube shows in the placeholder. Otherwise write "Problems: skip" with the reason. Whether Google surfaces these for podcast-length content is unverified; the cost is one paste, so fill it when the rule passes and note in the package if a prior episode's Problems lines ever appeared in Search.

Deliver as three labeled lines (Category, Type, Problems) with the reason for each, paste-ready.

## 12. Promote targeting

For paid spend through YouTube Studio's Promote flow. Every package ships a paste-ready targeting block. Each field optimizes for its own metric: locations and age for subscriber quality per dollar, interests for relevance without dilution. Views alone are never the metric, since Promote will happily buy cheap views that never subscribe and never watch a second episode.

**The standing rule behind every pick.** A subscriber only counts if they look like the audience the show is built for (and the audience a sponsor would pay to reach, if the show carries sponsors). Optimize cost per audience-grade subscriber, never cost per view.

**Inputs, read before recommending.**

1. The Audience baseline block in `.skills-data/channel-profile.md`: top countries by watch time and subscribers gained, age and gender split, refreshed quarterly from YouTube Studio's Audience tab (or an analytics tool that exposes the same reports). If the block is empty, use the defaults below, label them "prior, no channel data," and ask the user once for the Studio Audience rows so the block can be filled.
2. `.skills-data/youtube-log.md`: one row per campaign (date, episode, goal, locations, age, interests as the exact labels used, budget, days, views, subscribers gained, cost per view, cost per subscriber). Read the last five rows. If a tighter interest set beat a wider one on cost per subscriber, the tighter set is the standing set until a row says otherwise. If the file is missing, create it with the header row and the campaign this package proposes, marked pending results.

**Goal.** Subscribers for the full episode. The views goal buys watch time from whoever is cheapest; the subscribers goal optimizes toward people who act, which is the growth the user is paying for. Use the views goal only for a Shorts clip run, and say so.

**Locations (rank by watch time share times audience value).** Default until the baseline exists: United States, United Kingdom, Canada, Australia. From the baseline: keep the countries that together carry about 80 percent of subscriber gains among the markets the show is built for; add any country over 5 percent of watch time that the show wants to reach. Never leave the field empty. Empty means every market, which fills the campaign with the cheapest impressions on earth, inflates the view count, and trains the recommender on an audience that will never watch episode two. Per-episode overrides: a guest or a tool with a strong regional base earns its country a slot for that episode only, named with the reason.

**Age and gender.** Default 25-54, all genders; refine from the baseline and drop any bracket under 5 percent of watch time. Do not narrow gender.

**Interests (2 to 4 total, structured, never a list).** Interests union together: every added interest widens the audience, so each one is a dilution decision, and Promote already expands a narrow selection on its own (fact, from the field's own copy). The failure direction is too broad, never too narrow.

The picker runs on Google's standard affinity and in-market audience taxonomy, and that taxonomy has no artificial intelligence, machine learning, or 3D modeling segment. AI exists in Google Ads as a keyword and a topic, never as an audience. Never name a concept and hope the picker has it. Every interest in the package must be a label listed under Confirmed Promote interest labels in `channel-profile.md`, or a Google affinity or in-market segment name carrying a "verify label" flag.

Build the set in slots:

- **Core (2, every episode)**: the two in-market segments closest to what the audience buys. For a marketing and creative-tools show, that shape is "Marketing & Advertising Services" then "Design Software" (verify label until confirmed). If the picker exposes children under a parent, keep the parent until a log row shows a child beating it on cost per subscriber.
- **Episode (0 to 1)**: an affinity segment for the episode's anchor, such as "Technophiles" for a model release or new-tool demo. When the anchor is a craft topic with a matching in-market segment ("Video Software" for a video-editing episode), name that segment with a "verify label" flag instead. When nothing fits, stop at two.
- **Audience (0 to 1)**: a professional affinity segment such as "Business Professionals" only when the anchor is running a business with the tool rather than making with the tool. Verify label.

Never pick broad Technology, Entertainment, Social Media, Business as a whole, or any interest that describes the platform rather than the viewer. When the user reports a label as present or absent in the picker, update the Confirmed list in `channel-profile.md` in the same session so the next package starts from real names, and record the exact labels in the log row.

**Deliver** as a paste-ready block: Goal, Locations, Age, Gender, Interests by slot with the reason per line, then the one line the log needs once results settle. Never write ad copy, never propose a budget, never start a campaign. The user presses the button.

## Delivery

All 12 sections appear in the chat, verbatim, in order. Also save the full package to `.skills-data/youtube-packages/YYYY-MM-DD_<episode-slug>.md` so it survives the session. Save AND show; a file path is not delivery.

After delivery, offer (never auto-run): banking the citable claims through /mine, and running /fleet on the same transcript for written derivatives.

## Output

The 12 sections above, in order, verbatim in chat: themes and queries, titles, description, chapters, citable claims, pinned comment, caption fixes, cold open, tags, clips with bench, Category/Type/Problems, Promote block with its pending log row. Plus one saved package file.

## Boundaries

- Never fabricates a timestamp, a stat, or a quote. Never writes "verified" without naming the method.
- The recommended title, Line 1, and the cold open are theme-anchored. Segment titles are labeled and never recommended.
- Never writes ad copy, proposes a budget, or starts a campaign.
- Never names a Promote interest without confirmation or a "verify label" flag.
- Not for a standalone description, a quick title brainstorm, or Shorts-only packaging without a full transcript.
