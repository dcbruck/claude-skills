---
name: adopt
description: Manual external-content evaluator. ONLY triggers when the user explicitly types /adopt followed by a source (pasted post, article text, URL, or file path). Do NOT auto-fire on "what do you think of this," "summarize this," or any paste without the command. Parses outside content for claims, tactics, and mindsets, verifies at a depth matched to source trust, reads each item for general AND user-specific impact, audits against the user's actual setup so nothing contradicts, duplicates, or breaks what they own, then returns ranked ADOPT/ADAPT/SKIP verdicts with model-does/user-does specs. Before any SKIP stands, a repoint pass strips the item to its core mechanism and hunts the user's other surfaces for a better target. Names the salient takeaway, flags what the user does today that should change, offers to build on the spot. Verdicts bank to .skills-data/adopt-ledger.md. NOT for turning a source into content (/mine, /fleet), idea generation (/blindspot), or capturing verdicts (/triage).
license: MIT
metadata:
  version: 1.0.0
  author: Drew Brucker
  source: https://github.com/dcbruck/claude-skills
---

# /adopt: outside advice, audited against what the user owns

/adopt turns the daily flood of AI advice into system upgrades for the user, without the user supplying the context or the ideation. They spot the post. The skill does the reading, the vetting, the audit against what they already own, and the build plan. Most outside advice is recycled, some contradicts rules the user has already paid to learn, a few pieces are gold. The one failure this skill exists to prevent: judging outside advice against a generic mental model of a system instead of the user's real one.

## Setup

One file, under `.skills-data/` at the project root by default.

| File | What it is |
|---|---|
| `.skills-data/adopt-ledger.md` | Every verdict ever issued, additive-only. Missing on first run: create it with a one-line header and the format block from Step 6. |

Ecosystem audit reads whatever the user keeps: CLAUDE.md or equivalent, installed skills, a decisions log, a voice profile, project files. Nothing is required. A thin ecosystem means fewer overlap and conflict findings, so say so in one line when the inventory is thin.

Optional integrations: web tools to fetch URLs, a transcription tool for video sources. If the source is a video URL and no transcription tool is available, ask the user to transcribe it and feed the output here.

Your project's writing and formatting rules apply if you have them (CLAUDE.md or equivalent). Assume them.

## Trigger

The user types `/adopt` followed by a source: pasted text, a URL, or a file path. Fetch URLs with web tools. Read file paths directly.

```
/adopt https://example.com/posts/how-i-run-my-agents
/adopt [pasted 600-word post about prompt caching]
/adopt notes/vendor-playbook.md
```

Does not fire on "what do you think of this," "summarize this," or any paste without the slash command.

## Step 0: Ledger check, silently

Read `.skills-data/adopt-ledger.md`. If any extracted idea (Step 1) matches a past evaluation in substance, not just wording, carry the prior verdict into the output: `[evaluated YYYY-MM-DD: VERDICT, reason]`. A repeat idea gets re-opened only if the source adds something the original evaluation did not have. Say what that something is. Recycled advice returning every six weeks is the exact failure this ledger prevents.

## Step 1: Read fully, then extract

Read the source in its entirety before extracting anything. No skimming, no judging from the hook.

Pull the discrete items out. An item is anything that could genuinely change how the user operates or thinks: a claim, tactic, workflow, prompt pattern, system design, framing, or mental model. Tangible or intangible, leverage counts either way. Motivation, throat-clearing, and engagement bait are not items. A 600-word post usually holds 2-4 real items. Zero is a legitimate count.

Tag each item on extraction:

- **Claim**: asserts something checkable ("X model does Y," "this converts 3x better").
- **Tactic**: a way of doing something, testable only by doing it.
- **Mindset**: a framing, mental model, or operating principle. Internalized rather than built. Still an item; a reframe that changes how the user prices or positions can outleverage any workflow.
- **Taste**: opinion or style preference, not verifiable, still sometimes worth adopting.

## Step 2: Tiered ecosystem scan

**Layer 1, every run.** The user's CLAUDE.md or equivalent in full, the installed-skill roster with descriptions, and the scheduled tasks and automations the user runs. This is the map.

**Layer 2, opened only when an item touches its territory.** Read the actual files, never the memory of them:

| Item territory | Open these |
|---|---|
| Content, writing, hooks, posting | The voice profile and kill list, if the user keeps them; any writing rules in CLAUDE.md |
| Pricing, sales, positioning, offers | Positioning notes, pipeline or project files, if kept |
| Memory, workflow, session habits | The decisions log, if kept |
| Automation, agents, scheduled work | The live task roster, `.skills-data/triage-backlog.md` if present |
| Skills and prompting patterns | The SKILL.md files of any skill the item overlaps |
| Brand, design, visual output | Brand or design files, if kept |

An item spanning two territories opens both. An item touching none gets Layer 1 only. The point of the tier: a 200-word post about hooks deserves a deep read of the writing rules and zero reads of the pipeline.

**What the scan produces per item:** overlap (the user already has this, name where), conflict (this contradicts a rule, decision, or lesson, cite it), or clear (nothing touches it). A conflict with the decisions log or the kill list is decisive unless the user explicitly overrides. Their paid-for lessons outrank a stranger's post. The scan is also the break-nothing gate: an item that would touch a running automation, a scheduled task, or a file another system reads gets its blast radius named before it can reach ADOPT.

**The scan runs both directions.** While checking the source against the user's system, watch for the reverse finding: something the user currently does that the source, once verified, shows should change or stop. Bank these for the "On your current setup" section (Step 5). The audit judges the source against the system AND the system against the source.

## Step 3: Verify, at a depth the source earns

Tier the source first, then spend verification where the trust is thinnest:

- **Cited**: references a named paper, official docs, a changelog, a dataset. Spot-check that the citation exists and says what the post claims it says. One check per citation, no deeper. A real source misquoted is the sneakiest failure here.
- **Firsthand**: a practitioner reporting their own results, with receipts. Verify only the load-bearing claims: the ones where the verdict flips if they are false (a model capability, a feature that may not exist, a stat doing heavy lifting).
- **Uncited social**: big claims, no receipts, hyperbolic register. Every load-bearing claim gets checked or labeled unverified, and unverified lowers the bucket. Name hyperbole as hyperbole. Never launder "this changed everything" into a finding.

Two searches per claim maximum. If it is still murky, say "unverified" and move on rather than burning the session on forensics. Mindset and Taste items skip verification entirely. Label every load-bearing input Fact (sourced), Inference, or Assumption; show the label only where the verdict depends on it.

## Step 4: Bucket

- **ADOPT**: verified, clear of conflicts, adds something the user does not have. Comes with an implementation spec.
- **ADAPT**: the core survives but the as-written version overlaps or conflicts. Spec states what changes and why the user's version beats the source's.
- **SKIP**: with the reason in one of four words: *owned* (already has it, name it), *conflicts* (cite the rule or decision), *unverified* (the load-bearing claim did not check out), *low-value* (true but not worth the user's hours).

**The repoint pass. Run it on every item headed for SKIP, before the verdict stands.**

A SKIP verdict judges the item as the source aims it. The source's aim is often the only thing wrong with the item.

1. Strip the item to its core mechanism: the part that does the work, separated from the target the source points it at.
2. Check the core mechanism against the user's other surfaces: chat register, content the user signs, agent-facing prose (SKILL.md files, task prompts, automation blocks), client deliverables, sales motion, brand assets, memory or notes layer.
3. If the core mechanism lands clean on a different surface, escalate the item to ADAPT. The spec names the new target and states why the source's target was wrong.
4. If no surface fits, the SKIP stands.

The failure this pass prevents, by example: a source says "write everything in simplified technical English." As aimed, that conflicts with the user's chat register and heads for SKIP. The mechanism, a controlled vocabulary and one idea per sentence, lands clean on agent-facing prose like SKILL.md files and task prompts. The pass exists so the first report finds that target, not the user's follow-up question.

**The spec, four lines max:** what changes; which file or skill it lands in; the split, meaning what the model builds solo without losing accuracy or context versus what the user must do or provide (access, judgment calls, approvals, outside dependencies, ideally none); and effort for each side (minutes / an hour / a build session). If the change would touch a file containing the user's own words, the spec says "additive-only" explicitly. The ideal spec reads: "Model: 20 min, solo. User: tap yes."

**Mindset ADOPTs get a landing spot, not a build spec.** An idea worth internalizing needs one place it gets written so it survives the session: a principle in CLAUDE.md, a decisions-log entry, a doctrine file, a line in positioning notes. "Internalize it" with no landing spot is how good ideas evaporate by Friday. Name the spot and the one-line form it would take there.

## Step 5: Present

Open with one line on the source: what it is, who wrote it, trust tier. Then the buckets, one item per block, **ranked by user-specific impact, highest first**. The user should be able to stop reading after the top two items and have gotten the run's value.

**[Item name]**: VERDICT
*Impact:* one line, two reads: how much this matters in general, then how much it matters for this user given their system, projects, and pipeline.
*Why:* one line, citing the ecosystem file or verification result that decided it.
*Spec (ADOPT/ADAPT only):* the four-line split spec, or the landing spot for mindset items.

**On your current setup.** When the two-way scan (Step 2) found something the user currently does that this source shows should change or stop, give it its own short section after the buckets. One line per finding, citing the file or practice, verdict verbs: change, retire, or keep-but-watch. Removal is a legitimate recommendation and this is the only section allowed to make it. Empty most runs; say nothing when it is empty.

**The blind-spot hatch.** When an item's general impact is high but its relevance to the user cannot be judged from the files (they may be sitting on plans nothing on disk records), say exactly that and ask one targeted question: "High general value. Relevant to you only if [X] is in play. Is it?" Never silently downgrade an item because the user's side of the picture is invisible. Cap: two such questions per run, asked at the close, never mid-report.

Close with three things: the counts (extracted / adopted / adapted / skipped, counted programmatically), **the single most salient takeaway in one line**, the thing worth internalizing even if nothing gets built today, and the question: "Build the adopted items now?" with the buildable items numbered so the user can pick a subset.

## Step 6: Execute on yes, bank always

**On an explicit yes in the current message**, build the picked items. Additive-only on any file holding the user's words or data. Destructive changes get listed and confirmed first. New skills get written as a SKILL.md in the user's skills folder. Mindset items write to their named landing spot. Show the diff or the new content in chat, verbatim, when done.

**Bank every verdict regardless**, including SKIPs and "on your current setup" findings. Append to `.skills-data/adopt-ledger.md`, additive only:

```
- **[A-YYMMDD-NN]** [item, one line] | **VERDICT** (*owned/conflicts/unverified/low-value* for skips) | [deciding reason] | *source: [title/author/URL, trust tier]* | *[date]* | built: [yes/no/date]
```

When an ADOPT gets built later, append a new line referencing the ID rather than editing the original. If the ledger does not exist, create it with a one-line header and this format block.

## Output

In order, every run:

1. One line on the source: what, who, trust tier.
2. The buckets, ranked by user-specific impact, one block per item (name, verdict, impact, why, spec).
3. "On your current setup," only when non-empty.
4. Up to two blind-spot questions.
5. The counts, the salient takeaway, and "Build the adopted items now?" with items numbered.

Silent, every run: the ledger check and the ledger append.

## Boundaries

- **Never execute without the yes.** The verdict and specs are free. Changing the user's system is not. "Build it" in a previous session is not confirmation now.
- **Conflicts beat novelty.** When outside advice contradicts a logged decision or lesson, the default verdict is SKIP-conflicts, presented with the citation. The user can override. The skill never overrides for them.
- **Break nothing, leak nothing.** Any item touching a running automation, scheduled task, or file another system reads gets its blast radius named in the spec. Anything client-facing or containing deal data never leaves the project as a side effect of a build.
- **Name the overlap precisely.** "You sort of have this" is useless. "This is /mine Step 9 minus the synthesis" lets the user judge the delta in one glance. Partial overlaps go to ADAPT only when the new part can carry the item alone.
- **Zero items is a valid output.** If the source is all engagement bait, say so in two lines and bank nothing except a one-line ledger note on the source. Do not manufacture buckets to justify the run.
- **Count programmatically.** Extracted, verified, bucketed, banked. Real numbers, checked before the close.
- **Cap the run.** Extraction plus scan plus verification should fit one pass. If a source is a 40-minute read spawning 15 items, present the top items by potential impact and say what was left unevaluated.
- Not for remixing a source into content, banking a transcript (/mine, /fleet), generating ideas from the user's own system (/blindspot), or capturing verdicts on a list (/triage).
