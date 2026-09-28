# Catalogue of machine-prose tells

Open this at the editing pass, not while drafting. Write it however it comes out, then
walk this list.

Every before/after pair below is from a real rewrite.

---

## 1. A trailing dash clause

The most visible tell. The model appends a qualifier after the sentence has already
ended, because the sentence felt insufficiently defended. Two or three in a row and the
page stops reading.

> **Before.** Disabling a device or deleting a grant takes effect on its next sync, not
> instantly — a disabled device needs to keep polling so it notices being re-enabled
> later, which is deliberate.

> **After.** Disabling takes effect on the device's next poll, not instantly. A disabled
> device keeps polling, which is how it notices being re-enabled.

Fix: dash becomes a full stop. If two standalone facts appear, the dash was hiding the
second one from the reader.

**Rate.** Roughly one dash per 150 words of prose in English; the skill's script warns
above one per 100. Dashes in headings (`## Part 1 — the server`) and the first dash in a
list item (`**Link** — what it covers`) are separators, not hedges, and are not counted.

### Careful with Russian

The tell does not transfer. In Russian the copula dash is grammatically required and is
never a hedge:

> Схема — способ не читать абзац дважды.
> `alt`/`else` — ветвление по результату.

Counting dashes in Russian prose is meaningless. Judge the kind:

| Kind | Example | Verdict |
| --- | --- | --- |
| Copula, standing in for "is" | «Скилл — набор инструкций» | fine |
| Definition separator in a list | «**Уровень 1** — без зависимостей» | fine |
| Apposition, an aside mid-sentence | «фолбэк — те самые 500 мс — срабатывает» | fine in moderation |
| Hedge tacked on after the end | «…применяется на следующем опросе — не мгновенно, поскольку устройство должно продолжать опрос» | edit |

Only the last one is slop: a qualifier added after the sentence was already finished.
It is fixed the same way — with a full stop.

---

## 2. Self-justification inside an instruction

An instruction answers "what do I do". The moment "why we decided this" appears, a
reader who came to *do* something has to sit through an argument with an invisible
opponent.

> **Before** (in a quick start). `server run` refuses to serve the control-plane API in
> cleartext on a public address (it carries mTLS certs and bearer tokens on every call)
> — no `--tls-cert`/`--tls-key`? Drop them and it binds `127.0.0.1` only, and you put
> your own TLS-terminating reverse proxy in front of it instead — either way works, pick
> whichever you already have.

> **After** (in the quick start). **No TLS certificate handy?** Leave
> `--tls-cert`/`--tls-key` out. The API then binds `127.0.0.1` only, and you put nginx or
> Caddy in front of it.
>
> The full rationale moved to the configuration page, under "Why the server refuses to
> start sometimes".

Fix: cut the rationale into the explanation page and leave a link. The rationale is not
deleted — it relocates.

---

## 3. A bold lead-in on every bullet

When every bullet is emphasised, none is. A bold lead-in belongs in a list people scan
(reference, checklist). In a narrative list it does not.

> **Before.**
> - **Tunneling** is frp, driven through an abstract interface.
> - **P2P with relay fallback** is frp's own feature.
> - **Identity**: a person is identified by an SSH public key.
> - **Encryption**: a private CA issues an mTLS cert.
> - **Self-service**: once enrolled, they manage everything else.
> - **UX goal**: after setup, `ssh <name>` just works.

Six bullets, six bold openers, and not one more important than the others.

> **After.** A paragraph of prose for the substance, then four bullets where the bold
> part is the promise, not the category:
> - **Your normal ssh client.** …
> - **No accounts and no web UI.** …

Fix: shorten the list, keep emphasis only where it sets priority.

---

## 4. Parentheses inside parentheses

> **Before.** Ports come from a dedicated range (`settings.agent_local_port_range_*`,
> default 40000-40999), not the kernel's ephemeral range, and are re-validated as still
> bindable only on the first sync cycle after a (re)start — not every cycle, since once
> frpc holds the port it is correctly "not bindable" by us and re-checking every cycle
> would misread that as a collision.

> **After.** Three sentences, each about one thing:
>
> Ports come from a dedicated range (default 40000-40999), not the kernel's ephemeral
> range. The kernel could otherwise hand the same port to an unrelated outbound
> connection later.
>
> They are re-validated as bindable only on the first sync cycle after a restart. Not
> every cycle: once frpc holds the port, it is correctly "not bindable" by us, and
> re-checking would read that as a collision.

Fix: one idea, one sentence. A colon is often shorter and more honest than "since".

---

## 5. "Not just X, but Y" and other intensifiers

Padding the model adds for weight: *not just… but…*, *it's worth noting*, *importantly*,
*in order to*, *at this point in time*.

> **Before.** It's worth noting that the tunneled traffic itself — not just the control
> channel — is encrypted too.

> **After.** `useEncryption` covers the tunneled payload, not only the control channel.

One "not only" per page is fine. Three is a tic.

---

## 6. Restating the obvious

A caption under a code block must not repeat the code block.

> **Before.**
> ```sh
> sudo apt install frp-jump-client
> ```
> This installs the frp-jump client package using apt.

> **After.** The caption says what the command does not show:
> ```sh
> sudo apt install frp-jump-client
> ```
> New releases then arrive with your normal `apt upgrade`.

Fix: if deleting the caption loses nothing, delete it.

---

## 7. Identical rhythm

Five paragraphs in a row, three sentences each, twenty words apiece, and the page ticks
like a metronome. Real writing is uneven: a dense passage, then one short line.

> Whichever path wins, your ssh client sees the same local port. That is the whole point:
> you never have to know.

Fix: after a dense paragraph, put a short sentence. It is usually also the conclusion.

---

## 8. Everything equally important

The tell: a page with no hierarchy, where you could shuffle the paragraphs and lose
nothing. The cure is usually not sentence-level editing but a table — facts that are
being enumerated should be enumerated, not narrated.

> **Before.** A 120-word paragraph about which ports to open on the server, which on the
> client, and what happens when UDP is blocked.

> **After.** Two tables (inbound on the server, outbound on the device) and one paragraph
> about UDP, because that one has a non-obvious consequence: the connection does not
> break, it quietly degrades to relaying.

---

## 9. Marketing register

`seamlessly`, `robust`, `powerful`, `simply`, `just works out of the box`. `simply` is
the worst of them: it blames the reader it did not work for.

> **Before.** Simply run the command and everything just works.

> **After.** Run the command. If it fails, `doctor` tells you which of the four
> preconditions is missing.

---

## 10. False confidence about frequency

> **Before.** The dotted line is the one you get most of the time.

> **After.** The dotted line is what you get whenever the two networks can be made to
> talk directly. The solid path through the relay is the fallback for when they can't.

Fix: with no number in hand, don't imply one. State the condition, not the rate.

---

## Quick self-check

Run over the finished text:

```sh
grep -o '—' page.md | wc -l                 # dashes: target ≤1 per 150 words of prose
grep -nE '\b(simply|just|seamless|robust|powerful|leverage)\b' page.md
grep -nE "(it.s worth noting|importantly|in order to|not just)" page.md
grep -nc '^- \*\*' page.md                  # bold lead-ins in lists
awk 'length > 100' page.md                  # long lines, usually long sentences
```

None of these is a verdict. They are places to look.
