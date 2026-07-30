"""
Clementine — her face and her brain, on one address.

Serves the built Svelte interface from webapp/dist alongside the JSON API,
so there is a single origin: no CORS, and a phone needs no configuration
beyond the address itself. Shares the same brain and memory folder as the
terminal version (clementine.py), so you can switch between them freely.

    pip install -r requirements.txt
    cd webapp && npm install && npm run build && cd ..
    python server.py                  # everything at http://127.0.0.1:5000

During development, run vite instead and it will proxy to this API:

    python server.py                  # brain
    cd webapp && npm run dev           # face, on its own port

Binds 127.0.0.1 by default. --host exists for putting her behind a reverse
proxy you control, and warns when used, because this server has no
authentication of its own — that is the proxy's job (see deploy/).
"""

import argparse
from pathlib import Path

import requests
from flask import Flask, Response, jsonify, request, send_from_directory

from crystalcore import (Clementine, Verdict, delete_profile, destination_of,
                         list_profiles, profile_dir, profile_meta)
from crystalcore import profiles as _profiles
from crystalcore.companion import EMBED_URL, OLLAMA_HOST, OLLAMA_URL

WEBAPP_DIST = Path(__file__).parent / "webapp" / "dist"


def _profile_of(companion: Clementine) -> str:
    p = Path(companion.memory_dir)
    return p.name if p.parent == Path(_profiles.PROFILES_DIR) else "default"


def create_app(companion: Clementine) -> Flask:
    app = Flask(__name__)
    holder = {"c": companion}  # swapped in place when the profile changes

    @app.after_request
    def allow_local_webapp(resp):
        # The Svelte dev server (vite) runs on another localhost port.
        # Only ever localhost origins — sovereignty means local only.
        origin = request.headers.get("Origin", "")
        if origin.startswith("http://127.0.0.1:") or origin.startswith("http://localhost:"):
            resp.headers["Access-Control-Allow-Origin"] = origin
            resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
            resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return resp

    @app.route("/api/<path:_any>", methods=["OPTIONS"])
    def preflight(_any):
        return ("", 204)

    # ---------- honesty endpoints ----------

    @app.get("/api/health")
    def health():
        """What is actually true right now — not what we hope is true."""
        c = holder["c"]
        models, reachable = [], False
        try:
            r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=3)
            r.raise_for_status()
            models = [m.get("name") for m in r.json().get("models", [])]
            reachable = True
        except requests.exceptions.RequestException:
            pass
        return jsonify({
            "ok": True,
            "model": c.model,
            "model_present": c.model in models if reachable else None,
            "models": models,
            "ollama": reachable,
            "ollama_host": OLLAMA_HOST,
            # "local" means the model runs on this same machine.
            "destination": destination_of(OLLAMA_URL),
            "embeddings": c._embed_ok,
            "audit_entries": len(c.audit.entries()) if c.audit else 0,
        })

    @app.get("/api/audit")
    def audit():
        """The continuity record, read-only, with its own integrity verdict."""
        c = holder["c"]
        if not c.audit:
            return jsonify({"entries": [], "intact": None,
                            "note": "auditing is disabled for this session"})
        intact, problems = c.audit.verify()
        entries = c.audit.entries()
        limit = request.args.get("limit", type=int)
        return jsonify({
            "entries": entries[-limit:] if limit else entries,
            "total": len(entries),
            "intact": intact,
            "problems": problems,
            "head": c.audit.head(),
        })

    @app.get("/api/status")
    def status():
        c = holder["c"]
        return jsonify({
            "name": c.personality.name or "Clementine",
            "avatar": c.personality.avatar,
            "model": c.model,
            "profile": _profile_of(c),
            "human_name": c.personality.human_name,
            "last_seen": c.time_since_last(),
        })

    @app.post("/api/chat/stream")
    def chat_stream():
        message = ((request.get_json(silent=True) or {}).get("message") or "").strip()
        if not message:
            return jsonify({"error": "empty message"}), 400
        return Response(holder["c"].chat_stream(message),
                        mimetype="text/plain; charset=utf-8",
                        headers={"X-Accel-Buffering": "no"})

    @app.get("/api/memories")
    def memories():
        c = holder["c"]
        facts = [{"handle": k, "text": f"{k}: {v['value']}",
                  "tags": v.get("tags") or []}
                 for k, v in c.memory.facts.items()]
        notes = [{"handle": f"n{i}", "text": n["text"],
                  "tags": n.get("tags") or []}
                 for i, n in enumerate(c.memory.notes, 1)]
        reflections = [{"handle": f"r{i}", "text": r["text"], "tags": []}
                       for i, r in enumerate(c.memory.reflections, 1)]
        return jsonify({"facts": facts, "notes": notes,
                        "reflections": reflections})

    @app.post("/api/reflect")
    def reflect():
        return jsonify({"insights": holder["c"].reflect()})

    @app.post("/api/teach")
    def teach():
        data = request.get_json(silent=True) or {}
        text = (data.get("text") or "").strip()
        key = (data.get("key") or "").strip()
        if not text:
            return jsonify({"ok": False, "error": "empty"}), 400
        if key:
            holder["c"].remember_fact(key, text)
        else:
            holder["c"].remember(text)
        return jsonify({"ok": True})

    @app.post("/api/forget")
    def forget():
        handle = ((request.get_json(silent=True) or {}).get("handle") or "").strip()
        forgotten = holder["c"].forget(handle)
        return jsonify({"ok": bool(forgotten), "forgotten": forgotten})

    @app.get("/api/profile")
    def profile_get():
        c = holder["c"]
        current = _profile_of(c)
        names = list_profiles()
        if current not in names:
            names = [current] + names
        profiles = []
        for n in names:
            if n == current:
                profiles.append({"profile": n,
                                 "avatar": c.personality.avatar,
                                 "description": c.personality.description,
                                 "name": c.personality.name,
                                 "model": c.model})
            elif n == "default":
                profiles.append({"profile": n, "avatar": "",
                                 "description": "", "name": "", "model": ""})
            else:
                profiles.append(profile_meta(n))
        return jsonify({"current": current, "profiles": profiles})

    @app.post("/api/profile/meta")
    def profile_meta_set():
        data = request.get_json(silent=True) or {}
        c = holder["c"]
        if "avatar" in data:
            c.personality.avatar = str(data["avatar"]).strip()[:8]
        if "description" in data:
            c.personality.description = str(data["description"]).strip()[:200]
        if "model" in data and str(data["model"]).strip():
            c.set_model(str(data["model"]))
        if data.get("choose_name"):
            chosen = c.choose_own_name()
            if not chosen:
                return jsonify({"ok": False,
                                "error": "she couldn't settle on a name — try again"})
            c.save()
            return jsonify({"ok": True, "name": chosen})
        c.save()
        return jsonify({"ok": True})

    @app.post("/api/profile/delete")
    def profile_delete():
        name = ((request.get_json(silent=True) or {}).get("profile") or "").strip()
        if name == _profile_of(holder["c"]):
            return jsonify({"ok": False,
                            "error": "switch away before deleting the active profile"}), 400
        return jsonify({"ok": delete_profile(name)})

    @app.post("/api/profile")
    def profile_switch():
        name = ((request.get_json(silent=True) or {}).get("profile") or "").strip()
        try:
            target = profile_dir(name)
        except ValueError:
            return jsonify({"ok": False, "error": "invalid name"}), 400
        old = holder["c"]
        holder["c"] = Clementine(model=old.model, memory_dir=target,
                                 embed_model=old.embed_model)
        c = holder["c"]
        return jsonify({"ok": True, "profile": _profile_of(c),
                        "name": c.personality.name or "Clementine"})

    # ---------- her face, from the same address ----------

    @app.get("/")
    @app.get("/<path:asset>")
    def webapp(asset: str = "index.html"):
        """Serve the built Svelte interface. Anything unrecognised falls back
        to index.html so client-side routes work on a hard refresh."""
        if not WEBAPP_DIST.exists():
            return Response(
                "Clementine's interface has not been built yet.\n\n"
                "    cd webapp && npm install && npm run build\n\n"
                "Her API is running and answering at /api/status — this "
                "address just has no face to show you.\n",
                mimetype="text/plain", status=503)
        target = (WEBAPP_DIST / asset)
        if not target.is_file():
            asset = "index.html"
        return send_from_directory(WEBAPP_DIST, asset)

    return app


def main():
    parser = argparse.ArgumentParser(
        description="Clementine — her face and her brain on one address.")
    parser.add_argument("--model", default="llama3.1:8b",
                        help="Ollama model tag (same choices as the CLI).")
    parser.add_argument("--memory-dir", default="clementine_memory",
                        help="Her memory folder (shared with the CLI).")
    parser.add_argument("--profile", default="",
                        help="Named profile (separate person, separate memory).")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--host", default="127.0.0.1",
                        help="Interface to bind. Leave as 127.0.0.1 unless an "
                             "authenticating reverse proxy sits in front.")
    parser.add_argument("--remote-model-ok", action="store_true",
                        help="Consent, given once here, for this server to use "
                             "a model that is not on this machine (OLLAMA_HOST). "
                             "Without it, non-local model calls are refused.")
    args = parser.parse_args()
    if args.profile:
        args.memory_dir = profile_dir(args.profile)

    # No human is watching a web server's stdin, so consent cannot be asked
    # for per call. It is given once, here, as a deliberate flag — and every
    # call it permits says so in the audit log rather than appearing unremarked.
    asker = None
    if args.remote_model_ok:
        def asker(_request):  # noqa: E306
            return Verdict(True, "pre-authorised at startup with --remote-model-ok",
                           remember=False)

    companion = Clementine(model=args.model, memory_dir=args.memory_dir,
                           asker=asker)
    app = create_app(companion)
    name = companion.personality.name or "Clementine"

    where = destination_of(OLLAMA_URL)
    print(f"{name} is at http://{args.host}:{args.port}")
    print(f"  model     {companion.model} on {'this machine' if where == 'local' else where}")
    if where != "local" and not args.remote_model_ok:
        print("            refusing to use it — pass --remote-model-ok to consent")
    print(f"  face      {'built' if WEBAPP_DIST.exists() else 'NOT BUILT — cd webapp && npm run build'}")
    print(f"  record    {companion.audit.path if companion.audit else 'disabled'}")

    if args.host not in ("127.0.0.1", "localhost"):
        print()
        print(f"  WARNING: bound to {args.host}, not loopback. This server has")
        print("  no authentication of its own — anyone who can reach this port")
        print("  can talk to her and read her memory. Put an authenticating")
        print("  reverse proxy in front of it (see deploy/).")
    print()
    print("Ctrl+C to say goodnight.")
    # debug=False always: the Werkzeug debugger is a remote shell.
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
