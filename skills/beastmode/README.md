# /beastmode

**What it does**

Rewrites the prompt you typed into the prompt you should have typed, shows you the rewrite as a six-section block (Goal, Context, Constraints, Output, Avoid, Assumed), then executes it or routes it to the skill that owns the job. A fidelity gate checks the rewrite against what you actually asked, so nothing you said gets dropped and nothing you did not ask for gets added. Every run is logged, and moves that keep recurring get proposed as standing defaults.

**Install**

See the root `INSTALL.md`.

**Try it**

```
/beastmode write the follow-up email to Acme after yesterday's kickoff, they want the timeline by Friday
/beastmode --review what should the pricing page say for the new tier
```

Add `--deep` to fan out across independent angles before synthesizing. Say "fast" to cancel an automatic `--deep`.

**Files it uses**

- `.skills-data/beastmode-log.md` (created on first run; holds Standing moves plus one entry per run)
- Optional: any connected source tool for transcripts, threads, docs, or calendar entries

**Pairs with**

- `/ghost` for content it routes out
- `/blindspot` and `/triage` for idea generation and verdicts
- `/mine`, `/fleet`, `/youtube` for source material and episodes
- `/adopt`, `/domainjack`, `/redline`, `/graph` for the other routed classes
