# /mine

**What it does**

Turns any transcript (a podcast, a talk, a prospect call, your own episode, an AI chat session) into a permanent deposit in an idea library: claims with timestamps, verbatim quotes, frameworks, stories and numbers. Each new deposit gets collided against everything already banked and against your positioning, so the library produces takes instead of notes. Ask it questions later and every answer cites a deposit and a timestamp. Every five deposits it writes a synthesis: what you apparently believe, where you are heading, and which themes you consume but never publish.

**Install**

See the root `INSTALL.md`.

**Try it**

```
/mine transcripts/acme-founder-interview.txt
/mine ask what does the library say about pricing creative work by outcome
```

Pin lines you want to keep with `/mine pin "..."`.

**Files it uses**

- `.skills-data/transcripts/` for deposits, with `index.md` (positioning, theme vocabulary, deposit rows, anchors, synthesis) and `mine-log.md`
- `voice-profile.md` and `kill-list.md` at the project root, optional, for pinned rewrites and the voice pass
- `.skills-data/content-seeds.md`, optional, for approved seeds
- A connected recording or transcript tool, if you have one (optional)

**Pairs with**

- `/fleet` to draft a full content set from a transcript once it is banked
- `/youtube` for the episode's upload package from the same transcript
- `/ghost` to draft one piece from a seed the report surfaced
