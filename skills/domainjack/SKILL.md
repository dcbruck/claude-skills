---
name: domainjack
description: Manual cross-domain idea engine (Domain Jacking). ONLY triggers when the user explicitly types /domainjack followed by a target they name (a problem, opportunity, goal, outcome, role, or task), a donor domain plus target, or a practice they already spotted. Do NOT auto-fire on 'any ideas,' 'cross-industry,' 'what could we borrow,' or general ideation. Finds proven mechanisms in non-obvious domains and transfers them where they are novel and valuable, across three modes (Target-First, Bridge, Seed-First), ranked by a multiplicative spread score with a fake-arbitrage guard. NOT for high-ceiling idea generation against the user's own system (/blindspot), structured decision ideation, or capturing verdicts (/triage).
license: MIT
metadata:
  version: 1.0.0
  author: Drew Brucker
  source: https://github.com/dcbruck/claude-skills
---

# /domainjack: cross-domain mechanism transfer

/domainjack finds proven or promising ideas in non-obvious industries, professions, sciences, subcultures, technologies, or historical systems and adapts them to the target the user names. The goal is not random creativity. The goal is to find things already mature, effective, or well-understood somewhere else that are underused, overlooked, or absent here. Find elsewhere, understand the mechanism, adapt it here. The one failure it exists to prevent: fake arbitrage, an idea presented as novel in the target domain when the target already does it.

## Setup

No files. Web tools are optional: when connected, the skill verifies niche sources and checks target-domain adoption. Without them, it labels those ideas as unverified rather than inventing precedent.

Your project's writing and formatting rules apply if you have them (CLAUDE.md or equivalent). Assume them.

## Trigger

The user types `/domainjack` followed by one of three inputs.

```
/domainjack reduce no-shows for discovery calls with new prospects
/domainjack what could a consulting onboarding process borrow from air traffic control
/domainjack pre-mortems, the way surgical teams run them: where else would this land
```

Does not fire on "any ideas," "cross-industry," "what could we borrow," or general ideation without the slash command.

## Mode (detect from the input)

- **TARGET given**, a problem, opportunity, goal, outcome, result, role, task, or capability the user names, with no source domain in mind: **Target-First.** Abstract it to the underlying function or job to be done, then hunt donor domains that already perform that function well and transfer their mechanisms back. The user does not need a source in mind. Finding the source is your job.
- **DONOR DOMAIN plus target given: Bridge.** Inspect the donor domain for mechanisms, tools, practices, systems, workflows, heuristics, and operating patterns that could transfer. Do not favor the most famous or obvious examples. Prioritize the ones with the strongest structural fit, hidden usefulness, and transfer potential into the target. The user is not supplying the source facts. You are. Tag each with proof level so they know what is real versus extrapolated.
- **SEED given**, a specific practice already spotted: **Seed-First.** Find the markets or audiences where that mechanism is novel, needed, and deployable without the source's infrastructure.

## Core method

1. Abstract the target beyond its obvious category, down to the underlying function or job to be done. Ask "who else has to produce this outcome, perform this function, or play this role," never "what industries look similar." A problem, a goal, an outcome, a role, and a task all reduce to a function someone elsewhere already performs, often under harder conditions. (Bridge mode: instead, scan the donor domain broadly for real mechanisms, tools, practices, systems, and operating patterns, including specialized or obscure ones, then abstract the strongest candidates to see where they land in the target.)
2. Identify structurally similar problems or mechanisms in distant and adjacent domains.
3. Extract the mechanism that makes it work. Not the surface, the cause.
4. Translate that mechanism into the target context, concretely.
5. Prioritize ideas novel here but credible elsewhere.
6. Make each idea concrete enough to test.
7. Rank aggressively. Kill weak ideas. Do not pad.

## Mechanism first

For every source, name what is actually making it work. Never transfer surface aesthetics or buzzwords.

- Bad: "use gamification." Better: "use visible progression, variable rewards, and completion tension to drive repeat engagement."
- Bad: "learn from luxury." Better: "reduce choice, increase ritual, control access, and make the buying process itself signal status."

The transferable mechanism matters more than the source example.

## Look for asymmetry

Prioritize ideas obvious in Domain A but invisible in Domain B. Especially: mature tools that never crossed industries, specialized workflows outsiders never see, expensive practices now cheap enough to democratize, old ideas newly enabled by AI, consumer behaviors that could move to B2B and back, digital mechanics that could move physical and back, and proven mechanisms never yet combined here.

Use extreme analogues when useful: who cannot afford to fail at this, who solves it under extreme time pressure, at massive scale, with almost no resources, before modern technology existed, how nature solves a structurally similar problem, who faces the same problem with opposite incentives, and where it is unusually expensive, dangerous, regulated, or competitive. Extreme environments hold unusually strong mechanisms.

## Banned: the usual suspects

Any source already famous AS a cross-domain lesson, whether a household brand (Apple, Disney, Netflix, Amazon) or an overused chestnut (F1 pit crews, casino reward loops). Ban the tired EXAMPLE, not the industry. The industry's unmined corners stay in play. Overused examples may be cited as precedent, never proposed as a transfer.

## Reframe when needed

If the stated target is too narrow, mis-framed, or aimed at a symptom instead of the real outcome, reframe it briefly before generating. Do not derail the task.

## Research behavior

This is usually ideation, so do not slow it with needless research. Verify when the source is niche or unfamiliar, when a factual claim materially changes the idea, when the transfer depends on a specific practice actually existing, when recency matters, or when an idea is strong enough that proof raises confidence. Prefer primary or expert sources. Never invent precedent.

Tag every idea:

- **Proven**: established elsewhere.
- **Strong analogue**: mechanism proven, application here is new.
- **Speculative**: plausible but meaningfully untested.

## Scoring (ranking engine)

Rank by Spread = Maturity elsewhere (how proven, 1-5) x Novelty here (how unheard-of, 1-5) x Transfer feasibility (how cleanly it moves without the source's infrastructure, 1-5). Multiply, rank highest first. A weak score on any one axis should sink the idea. That is deliberate.

Novelty here must reflect evidence or informed confidence, never assumption. If target-domain adoption is uncertain, cap Novelty at 3 unless verified. This is the main guard against fake arbitrage. If a capped-novelty idea would still rank top-tier, flag it for a quick verify rather than burying it, so a real find is not lost to caution.

Tiebreakers only when spreads are close: speed to test, reversibility, compounding potential, cost, adoption friction. Never let these override a higher spread.

## Output

Underlying function: the 2 to 4 most useful abstractions of the target (the job to be done). Brief. (Bridge mode: open instead with the donor domain's mechanisms you surfaced.)

Then up to 5 ideas, strongest spread first. Fewer if fewer clear the bar. For each:

- **[Idea name]**
- Source: where it comes from.
- Mechanism: the transferable principle.
- Transfer: exactly how it applies to the target.
- Why it matters: the "so what," 2 sentences max.
- Proof level: Proven / Strong analogue / Speculative.
- Spread: the three scores and the product.
- First test: the smallest realistic experiment.

Best bet: the single highest-spread transfer and why.
Wild card: if one idea is meaningfully more unconventional than the rest, flag it. Do not invent a separate wild card.
Combination play: if useful, fuse 2 to 3 of the strongest mechanisms into one higher-order idea.

## Quality bar

A strong result makes the user think "I never would have looked there, but that makes complete sense," followed by "and I could actually test this."

Avoid: shallow analogies, generic brainstorming, obvious adjacent competitors, novelty without utility, long lists of weak ideas, impossible implementations, buzzwords without mechanisms, copying surface features instead of causal principles.

Prioritize: proven elsewhere plus non-obvious here plus transferable mechanism plus realistic implementation plus asymmetric upside.

## Boundaries

- Manual invocation only. Never auto-fire on cross-industry or borrowing language without the slash command.
- This skill owns cross-domain transfer and analogical ideation. When /beastmode receives a prompt about borrowing, stealing, or adapting ideas, tools, mechanisms, systems, or workflows from another industry, domain, discipline, subculture, or era into a target, it routes here.
- Never invent precedent. An unverifiable source gets tagged Speculative or dropped.
- Never present a banned example as a transfer.
- Not for high-ceiling idea generation against the user's own system (/blindspot), structured decision ideation, or capturing verdicts (/triage). Survivors the user wants to keep go to /triage.
