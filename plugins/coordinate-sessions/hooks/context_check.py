#!/usr/bin/env python3
"""PostToolUse hook: tell the model its real context size once it gets large.

Models in Claude Code can't see their own token count, so a rule like "hand over at
~150k" only works if something measures it. This reads the latest usage figure from
the session transcript (incrementally, so it stays cheap) and adds a reminder:

- coordinator sessions (ran the coordinate-sessions skill): at 150k, then every +25k
- every other session: at 200k, then every +50k

It never blocks and never fails loudly: any error means no output.
"""
import json
import os
import sys
import tempfile

COORD_AT, COORD_STEP = 150_000, 25_000
OTHER_AT, OTHER_STEP = 200_000, 50_000
STATE_DIR = os.path.join(tempfile.gettempdir(), "coordinate-sessions-context")


def scan(path, state):
    """Read transcript lines added since the last call; update context and coordinator flag."""
    size = os.path.getsize(path)
    if size < state["offset"]:  # transcript rewritten: start over
        state.update(offset=0, ctx=0)
    with open(path, "rb") as f:
        f.seek(state["offset"])
        chunk = f.read()
    end = chunk.rfind(b"\n")
    if end < 0:
        return
    state["offset"] += end + 1
    for raw in chunk[: end + 1].splitlines():
        if not state["coord"] and b"coordinate-sessions" in raw and (
            b'"name":"Skill"' in raw or b'"name": "Skill"' in raw or b"<command-name>" in raw
        ):
            state["coord"] = True
        if b'"usage"' not in raw:
            continue
        try:
            d = json.loads(raw)
            if d.get("type") != "assistant" or d.get("isSidechain"):
                continue
            u = d["message"]["usage"]
        except (ValueError, KeyError, TypeError):
            continue
        ctx = (u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
               + u.get("cache_creation_input_tokens", 0))
        if ctx:
            state["ctx"] = ctx


def message(state):
    ctx, k = state["ctx"], state["ctx"] // 1000
    at, step = (COORD_AT, COORD_STEP) if state["coord"] else (OTHER_AT, OTHER_STEP)
    if ctx < at:
        return None
    level = at + (ctx - at) // step * step
    if level <= state["warned"]:
        return None
    state["warned"] = level
    if state["coord"]:
        return (f"Context check: this coordinator session is at ~{k}k tokens, past the ~150k "
                "handover trigger in coordinate-sessions. Finish the current merge or phase, then "
                "write coordinator-N-handover.md as section 6 says and tell David. Skip it only if "
                "fewer than ~20 of your calls of work remain.")
    return (f"Context check: this session is at ~{k}k tokens. At the next natural break, suggest "
            "to the user in one line that they continue in a fresh session, and say what it "
            "should start from.")


def main():
    data = json.load(sys.stdin)
    if data.get("agent_id") or data.get("agent_type"):  # subagent tool call
        return
    path, sid = data.get("transcript_path"), data.get("session_id")
    if not path or not sid or not os.path.isfile(path):
        return
    os.makedirs(STATE_DIR, exist_ok=True)
    state_path = os.path.join(STATE_DIR, f"{sid}.json")
    state = {"offset": 0, "ctx": 0, "coord": False, "warned": 0}
    try:
        with open(state_path) as f:
            state.update(json.load(f))
    except (OSError, ValueError):
        pass
    scan(path, state)
    note = message(state)
    with open(state_path, "w") as f:
        json.dump(state, f)
    if note:
        print(json.dumps({
            "systemMessage": f"Context at ~{state['ctx'] // 1000}k tokens.",
            "hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": note},
        }))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
