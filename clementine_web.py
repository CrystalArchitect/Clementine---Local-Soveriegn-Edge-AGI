"""
Clementine — local web interface

Runs only on your own machine (bound to 127.0.0.1, never exposed).
Shares the same brain and memory folder as the terminal version, so you
can switch between them freely. Nothing leaves your device.

    pip install -r requirements.txt
    python clementine_web.py            # then open http://127.0.0.1:5000
"""

import argparse
from pathlib import Path

from flask import Flask, Response, jsonify, render_template_string, request

from crystalcore import (Clementine, delete_profile, list_profiles,
                         profile_dir, profile_meta)
from crystalcore import profiles as _profiles

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ name }} — sovereign companion</title>
<style>
  :root{--bg:#000004;--ink:#E9EBF4;--muted:#A6ACC4;--purple:#A78BFA;
        --card:#07070F;--line:rgba(233,235,244,.12)}
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--ink);font-family:system-ui,sans-serif;
       display:flex;flex-direction:column;height:100vh}
  header{padding:14px 20px;border-bottom:1px solid var(--line);
         display:flex;justify-content:space-between;align-items:center}
  header b{color:var(--purple)}
  header small{color:var(--muted)}
  main{flex:1;display:flex;min-height:0}
  #chatcol{flex:2;display:flex;flex-direction:column;min-width:0}
  #log{flex:1;overflow-y:auto;padding:20px}
  .msg{max-width:70ch;margin:0 0 14px;padding:10px 14px;border-radius:12px;
       white-space:pre-wrap;line-height:1.55}
  .you{background:#141420;margin-left:auto}
  .her{background:var(--card);border:1px solid var(--line)}
  .her b{color:var(--purple)}
  form#send{display:flex;gap:10px;padding:14px 20px;border-top:1px solid var(--line)}
  input,button,textarea{font:inherit;color:var(--ink);background:#0D0D18;
       border:1px solid var(--line);border-radius:8px;padding:10px}
  input{flex:1}
  button{cursor:pointer;background:var(--purple);color:#050208;border:none;
         font-weight:600;padding:10px 18px}
  button.small{padding:2px 9px;font-weight:400;background:transparent;
               color:var(--muted);border:1px solid var(--line)}
  aside{flex:1;max-width:340px;border-left:1px solid var(--line);
        padding:16px;overflow-y:auto}
  aside h2{font-size:.95rem;color:var(--muted);margin-bottom:10px;
           text-transform:uppercase;letter-spacing:.08em}
  .mem{display:flex;justify-content:space-between;gap:8px;align-items:start;
       padding:8px 0;border-bottom:1px solid var(--line);font-size:.92rem}
  .mem .tags{color:var(--purple);font-size:.8rem}
  #teach{display:flex;flex-direction:column;gap:8px;margin-top:14px}
  footer{padding:10px 20px;color:var(--muted);font-size:.8rem;
         border-top:1px solid var(--line)}
  @media(max-width:760px){aside{display:none}}
</style>
<script defer src="/_vercel/speed-insights/script.js"></script>
</head>
<body>
<header><div><span id="heravatar"></span> <b id="hername">{{ name }}</b> · sovereign companion</div>
<div style="display:flex;gap:8px;align-items:center">
  <select id="profiles" title="Profile — separate person, separate memory"></select>
  <input id="newprofile" placeholder="new profile" size="9">
  <button class="small" id="mkprofile" type="button">create</button>
  <small>local only · 127.0.0.1</small>
</div></header>
<main>
  <div id="chatcol">
    <div id="log"></div>
    <form id="send">
      <input id="box" autocomplete="off" placeholder="Say something…" autofocus>
      <button>Send</button>
      <button type="button" id="stop" class="small" style="display:none">Stop</button>
    </form>
  </div>
  <aside>
    <h2>Her memory <button class="small" id="reflectbtn" type="button"
        title="Invite her to form gentle insights about you">reflect</button></h2>
    <div id="mems"></div>
    <form id="teach">
      <input id="teachtext" placeholder="Teach her something… (#tags ok)">
      <input id="teachkey" placeholder="Optional fact key (e.g. birthday)">
      <button>Remember</button>
    </form>
    <h2 style="margin-top:22px">This profile</h2>
    <form id="pmeta">
      <input id="pavatar" placeholder="Avatar emoji, e.g. 🌟" size="12">
      <input id="pdesc" placeholder="Short description" style="width:100%;margin-top:8px">
      <input id="pmodel" placeholder="Model for this profile (e.g. llama3.2:3b)" style="width:100%;margin-top:8px">
      <button style="margin-top:8px">Save profile</button>
    </form>
    <div style="margin-top:14px">
      <button class="small" id="delprofile" type="button">delete another profile…</button>
    </div>
  </aside>
</main>
<footer>Everything on this page stays on your device. Her memory lives in a
local folder you own. Non solus.</footer>
<script>
const log = document.getElementById('log');
function bubble(who, text){
  const d = document.createElement('div');
  d.className = 'msg ' + (who === 'you' ? 'you' : 'her');
  d.textContent = text;                 // textContent: nothing is ever HTML
  log.appendChild(d); log.scrollTop = log.scrollHeight;
  return d;
}
async function refreshMems(){
  const r = await fetch('/api/memories'); const data = await r.json();
  const box = document.getElementById('mems'); box.innerHTML = '';
  const all = [...data.facts, ...data.notes,
               ...(data.reflections || []).map(r => ({...r, text: '✨ ' + r.text}))];
  for (const m of all){
    const row = document.createElement('div'); row.className = 'mem';
    const left = document.createElement('div');
    left.textContent = (m.handle.startsWith('n') && /^n\\d+$/.test(m.handle)
                        ? m.handle + ' · ' : '') + m.text;
    if (m.tags.length){
      const t = document.createElement('div'); t.className = 'tags';
      t.textContent = m.tags.map(x => '#' + x).join(' ');
      left.appendChild(t);
    }
    const btn = document.createElement('button');
    btn.className = 'small'; btn.textContent = 'forget';
    btn.onclick = async () => {
      await fetch('/api/forget', {method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({handle: m.handle})});
      refreshMems();
    };
    row.appendChild(left); row.appendChild(btn); box.appendChild(row);
  }
}
let controller = null;
const stopBtn = document.getElementById('stop');
stopBtn.onclick = () => { if (controller) controller.abort(); };
document.getElementById('send').onsubmit = async (e) => {
  e.preventDefault();
  const boxEl = document.getElementById('box');
  const msg = boxEl.value.trim(); if (!msg) return;
  boxEl.value = ''; bubble('you', msg);
  const d = bubble('her', '');
  controller = new AbortController();
  stopBtn.style.display = 'inline-block';
  try {
    const r = await fetch('/api/chat/stream', {method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({message: msg}), signal: controller.signal});
    const reader = r.body.getReader();
    const dec = new TextDecoder();
    while (true){
      const {done, value} = await reader.read();
      if (done) break;
      d.textContent += dec.decode(value, {stream: true});
      log.scrollTop = log.scrollHeight;
    }
  } catch (err) {
    d.textContent += d.textContent ? ' — [stopped]' : '[stopped]';
  }
  stopBtn.style.display = 'none';
  controller = null;
  refreshMems();
};
async function refreshProfiles(){
  const r = await fetch('/api/profile'); const data = await r.json();
  const sel = document.getElementById('profiles'); sel.innerHTML = '';
  for (const p of data.profiles){
    const o = document.createElement('option');
    o.value = p.profile;
    o.textContent = (p.avatar ? p.avatar + ' ' : '') + p.profile +
                    (p.description ? ' — ' + p.description : '');
    if (p.profile === data.current){
      o.selected = true;
      document.getElementById('heravatar').textContent = p.avatar || '';
      document.getElementById('pavatar').value = p.avatar || '';
      document.getElementById('pdesc').value = p.description || '';
      document.getElementById('pmodel').value = p.model || '';
    }
    sel.appendChild(o);
  }
}
async function switchProfile(name){
  const r = await fetch('/api/profile', {method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({profile: name})});
  const data = await r.json();
  if (data.ok){
    document.getElementById('hername').textContent = data.name;
    log.innerHTML = '';
    bubble('her', `(profile: ${data.profile} — her memory of you here is separate)`);
    refreshProfiles(); refreshMems();
  }
}
document.getElementById('profiles').onchange = (e) => switchProfile(e.target.value);
document.getElementById('mkprofile').onclick = () => {
  const name = document.getElementById('newprofile').value.trim();
  if (name){ document.getElementById('newprofile').value = ''; switchProfile(name); }
};
document.getElementById('teach').onsubmit = async (e) => {
  e.preventDefault();
  const text = document.getElementById('teachtext').value.trim();
  const key = document.getElementById('teachkey').value.trim();
  if (!text) return;
  await fetch('/api/teach', {method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({text, key})});
  document.getElementById('teachtext').value = '';
  document.getElementById('teachkey').value = '';
  refreshMems();
};
document.getElementById('pmeta').onsubmit = async (e) => {
  e.preventDefault();
  await fetch('/api/profile/meta', {method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({avatar: document.getElementById('pavatar').value.trim(),
                          description: document.getElementById('pdesc').value.trim(),
                          model: document.getElementById('pmodel').value.trim()})});
  refreshProfiles();
};
document.getElementById('reflectbtn').onclick = async () => {
  const b = bubble('her', 'reflecting…');
  const r = await fetch('/api/reflect', {method:'POST'});
  const data = await r.json();
  b.textContent = data.insights;
  refreshMems();
};
document.getElementById('delprofile').onclick = async () => {
  const name = prompt('Delete which profile? (cannot be the active one — this erases its memory forever)');
  if (!name) return;
  if (!confirm(`Really delete profile "${name}" and all its memory? This cannot be undone.`)) return;
  const r = await fetch('/api/profile/delete', {method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({profile: name})});
  const data = await r.json();
  alert(data.ok ? `Profile "${name}" deleted.` : (data.error || 'Nothing deleted.'));
  refreshProfiles();
};
refreshProfiles(); refreshMems();
</script>
</body>
</html>"""


def _profile_of(companion: Clementine) -> str:
    p = Path(companion.memory_dir)
    return p.name if p.parent == Path(_profiles.PROFILES_DIR) else "default"


def create_app(companion: Clementine) -> Flask:
    app = Flask(__name__)
    holder = {"c": companion}  # swapped in place when the profile changes

    @app.get("/")
    def home():
        c = holder["c"]
        return render_template_string(
            PAGE, name=c.personality.name or "Clementine")

    @app.post("/api/chat")
    def chat():
        message = ((request.get_json(silent=True) or {}).get("message") or "").strip()
        if not message:
            return jsonify({"error": "empty message"}), 400
        return jsonify({"reply": holder["c"].chat(message)})

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

    return app


def main():
    parser = argparse.ArgumentParser(
        description="Clementine's local web interface (127.0.0.1 only).")
    parser.add_argument("--model", default="llama3.1:8b",
                        help="Ollama model tag (same choices as the CLI).")
    parser.add_argument("--memory-dir", default="clementine_memory",
                        help="Her memory folder (shared with the CLI).")
    parser.add_argument("--profile", default="",
                        help="Named profile (separate person, separate memory).")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
    if args.profile:
        args.memory_dir = profile_dir(args.profile)

    companion = Clementine(model=args.model, memory_dir=args.memory_dir)
    app = create_app(companion)
    name = companion.personality.name or "Clementine"
    print(f"{name} is at home: open http://127.0.0.1:{args.port}")
    print("Local only — nothing leaves this device. Ctrl+C to say goodnight.")
    # Never bind beyond localhost, never enable the debugger: sovereignty
    # means this page is reachable from this machine alone.
    app.run(host="127.0.0.1", port=args.port, debug=False)


if __name__ == "__main__":
    main()
