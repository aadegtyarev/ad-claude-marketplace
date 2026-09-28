---
name: repo-docs
description: "Write, rewrite and review the documentation that lives in a repository — README, docs/, guides and onboarding shipped next to the code. Splits pages by reader task (tutorial / how-to / reference / explanation), strips the tells of machine-written prose, adds Mermaid diagrams that show mechanism rather than boxes, and verifies links, anchors and facts against the source. Use when the user asks to write, rewrite, tidy up or review a README or a docs/ page, wants a page documenting a feature, asks for diagrams in the docs, or says the documentation reads like AI slop — «документация как ИИ-слоп», «сделай по-человечески», «перепиши доки», «напиши README», «нужны схемы в доках». NOT for: wiki.wirenboard.com pages (wiki-translator), community device templates and their wiki pages (community-template), design plans written before implementation (plan-feature), code comments, docstrings, commit messages, PR descriptions."
---

# repo-docs — documentation that ships with the code

A model asked to "write the documentation" produces a recognisable artefact: one wall
of text, every sentence propped up by a trailing dash clause, rationale interleaved
with instructions, no diagrams. This skill is how not to do that.

Scope is the repository: `README.md`, `docs/`, onboarding and guides that live next to
the code they describe. Everything on the wiki belongs to other skills; see
**Boundaries**.

## Quick Start

Six steps, in this order. Skipping the first is the main reason docs come out as slop.

1. **Read the source, not the old docs.** CLI entry points, settings, data models.
   Docs written from docs inherit their errors, and a fresh error reads more
   convincingly than an old one.
2. **Split by reader task** — see the routing table below. One page, one task.
3. **Sketch the page skeletons** before writing prose — `references/page-shapes.md`.
4. **Write, showing real command output** — copied from the code or from an actual run,
   never invented.
5. **Draw only diagrams that show mechanism** — `references/diagrams.md`.
6. **Verify mechanically** before handing over:
   `uv run plugins/repo-docs/skills/repo-docs/scripts/check_docs.py <repo root>`
   (outside the marketplace checkout: `uv run "<path-to-repo-docs-plugin>/skills/repo-docs/scripts/check_docs.py" <repo root>`)

## Hard rules — never violate without explicit user OK

- **Never write documentation from documentation.** Every factual claim — a port, a
  flag, a path, a unit name, an output format — is checked against the code in this
  session. No confirmation in the source means don't write it, or ask.
- **Never invent command output or file contents.** A reader will diff it against the
  real thing and stop trusting the whole page.
- **Rationale does not live in a how-to.** "Why we built it this way" goes on the
  explanation page; the how-to keeps the action and its result.
- **README is a door, not a house.** Target ≤150 lines: what it is, a diagram, a quick
  start, a map of the rest. Everything else is a link.
- **Never rename or delete an existing docs file blind.** `grep -rn '<filename>' .`
  across the whole repo first, source included: docstrings and user-facing CLI output
  link to docs more often than you'd expect.
- **State the limits.** A "what this doesn't do" section does more for trust than the
  rest of the page. Never quietly drop one that already exists.

## Boundaries — what belongs to other skills

| The user is asking about | Skill |
| --- | --- |
| A page on wiki.wirenboard.com, translating or auditing it | `wiki-translator` |
| Publishing a community device template, including its wiki page | `community-template` |
| A design plan for something not built yet (`docs/<topic>_plan.md`) | `plan-feature` |
| Whether a diff's docs match the change, as part of a review | `code-review-orchestrator` |
| A PR description or a commit message | `pr-author`, `workflow` |
| Docstrings and comments inside source files | none — ordinary code work |

The line against `plan-feature` is the one worth holding: it writes the design of
something that does not exist yet, this skill documents what already runs. Both live in
`docs/`. When a plan has been implemented and the user wants the feature documented for
real, that is this skill, and the plan is input, not a draft to publish.

## Where each page belongs

Four different reader needs ([Diátaxis](https://diataxis.fr/)). They do not coexist on
one page.

| The reader wants | Form | Sign you have drifted |
| --- | --- | --- |
| To learn from zero | Tutorial: one path through, every step verifiable | Branches appear — "if you have X instead" |
| To get a task done | How-to: goal or symptom → steps | Paragraphs of "why we chose" appear |
| To look up a fact | Reference: tables, complete, no narrative | "We recommend" appears |
| To understand it | Explanation: mechanism, decisions, trade-offs | Copy-pasteable commands appear |

Four forms does not mean four files. A small repo is well served by a README plus two
pages. `references/page-shapes.md` has the skeletons and a sizing table.

## Tells of machine-written prose

Full catalogue with before/after pairs in `references/anti-slop.md`. Open it at the
editing pass, not while drafting. The short list:

- A trailing dash clause hedging almost every sentence.
- Self-justification inside an instruction: "this is deliberate, because…".
- A bold lead-in on every bullet. When everything is emphasised, nothing is.
- Nested parentheses, "not just X, but Y".
- Sentences over ~25 words, and identical paragraph rhythm throughout.
- Hedging: "generally", "it's worth noting", "in most cases".
- Restating the obvious: a caption that repeats the command above it.

Read the page aloud. Where you run out of breath, edit.

**Russian docs:** the dash tell does not transfer. In Russian the copula dash
(«Схема — способ не читать абзац дважды») is grammatically required and is not a hedge.
Judge by the kind of dash, not the count — `references/anti-slop.md` §1 has the table.

## Diagrams

A diagram earns its place when it carries what the text cannot: who calls whom, what
happens in what order, what turns into what. Three boxes labelled with layer names is a
table of contents drawn as a picture.

| To show | Mermaid type |
| --- | --- |
| Who connects to whom, and which way | `flowchart LR` |
| Ordering, a race, a fallback | `sequenceDiagram` with `alt` / `par` |
| A daemon loop, a state machine | `flowchart TD` with a back edge |
| The shape of the data | `erDiagram` |

GitHub renders Mermaid inline. Colours that survive both themes, the `linkStyle` trap
and how to validate: `references/diagrams.md`.

## Before you hand it over

- [ ] Every fact checked against the code.
- [ ] Command output is real.
- [ ] Internal links and anchors resolve (script).
- [ ] Mermaid blocks parse, `linkStyle` indices in range (script).
- [ ] No dangling references to renamed files, source included.
- [ ] README still fits through the door.
- [ ] The repo's own tests and linter pass, if source was touched.
- [ ] Editing pass done against `references/anti-slop.md`.

## References

- `references/anti-slop.md` — catalogue of machine-prose tells with before/after pairs,
  English and Russian. Open it at the editing pass.
- `references/page-shapes.md` — skeletons for each of the four forms, plus what a good
  README contains and how many pages a repo of a given size needs. Open it at step 3.
- `references/diagrams.md` — Mermaid recipes per job, colours for both themes, the
  `linkStyle` index trap, validation tiers. Open it once you decide to draw.

## What the agent does NOT do

- **Write documentation without reading the code**, even when asked to "just fix the
  style": a style pass almost always uncovers factual errors.
- **Carry a claim from the old docs into the new ones unverified.**
- **Multiply pages for the sake of structure.**
- **Fix style by changing meaning.** If a caveat had to go to make a sentence pretty,
  the caveat comes back and the sentence gets rewritten.
- **Delete a "known limitations" section** because it spoils the tone.
- **Commit or push** doc changes unasked.
- **Touch the wiki.** Publishing, translating and auditing wiki pages is
  `wiki-translator` and `community-template`, both of which write to a live public site.

## When to ask the user

- The documentation language is not obvious — code and CLI in English, the conversation
  in Russian. Ask once, then hold to the answer.
- A rewrite breaks external links (a file is renamed but was linked from PyPI, the wiki
  or a ticket) — offer to keep the old name on the closest surviving page.
- You found a factual error in the old docs that looks like a bug in the code, not in
  the text — surface it separately, do not fix it silently.
- Scope: a full rewrite versus a targeted edit. If the ask was "tidy up" but the honest
  answer is a teardown, say so before tearing down.

## Documentation

- Diátaxis: <https://diataxis.fr/>
- Plain-language principles: <https://www.archives.gov/open/plain-writing/10-principles.html>
- Mermaid: <https://mermaid.js.org/intro/>

