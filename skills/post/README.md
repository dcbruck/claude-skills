# /post

**What it does**

Drafts five versions of a LinkedIn post in five different shapes, each one written blind to the others and audited against your kill list until it's clean. Twins and failures get cut. The opening lines get written last, on top of the bodies that survived. You pick from up to three finished posts.

**Install**

See the root `INSTALL.md`.

**Try it**

```
/post why my best-performing post took 11 minutes to write
/post the client who asked for "more AI" and meant "fewer meetings" --one
```

Add `--no-voice` to run before you have a voice profile. Add `--hooks` for opening lines only.

**Files it uses**

- `voice-profile.md` at the project root (template in `templates/voice-profile.md`)
- `kill-list.md` at the project root (starter in `templates/kill-list.md`)
- Optional: `.skills-data/post-log.md`, a running log of what you shipped and how it did. The skill reads it to favor shapes that earn and rotate out shapes you've overused.

**Pairs with**

- `/fleet` when the idea is a whole episode or talk, not one post
- `/ghost` for anything that isn't a LinkedIn post
- `/beastmode` when the idea needs sharpening first
