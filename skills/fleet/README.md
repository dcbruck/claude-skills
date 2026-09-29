# /fleet

**What it does**

Turns one podcast episode or long-form recording into a full content set: LinkedIn posts, short-platform companions, ranked clips with verified timestamps, a subscriber newsletter section, a show-page newsletter, and optional long-form editions. Every piece is drafted in your voice from real transcript material, audited against your kill list on its own, then scanned against the rest of the batch so ten posts read as ten ideas instead of one idea in ten outfits. Personal-channel pieces never name co-hosts or guests. Stops and asks if the source looks like a private or client call.

**Install**

See the root `INSTALL.md`.

**Try it**

```
/fleet ep 12
/fleet transcripts/q3-panel.txt 6 posts, no clips
```

**Files it uses**

- `voice-profile.md` at the project root (template in `templates/voice-profile.md`)
- `kill-list.md` at the project root (starter in `templates/kill-list.md`)
- `.skills-data/transcripts/` for saved raw transcripts (optional)
- A connected recording or transcript tool, if you have one (optional)

**Pairs with**

- `/mine` to pull seeds from a transcript without drafting the full set
- `/youtube` for the episode's video-side packaging
- `/ghost` for one-off pieces outside the episode cycle
