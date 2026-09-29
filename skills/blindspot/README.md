# /blindspot

**What it does**

Generates the high-ceiling ideas you have not thought to ask for, against your actual setup rather than generic best practice. It inventories what you already own first (installed skills, scheduled tasks, project files, decisions log), generates three times what you asked for in private, kills everything that is generic, low-ceiling, or already yours, scores the survivors on a stated rubric, and presents only what clears the floor. If four ideas clear, you get four, and it says why the rest died.

**Install**

See the root `INSTALL.md`.

**Try it**

```
/blindspot
/blindspot my content pipeline
```

Type `/blindspot` alone to sweep the whole system. Ask for "10 more" and it excludes everything already shown.

**Files it uses**

- Reads: installed skills, scheduled tasks, whatever project files you keep
- Optional: `decisions.md` (standing constraints), `.skills-data/triage-backlog.md` (what was already held or killed)
- Writes: none

**Pairs with**

- `/triage` captures verdicts on the survivors
- `/domainjack` for ideas borrowed from other domains rather than found in your own seams
- `/beastmode` routes "what am I missing" prompts here
