---
name: graph
description: "Manual skill-and-system visualizer. ONLY triggers when the user explicitly types /graph followed by a skill name, system name, or file path (e.g. \"/graph beastmode\", \"/graph the ingest pipeline\"). Do NOT auto-fire on \"make a diagram,\" \"visualize this,\" or \"show me how this works.\" /graph reads the actual SKILL.md or system doc in full, extracts the real flow including branches and handoffs, and ships it as a self-contained HTML diagram (or an artifact if the environment supports one) in one pass. Accuracy over symmetry: the diagram shows what the file says, never an idealized version. Flag --light for a light background."
license: MIT
metadata:
  version: 1.0.0
  author: Drew Brucker
  source: https://github.com/dcbruck/claude-skills
---

# /graph: skill and system visualizer

/graph reads the file that governs a skill or system, pulls out the real flow (trigger, phases, branches, inputs, outputs, handoffs), and renders it as a finished diagram in one pass. The one failure it exists to prevent: a clean five-step pipeline drawn for a skill that actually branches three ways. It looks authoritative and it is wrong.

## Setup

No data files. The skill reads the file you point it at and writes one HTML file per run: `graph-<subject>.html` in the project root, subject in kebab-case (`graph-beastmode.html`). If the environment can publish an artifact, publish the same HTML there too.

**Theme.** Every diagram uses this token block. Dark is the default; `--light` flips it.

```css
:root {
  color-scheme: light;
  --bg: #0B0B0C;
  --text: #F2F2F2;
  --muted: #8A8A8E;
  --accent: #5B8CFF;
  --font: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}
:root.light {
  --bg: #F7F7F8;
  --text: #111113;
  --muted: #6B6B70;
  --accent: #2F63E0;
}
```

Swap this block for your brand tokens. Nothing else in the skill names a color or font by value.

Your project's writing and formatting rules apply to any text in the output if you have them (CLAUDE.md or equivalent). Assume them.

## Trigger

The user types `/graph` followed by a subject: a skill name, a system name, or a file path.

```
/graph beastmode
/graph the ingest pipeline
/graph docs/runbooks/deploy.md --light
```

Does not fire on "make a diagram," "visualize this," "show me how this works," or any request without the slash command.

## Step 1: Read the source in full

Read the governing file before drawing anything.

- A skill name resolves to its `SKILL.md`. Read the whole file, not the description.
- A system name resolves to whatever governs it: a README, a runbook, a config, a scheduled task prompt plus its log. More than one candidate: ask which.
- A path is read directly.

Never draw from memory or from the description field. The description is marketing; the body is the behavior. If the file cannot be found, say so and stop. Do not draw a plausible version.

## Step 2: Extract the real flow

Pull these out of the source, in this order:

**Trigger.** What fires it, and explicitly what does not. A "do NOT auto-fire on" clause belongs on the diagram.

**Phases.** The numbered stages in the body. Use the file's own names for them, not tidied-up synonyms.

**Branches.** Every conditional. Modes, flags, "if X then Y" forks, stop conditions, approval gates. These are where a diagram adds the most value and what gets smoothed away most often.

**Inputs and outputs.** Files read, files written, where results land.

**Handoffs.** Other skills it routes to or receives from.

Accuracy rules. Never add a box for visual balance. Never merge two distinct steps because the layout is tight. Never drop a branch because it complicates the shape. When the real flow is ugly, draw the ugly flow; if the ugliness is a finding, say so in one line under the diagram.

## Step 3: Apply the theme

Use the token block from Setup. Never hex-pick a color outside it. Never improvise a second font. Text is `--text`, secondary labels and connectors `--muted`, the trigger node and the final output node `--accent`. Under `--light`, add the `light` class to the root element.

## Step 4: Render

Hand-authored inline SVG is the default: full control over color, type, and layout, no dependencies.

Mermaid is the fallback for graphs too large or too interconnected to hand-place cleanly. Load it from a public CDN in one script tag and initialize it with the theme tokens. Theme fidelity is weaker with Mermaid; name that tradeoff in one line when you use it.

Layout. Left to right for pipelines, top to bottom for phase stacks. Branches split visibly, never through label text. The trigger and the final output are the two most legible elements on the canvas. Legend only when the shapes carry meaning.

## Step 5: Ship it

Write the complete self-contained HTML: styles inline, SVG inline, no external assets except the Mermaid script when used. Read it back to confirm it is whole. Publish it as an artifact if the environment supports one. Do not stop at the HTML and wait to be asked. The file is the deliverable, every time, unless the user says otherwise.

Keep `color-scheme: light` on the root even on a dark canvas, and set `--bg` explicitly on the container rather than relying on the page.

## Step 6: Close

Three lines under the diagram, no more.

```
Source: [path read]
Branches shown: N
Anything surprising: [one line, or omit]
```

The third line appears only when the file surfaced something worth knowing: a dead branch, a step with no exit, a handoff to something that does not exist, a stated cadence that contradicts the configured one. Those findings are half the value of drawing the thing.

## Output

One self-contained HTML file at `graph-<subject>.html` (plus an artifact when available), then the three-line close. Nothing else.

## Boundaries

**One subject per run.** A graph of the whole ecosystem is a different request. Say so and offer the top-level map with skills as single nodes.

**Never invent a step.** If the source is ambiguous about ordering, draw it ambiguous and say which part was unclear.

**Never restate the skill in prose.** The user has the file. The diagram is the output.

**Count programmatically.** Phases and branches get counted from the extraction, not estimated.

**No source, no diagram.**
