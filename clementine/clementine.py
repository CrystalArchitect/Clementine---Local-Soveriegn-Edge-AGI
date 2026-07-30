"""
Clementine — terminal interface for the CrystalCore sovereign companion.

The framework lives in the crystalcore/ package (memory, profiles, brain).
This file is her doorway from the command line:

    python clementine.py                    # default memory
    python clementine.py --profile Crystal  # a named profile
    python clementine.py --model llama3.2:3b

Everything runs on your own device. Nothing leaves it.
"""

import argparse
import sys

# Re-exported so `from clementine import ...` keeps working everywhere.
from crystalcore import (BASE_PROMPT, Clementine, Memory, Personality,  # noqa: F401
                         delete_profile, list_profiles, profile_dir,
                         profile_meta, terminal_asker)

HELP = """Commands:
  /name <name>      give her a name (or change it)
  /name             with no name: invite her to choose her own
  /iam <name>       tell her your name
  /remember <text>  ask her to permanently remember something (add #tags if you like)
  /fact <key> <value>  teach her a structured fact, e.g. /fact birthday June 3
                    (teach the same key again to correct it)
  /notes [#tag]     show what she remembers (optionally only one #tag)
  /forget <handle>  forget a fact by key or a note by number, e.g. /forget n2
  /editnote <n> <text>  rewrite a note, e.g. /editnote n1 she prefers dawn walks
  /summary [topic]  ask her to summarize what she remembers (optionally on a topic)
  /reflect          invite her to reflect and form gentle insights about you
                    (she also reflects on her own after long conversations;
                     insights appear in /notes as r1, r2... — /forget rN removes one)
  /style <text>     tune her voice, e.g. /style more poetic, fewer questions
  /temp <0.0-1.5>   set temperature (playfulness)
  /model <tag>      switch the local model, e.g. /model llama3.2:3b
  /exit             say goodbye (everything is saved automatically)
"""

def main():
    parser = argparse.ArgumentParser(
        description="Clementine — a sovereign, locally-run AI companion.")
    parser.add_argument(
        "--model", default="llama3.1:8b",
        help="Ollama model tag. Pick one that fits your hardware, e.g. "
             "llama3.1:8b (default, Q4_K_M — the sweet spot), "
             "llama3.1:8b-instruct-q5_K_M (higher quality), or "
             "llama3.2:3b (lighter machines).")
    parser.add_argument(
        "--memory-dir", default="clementine_memory",
        help="Where her memory is stored on this device.")
    parser.add_argument(
        "--profile", default="",
        help="Named profile (separate person, separate memory), e.g. "
             "--profile Crystal. Profiles live in clementine_profiles/.")
    args = parser.parse_args()
    if args.profile:
        args.memory_dir = profile_dir(args.profile)

    print("Starting Clementine (local mode)...")
    print("Make sure Ollama is running with a model loaded.\n")

    # In the terminal a human is present, so she can ask before sending
    # anything to a model that is not on this machine.
    companion = Clementine(model=args.model, memory_dir=args.memory_dir,
                           asker=terminal_asker)

    name = companion.personality.name or "Clementine"
    returning = bool(companion.memory.conversation or companion.memory.summaries)
    gap = companion.time_since_last()
    greeting = f"{name} is {'back with you' if returning else 'ready'}"
    if gap:
        greeting += f" — you last spoke {gap}"
    print(f"{greeting}. Type /help for commands, /exit to quit.")
    if not companion.personality.name and not returning:
        print("She has no name yet — /name <name> to give her one, "
              "or just /name to let her choose her own.")
    print()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_input:
            continue

        if user_input.lower() in ("/exit", "exit", "quit"):
            break
        elif user_input.lower() == "/help":
            print(HELP)
        elif user_input.lower().rstrip() == "/name":
            print("[She is choosing her own name…]")
            chosen = companion.choose_own_name()
            if chosen:
                name = chosen
                print(f"[She has chosen her own name: {name}.]\n")
            else:
                print("[She couldn't settle on one — try /name again, "
                      "or give her one with /name <name>.]\n")
        elif user_input.lower().startswith("/name "):
            companion.set_name(user_input[6:])
            name = companion.personality.name
            print(f"[She is now called {name}.]\n")
        elif user_input.lower().startswith("/iam "):
            companion.personality.human_name = user_input[5:].strip()
            companion.save()
            print(f"[She knows you as {companion.personality.human_name}.]\n")
        elif user_input.lower().startswith("/remember "):
            companion.remember(user_input[10:])
            print("[Remembered, permanently.]\n")
        elif user_input.lower().startswith("/fact "):
            parts = user_input[6:].split(" ", 1)
            if len(parts) == 2:
                companion.remember_fact(parts[0], parts[1])
                print(f"[Fact remembered: {parts[0]} = {parts[1]}]\n")
            else:
                print("[Usage: /fact <key> <value>, e.g. /fact birthday June 3]\n")
        elif user_input.lower().startswith("/notes"):
            want = user_input[6:].strip().lstrip("#").lower()
            def _shown(store):
                return not want or want in (store.get("tags") or [])
            for key, fact in companion.memory.facts.items():
                if not _shown(fact):
                    continue
                tags = " ".join("#" + t for t in fact.get("tags") or [])
                print(f"  - {key}: {fact['value']}"
                      f"{'  [' + tags + ']' if tags else ''}  ({fact['updated']})")
            for i, note in enumerate(companion.memory.notes, 1):
                if not _shown(note):
                    continue
                tags = " ".join("#" + t for t in note.get("tags") or [])
                print(f"  n{i} - {note['text']}"
                      f"{'  [' + tags + ']' if tags else ''}  ({note['when']})")
            if companion.memory.reflections and not want:
                print("  her own reflections (hold lightly; /forget rN removes one):")
                for i, r in enumerate(companion.memory.reflections, 1):
                    print(f"  r{i} - {r['text']}  ({r['when']})")
            print()
        elif user_input.lower().startswith("/forget "):
            forgotten = companion.forget(user_input[8:])
            if forgotten:
                print(f"[Forgotten: {forgotten}]\n")
            else:
                print("[Nothing matched. Use a fact key or a note number from /notes.]\n")
        elif user_input.lower().startswith("/editnote "):
            parts = user_input[10:].split(" ", 1)
            if len(parts) == 2 and companion.edit_note(parts[0], parts[1]):
                print("[Note rewritten.]\n")
            else:
                print("[Usage: /editnote n<N> <new text> — numbers are in /notes]\n")
        elif user_input.lower().startswith("/style "):
            companion.personality.style_notes = user_input[7:].strip()
            companion.save()
            print("[Style noted.]\n")
        elif user_input.lower().startswith("/temp "):
            try:
                companion.personality.temperature = float(user_input[6:])
                companion.save()
                print(f"[Temperature set to {companion.personality.temperature}.]\n")
            except ValueError:
                print("[Please give a number, e.g. /temp 0.8]\n")
        elif user_input.lower().startswith("/model "):
            companion.set_model(user_input[7:])
            print(f"[Now using model: {companion.model} — remembered for this profile]\n")
        elif user_input.lower().startswith("/summary"):
            topic = user_input[8:].strip()
            print(f"{name}: {companion.summarize(topic)}\n")
        elif user_input.lower() == "/reflect":
            print(f"{name} reflects…\n{companion.reflect()}\n")
        else:
            print(f"{name}: ", end="", flush=True)
            companion.chat(user_input, stream_to=sys.stdout)
            print()

    print(f"\n{name} sleeps. Your conversations stay on this device, in "
          f"'{companion.memory_dir}/'. Non solus.")


if __name__ == "__main__":
    main()
