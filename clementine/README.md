# Clementine — the sovereign companion

She runs on hardware you own. By default that is the machine in front of you and
nothing she hears leaves it; if you choose to run her on a server of your own, she
says so plainly rather than continuing to claim otherwise.

## Layout

- `clementine.py` — the terminal interface
- `crystalcore/` — the framework: brain, layered memory, profiles
  - `consent.py` — the gate: nothing goes to a model elsewhere without a yes
  - `audit.py` — the record: every call, hash-chained so it cannot be edited quietly
- `server.py` — the JSON API, and her face, on one address
- `webapp/` — the Svelte interface
- `verify_audit.py` — check the record has not been tampered with
- `deploy/` — putting her on a server you own, behind HTTPS and a password

## Running her

Prerequisite: [Ollama](https://ollama.com) with a model pulled, e.g.
`ollama pull llama3.1:8b`. Optionally `ollama pull nomic-embed-text`, which gives
her semantic recall instead of keyword matching.

### Terminal

```bash
pip install -r requirements.txt
python clementine.py
```

### Web interface

One address for both her face and her brain:

```bash
cd webapp && npm install && npm run build && cd ..
python server.py                 # everything at http://127.0.0.1:5000
```

Or, while working on the interface itself, run vite separately and let it proxy
the API:

```bash
python server.py                 # brain
cd webapp && npm run dev          # face, on its own port
```

Both interfaces share the same memory folder (`clementine_memory/` by default),
so you can move between terminal and browser freely. `--profile <name>` on either
keeps separate people separate.

## Where she runs, and how you can tell

Her model is wherever `OLLAMA_HOST` points — by default this machine. Anywhere
else and every call needs your consent:

- In the terminal she asks, and you answer yes, always-this-session, or no.
- `server.py` cannot ask a human at a prompt, so consent is given once at
  startup with `--remote-model-ok`, and every call it permits records that as its
  reason instead of passing unremarked.
- With no way to ask, a non-local call is **refused**. A gate that opens when
  nobody is there to ask is just a door.

The interface shows `on this machine` or `via <host>` from a live check, never a
hardcoded assumption.

## The record

Every model call — allowed or refused — is one line in `audit.jsonl` beside her
memory, each carrying the SHA-256 of the line before it. Edit an entry or remove
a line and the chain breaks detectably:

```bash
python verify_audit.py --show
```

It stores sizes and destinations, never what was said. Refusals are recorded as
carefully as approvals, because a log of only what succeeded would flatter the
system rather than describe it.

## Putting her on a server

See [`deploy/DEPLOY.md`](deploy/DEPLOY.md) — one script does it, and the runbook
starts from "how do I even get a terminal". HTTPS is required rather than
recommended: without it Safari blocks the microphone and Add to Home Screen gives
you a bookmark instead of an app.

## Still to come

Voice conversation and webcam sight are on the roadmap. Both will run through the
same gate and the same record as everything else here.
