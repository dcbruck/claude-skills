# /triage

**What it does**

Walks a numbered list of ideas or options, captures your verdict on each one (SHORTLIST, SCOPE, HOLD, or KILL) with the reason, and writes every verdict to a backlog file that survives the session. Before you see the list it marks anything you already own and resurfaces past holds whose date has come up. Holds carry a resurface date, kills carry their objection, and re-triaged items get a new line instead of an overwrite.

**Install**

See the root `INSTALL.md`.

**Try it**

```
/triage
1. Weekly competitor sweep as a scheduled task
2. Auto-draft replies to inbound leads
3. Rebuild the pricing page

/triage on the ideas above
```

Type `/triage` alone to walk the last numbered list in the session.

**Files it uses**

- `.skills-data/triage-backlog.md` (created on first run; one line per verdict, additive-only)
- Optional reads: installed skills, scheduled tasks, project files, for the dedupe pass

**Pairs with**

- `/blindspot` generates the lists this skill walks
- `/beastmode` routes "which of these" prompts here
- `/adopt` and `/domainjack` produce candidates worth triaging
