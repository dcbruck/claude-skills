# /ghost

**What it does**

Drafts emails, proposals, newsletters, scripts, and page copy in your voice, then runs every draft through a seven-step audit gate before you see it. The gate hunts the tells that mark writing as machine-made (negate-then-assert, trio lists, summary closers, contraction avoidance, and the rest of your kill list), then checks it did not flatten the voice while doing it. You get the clean draft. No audit log, no preamble.

**Install**

See the root `INSTALL.md`.

**Try it**

```
/ghost email to Acme confirming Monday kickoff and Net 15 terms
/ghost newsletter section on why brand-voice plugins miss the personal-name problem
```

Add `--no-voice` to run with a plain first-person register before you have a voice profile.

**Files it uses**

- `voice-profile.md` at the project root (template in `templates/voice-profile.md`)
- `kill-list.md` at the project root (starter in `templates/kill-list.md`)
- Optional: an email playbook, a metaphor bank, a bio file, a design direction for page copy

**Pairs with**

- `/fleet` for episode-derived LinkedIn posts and companions
- `/mine` for pulling seeds out of transcripts before drafting
- `/beastmode` when the ask needs sharpening before it reaches /ghost
