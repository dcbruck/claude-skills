# /redline

**What it does**

Reviews a contract you are about to sign (MSA, SOW, NDA, licensing or vendor agreement) clause by clause against the positions you already hold, then reads it again as the counterparty's lawyer to find what a friendly read misses. Every material issue gets a severity (MUST-FIX / PUSH / WATCH), the current language, the proposed change, and how hard to push. Ends with a counsel-gate every time. Strategic and editorial analysis only; a lawyer reviews anything signed.

**Install**

See the root `INSTALL.md`.

**Try it**

```
/redline contracts/acme-msa.pdf
/redline [pasted vendor SOW] --swarm
```

Add `--outbound` to check your own draft for what you are giving away, and `--doc` for a tracked-changes .docx of the redlines.

**Files it uses**

- `.skills-data/standard-clauses.md`, optional: the clauses you insist on (IP carve-out, voice and likeness, liability line, insurance, non-solicit thresholds, known anti-patterns). Example layout in the skill's Setup.
- `.skills-data/redlines/` for `--doc` output

**Pairs with**

- `/ghost` to draft the cover email that sends the redlines back
- `/beastmode` when the ask needs sharpening before the review runs
