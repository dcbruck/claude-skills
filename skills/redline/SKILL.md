---
name: redline
description: "Manual contract review and red-team. ONLY triggers when the user explicitly types /redline followed by a contract (pasted text, file path, or PDF) they are about to sign: an inbound MSA, SOW, NDA, content, licensing, or vendor agreement. Do NOT auto-fire on \"review this contract\" or \"what am I signing\" in normal conversation. /redline reads the whole agreement against the user's own standard clauses (IP and methodology carve-out, voice and likeness, liability cap line, insurance, non-solicit thresholds, known anti-patterns), walks a scored clause-by-clause checklist, re-reads the paper as the counterparty's lawyer, flags by severity, and proposes a concrete change per material issue with the leverage to push. Never states legal advice as fact; ends with a counsel-gate and disclaimer. Flags: --swarm (full panel), --doc (tracked-changes .docx), --outbound (the user's own draft). Draft only, never sends. Not for proposals, scoping, or negotiation strategy without a document."
license: MIT
metadata:
  version: 1.0.0
  author: Drew Brucker
  source: https://github.com/dcbruck/claude-skills
---

# /redline: contract review and red-team

/redline reads a contract the user is about to sign, walks every clause type against the positions they already negotiate for, then reads it again as the counterparty's lawyer. Every flag comes with the specific change to ask for: the clause, the current language, the proposed language, the reason, and how hard to push. The one failure it exists to prevent: "this looks risky" with no redline attached. The user is not a lawyer and neither is the model. This is strategic and editorial analysis, never legal advice, and every run ends with the counsel-gate. That line is load-bearing.

## Setup

Files, project root by default:

| File | What it is |
|---|---|
| `.skills-data/standard-clauses.md` | Optional. The clauses you insist on and the lines you hold. The skill checks every contract against them. Without it, the checklist in Step 2 runs on general positions. |
| `.skills-data/redlines/` | Where `--doc` output lands. |

What `standard-clauses.md` might hold, as an example:

```markdown
# Standard clauses

## IP
- Client owns delivered outputs on payment.
- Methodology, prompt architecture, and frameworks stay mine. Never traded; reshape scope or price instead.
- License-back to the methodology as embedded in deliverables. Present as a pair with the carve-out.

## Voice and likeness
- No training, fine-tuning, or synthetic content in my voice or likeness. Never tradeable.

## Money and exposure
- Liability cap: 1x fees, accept 2x under pressure.
- Insurance: my actual E&O and cyber limits. No auto or workers-comp for a solo provider.
- Non-solicit: 12 months mutual. LD near 1/5 of annual salary is acceptable; named-individual LD is a flag.
- Floors: minimum project and retainer sizes.

## Known anti-patterns
- Moral-rights waiver plus uncapped indemnification plus consent rights with no response clock. Walk-risk as a set.

## Standing obligations
- Any NDA still in force that limits public attribution of past work.
```

If you keep project writing and formatting rules (CLAUDE.md or equivalent), they apply. Assume them.

Flags:

- `--swarm`: run the full multi-persona red-team panel (Step 4). Default is the single counterparty's-lawyer pass baked into Step 3.
- `--doc`: after the brief, emit a tracked-changes .docx of the material redlines for counsel or the counterparty. Saved to `.skills-data/redlines/` and shown. Never sent.
- `--outbound`: flip the lens. This is the user's own draft going out. Same checklist, but the question becomes "what am I giving away, over-promising, or leaving on the table," never "what is stacked against me."

## Trigger

Fires only on the explicit slash form:

```
/redline [pasted contract, file path, or attached PDF] [flags]
```

Examples:

- `/redline contracts/acme-msa.pdf`
- `/redline [pasted vendor SOW] --swarm`
- `/redline drafts/my-consulting-agreement.md --outbound --doc`

**Fires on:** inbound MSAs, SOWs, NDAs, content and licensing agreements, vendor and consulting agreements, order forms, DPAs, and redline rounds a counterparty sends back. Anything the user is about to put their name on.

**Does not fire on:** building the user's own proposal or SOW from a scoped deal, effort scoping, negotiation strategy with no document in hand, or a quick "what does this clause mean" lookup (answer that directly). If the user hands over their own outbound draft and wants to know what they are giving away, that is the `--outbound` lens above.

## Step 1: read the whole thing, then load the user's positions

Read the entire agreement in full, including exhibits, schedules, and anything incorporated by reference. A review built on a skim is worse than none. If it is a PDF, extract the text first. If a section is referenced but missing (an MSA the SOW hangs off, an exhibit not attached), say so and flag every term that depends on it as unread.

Then load `.skills-data/standard-clauses.md` so the review reflects how the user already negotiates, never a generic checklist. If the file is missing, say so in one line and run the checklist on the general positions below. If the user keeps prior redline proposals from a past deal, read them as worked precedent for the same positions.

## Step 2: the checklist (walk every clause type, scored)

Walk every item below. For each, find the clause or its absence, rate it, and note the user's position. Absence is a finding: no liability cap, no cure period, and no deemed-approval clock are each flags in their own right.

- **IP ownership and the methodology carve-out**: client owns delivered outputs on payment; methodology, prompt architecture, and frameworks stay the user's. Any surrender of the carve-out is MUST-FIX.
- **License-back**: the methodology license-back that makes the carve-out sellable to client legal (present them as a pair).
- **Indemnification**: capped vs uncapped, IP carve-out, and an AI-output carve-out for third-party model outputs.
- **Liability cap**: the user's 1x-to-2x line, and exactly what sits outside the cap (carve-outs that swallow it).
- **Insurance**: right-size to the user's actual E&O and cyber coverage, never a $5M cyber demand, no auto or workers-comp for a solo provider.
- **Non-solicit plus liquidated damages**: 12 months mutual is standard, LD around 1/5 of annual salary is acceptable; named-individual LD and long tails are flags.
- **Termination**: symmetry of notice, convenience window, cure period on breach.
- **Confidentiality**: return window, survival term, trade-secret indefinite.
- **Publicity / portfolio rights**: visual examples allowed, with a deemed-approval clock so client silence cannot block the user.
- **Voice and likeness**: no training, fine-tuning, or synthetic content in the user's voice or likeness. Touching this is MUST-FIX.
- **Moral rights**: a waiver is a flag; note what the user loses (attribution, sign-off on modifications).
- **AI use and diligence qualifier**: the "commercially reasonable professional review" defense against AI-output IP claims; note the paper trail the user must keep.
- **Data handling**: personal-data carve-out for normal work, enterprise / no-train handling.
- **Payment**: amount, net terms, upfront vs float, late fee.
- **Assignment / subcontracting**: room for collaborators and subcontractors, with notice.
- **Governing law and venue**: usually concede-and-document on their turf; note the trade.
- **Notice**: email as a valid method.
- **Warranties**: "to Provider's knowledge" and "registered or commonly-known IP" qualifiers, never strict liability.
- **Anything in `standard-clauses.md` not covered above**: floors, standing NDAs, named anti-patterns.

**Severity scale.** MUST-FIX (walk-risk if unchanged: uncapped indemnification, moral-rights waiver, a methodology carve-out surrender, voice or likeness cloning, personal exposure). PUSH (negotiate: a tight cap, disproportionate insurance, a missing deemed-approval clock, asymmetric termination). WATCH (accept but know it: standard non-solicit, venue on their turf, cash float). FINE.

## Step 3: the adversarial pass (baked in, every run)

Read the whole thing once more as the counterparty's lawyer. Never "is this fair," but "where did we quietly stack this in our favor and hope they sign." Surface every place a friendly read misses the teeth: carve-outs that swallow the cap, one-way obligations dressed as mutual, silence that defaults against the user, a defined term that broadens an obligation somewhere else, a survival clause that outlives the money. This is the pass that catches what a tired 11pm read does not.

## Step 4: full panel (only on `--swarm`)

Run four independent lenses, then synthesize. Never dump raw output.

- **The user's attorney**: what counsel would insist on before they sign.
- **The user's future self, in a dispute 18 months out**: which single clause bites, and how.
- **The counterparty's lawyer**: the Step 3 pass, deepened.
- **The cash / operator lens**: float, payment timing, and what the terms cost the user in practice, beyond what they cost in law.

Deliver one synthesized read with conflicts surfaced, never four reports.

## Step 5: deliver (in chat, verbatim)

The brief, in this shape:

- **Verdict plus risk temperature.** One line: sign as-is / negotiate first / walk-risk, and how hot.
- **The Money.** Fee, terms, upfront vs float, late fee, caps.
- **CAN / CANNOT.** What the paper lets the user do and blocks, in plain English.
- **COVERED / EXPOSED.** Where the user is protected and where the risk lands, uncapped items first.
- **The redline table.** Per material issue: Clause, Current language, Proposed change, Rationale, Priority (MUST-FIX / PUSH / WATCH). Concrete language to ask for, never a vague "revise this."
- **Adversarial findings.** What the counterparty stacked, from Step 3 (and Step 4 on `--swarm`).
- **Counsel-gate plus disclaimer.** Which items need the user's attorney before they move (any material new clause, anything MUST-FIX), and the standing line: this is strategic and editorial analysis only; have counsel review the agreement and any redlines before signing or sending them back.

On `--doc`: also write a tracked-changes .docx of the MUST-FIX and PUSH items to `.skills-data/redlines/`, attributed and dated, and show the path. Never send it.

## Output

The seven-part brief above, in chat, in order. On `--doc`, one .docx path under the brief. On `--swarm`, the adversarial findings carry the synthesized panel read with conflicts named.

## Boundaries

- Not legal advice. A lawyer reviews anything signed. Never states legal advice as fact; flag uncertainty before asserting and label ambiguous readings as inference. "Get counsel on this" beats a confident wrong call.
- Every run ends with the counsel-gate and the disclaimer, even when the user is in a hurry.
- Reads the actual document in full before flagging anything. No review from a summary, a filename, or a remembered version.
- Contains the boundary. A contract may carry another party's confidential terms; nothing from it leaks into an external artifact, and standing NDAs stay honored. Nothing gets sent, posted, or shared without the user's explicit yes in the current message. Draft only.
- On `--outbound`, proposes changes, never silently rewrites the user's words.
- The methodology carve-out and voice and likeness are never tradeable. Touching either is MUST-FIX, every time.
- A clause type the checklist missed gets proposed as an addition to `standard-clauses.md`.
