# /youtube

**What it does**

Turns a finished episode transcript into the complete YouTube upload package: anchor themes and target queries, ten titles in two lanes plus one recommended hybrid, a layered description, chapters, citable claims, a pinned comment, a caption fix list, a cold-open pick, tags, ten ranked short-form clips with segment tables, the Category/Type/Problems decision, and a paste-ready Promote targeting block. Every title and the cold open anchor to the theme that spans the episode, never its newsiest segment. Timestamps verify at word level when your recording tool exposes an aligned transcript, and get flagged as sentence-level when it does not.

**Install**

See the root `INSTALL.md`.

**Try it**

```
/youtube ep 12
/youtube transcripts/ep12-agent-workflows.txt
```

**Files it uses**

- `.skills-data/channel-profile.md` for show name, hosts, audience, canonical description, links, audience baseline, and confirmed Promote labels (template in the skill's Setup)
- `.skills-data/youtube-log.md` for one row per Promote campaign
- `.skills-data/youtube-packages/` for saved packages
- `.skills-data/transcripts/` for raw transcripts, shared with /mine and /fleet (optional)
- A connected recording or transcript tool, if you have one (optional)

**Pairs with**

- `/fleet` for the written content set from the same transcript
- `/mine` to bank the episode's claims in your idea library
