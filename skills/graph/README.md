# /graph

**What it does**

Reads the file that governs a skill or system and draws the real flow: trigger, phases, every branch and gate, inputs and outputs, handoffs to other skills. Ships it as one self-contained HTML file (inline SVG, or Mermaid for large graphs) in a neutral dark theme you can swap for your own tokens. It refuses to draw from memory or from a description field, and it draws the ugly version when the file is ugly, because a tidy diagram of a messy skill is a lie.

**Install**

See the root `INSTALL.md`.

**Try it**

```
/graph beastmode
/graph docs/runbooks/deploy.md --light
```

**Files it uses**

- Reads: the `SKILL.md`, runbook, config, or path you name
- Writes: `graph-<subject>.html` in the project root (and an artifact when the environment supports one)

**Pairs with**

- `/beastmode` routes "show me how X works" here
- Any repo skill as a subject: `/graph fleet`, `/graph redline`, `/graph mine`
