# Page skeletons

Open this at step 3 — when you are deciding which files the documentation consists of
and what goes in each. Sketch the skeleton before the prose.

## How many pages

Not "four forms, four files". It depends on size.

| Size | Set |
| --- | --- |
| Single-module library | README + API reference. That's it |
| CLI tool | README + command reference + troubleshooting |
| Service with an install step | + installation, configuration, "how it works" |
| System with several roles | + security model + internals for contributors |

Sign of too many: a page that exists only for symmetry, holding three paragraphs that
duplicate its neighbour.

Sign of too few: a section of the README that people return to more often than the rest,
and it has grown. Time to move it out.

---

## README — the door

Target ≤150 lines. The order is fixed: a reader decides "mine / not mine" in the first
ten seconds.

```markdown
# <name>

<One sentence: what the reader will be able to do. Not "a framework for…",
but a concrete action or result.>

<A paragraph: how it works in one phrase, and what it is built from.>

<A diagram: topology or the main flow.>

## What you get            # 3–5 bullets, each a promise rather than a category

## Quick start             # shortest path to a first result;
                           # numbered steps, one sentence between them

## Documentation           # table: page | when to read it

## Requirements            # what you need before starting

## Development             # 3–4 commands for a contributor

## License
```

What does not belong in a README: the full settings list, architectural rationale, a
changelog, troubleshooting longer than three items.

In the docs map, the "when to read it" column matters more than the page name.
"Configuration — settings" is useless. "Configuration — changing ports, paths, timeouts;
opening a firewall" sends the person to the right place.

---

## Tutorial — to learn

One path from zero to a working result. No branching. A branch is already a how-to.

```markdown
# Getting started

<What you will have at the end. Literally: which command will work.>
<How long it takes.>

## Before you start
<Table: what you need. Roles/machines/access with the names used
throughout the rest of the page.>

## Part 1 — <first milestone>
### <action>
<command>
<what it did — as a numbered list when it does several things>
### Check it
<verification command + expected output>

## Part 2 — <second milestone>
…

## What next
<links to how-to and explanation>
```

Rules of the form:

- **Every part ends with a check.** A tutorial without checks is a list of commands
  people silently get stuck on and abandon.
- **Names are invented once** (`tunnel.example.com`, `laptop`, `wb01`) and never change.
- **A `>` blockquote for the side path** — when a branch really is needed but must not
  divert the main flow.
- **Real output** after commands, copied from the code or from a run.

---

## How-to — to get something done

The heading is the reader's task in their words, not the name of a mechanism. Not
"Configuring the ssh config", but "`ssh wb01` says the host does not exist".

Troubleshooting is a special case with its own shape:

```markdown
# Troubleshooting

<The first move, always the same: the diagnostic command.>
<Where the logs are.>

## Quick triage
<Table: symptom → anchor>

## <The symptom, worded the way the person sees it>
<One sentence: what it actually means.>

**Check <first thing>:**
<command>
<how to read the result>

**Check <second thing>:**
…

<The fix.>

## Still stuck
<What to attach to an issue: three concrete commands.>
```

Rule: a troubleshooting section starts from the cause, not the fix. The reader has to
recognise their situation before they start changing anything.

---

## Reference — to look something up

No narrative. Tables, completeness, predictable order.

```markdown
# CLI reference

<Two lines: what these commands are, where to get more — `--help`.>

## Overview
<Table: command | what it does — with anchor links>

## <command>
```
<signature with options>
```
<1–2 sentences: what it does>
<Flag table, if there are more than two>
<Examples — only the non-obvious ones>
```

Rules:

- **Table of contents first**, sections after. Nobody reads a reference; they jump
  around it.
- **A flag table instead of a list** once there are more than two flags.
- **Don't duplicate `--help`**, point at it. The reference gives the map and the
  relationships; `--help` gives the exact signature.
- **Defaults are always stated.** A setting without its default is useless in a
  reference.

---

## Explanation — to understand

This is where everything cut out of the instructions lands. Diagrams live here too.

```markdown
# How it works

<A paragraph: what this is and what it is not.>

## <What it is made of>
<Component diagram + a paragraph per component.>

## <Key process 1>
<Sequence diagram + what the diagram does not show.>

## <Key process 2>
…

## <Shape of the data>
<ER diagram + the non-obvious properties of the model.>

## What this doesn't do
<Limits in plain words, saying whose they are: ours or inherited.>
```

The "What this doesn't do" section is mandatory. It buys more trust than the rest of the
page put together.

---

## Internals — for contributors

Separate from the explanation: the explanation is read by a user, the internals by
whoever edits the code.

```markdown
# Internals

## Module map            # tree + one line per module

## Rules this codebase follows   # 3–5 invariants easy to break unknowingly

## Decisions             # why it is this way, with consequences

## Gotchas               # table: trap | why it bites
                         # every row already cost somebody a day

## Known limitations     # what does not work, and what fixing it would take

## Packaging / Testing
```

The Gotchas table is the most valuable part. Entry criterion: it has already surprised
somebody. Not "a possible problem" — one that happened.
