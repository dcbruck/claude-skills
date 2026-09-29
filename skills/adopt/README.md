# /adopt

**What it does**

Evaluates a piece of outside content (a post, article, URL, or file) against what you actually own. It extracts the real claims, tactics, and mindsets, verifies them at a depth matched to how much the source can be trusted, then audits each one against your installed skills, rules, and decisions so nothing you adopt contradicts, duplicates, or breaks something already in place. You get ranked ADOPT / ADAPT / SKIP verdicts, each with a four-line build spec splitting what the model does from what you do, and an offer to build on the spot. Before any SKIP stands, a repoint pass checks whether the mechanism fits a different surface than the one the source aimed it at.

**Install**

See the root `INSTALL.md`.

**Try it**

```
/adopt https://example.com/posts/how-i-run-my-agents
/adopt [paste a 600-word post about prompt caching]
```

**Files it uses**

- `.skills-data/adopt-ledger.md` (created on first run; every verdict, additive-only)
- Reads whatever you keep: CLAUDE.md or equivalent, installed skills, a decisions log, a voice profile, project files
- Optional: web tools for URLs, a transcription tool for video sources

**Pairs with**

- `/triage` for walking a list of adopted items
- `/blindspot` for ideas generated from your own system rather than from outside content
- `/mine` and `/fleet` for source material headed to content instead of evaluation
