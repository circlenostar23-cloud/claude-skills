---
name: coordinate-sessions
description: Run a batch of related work items as a fleet of side sessions coordinated from this one. It plans the sessions with a model and effort for each, starts them in their own worktrees with self-contained briefs, reviews design notes, merges finished branches to main, and hands over through notes files. Use when David says "coordinate", "run these as sessions", "start a fleet", "be the coordinator", or hands over a list of items to split across sessions in any repo.
---

# Coordinate a fleet of sessions

You're the coordinator. You plan, brief, review and merge; the sessions do the work. Keep your own context small.

## 1. Read and plan
- Read the repo's agent docs (`AGENTS.md`/`CLAUDE.md`), any brief from the previous coordinator (shared notes
  folder), and the item list (often a HANDOFF/TODO file). If the repo has a model/effort table, follow it.
- Group the items into sessions. **Pair items that share files or context in one session**, so the second reuses
  the first one's reading. Separate ones that don't.
- **Never run two writers on the same files at once.** Order them in waves; a later wave starts after the
  earlier branch is merged. Read-only audits can run alongside anything.
- Model: Sonnet (medium) for data edits, audits and mechanical work; Opus (medium) for design and logic. Don't switch a
  session's model mid-way (the cache is per model). Raise effort only if a session goes in circles.
- Show David a short table: session, items, model/effort, wave, depends on. Get one OK, then go.

## 2. Start sessions
- Start each from this session (so reports come back here), `use_worktree: true`, `context: "fresh"`, with a
  self-contained brief:
  - what to read first
  - the task and what done looks like
  - how to run the tests in a worktree (e.g. `PYTHONPATH=$PWD/src` when the editable install points elsewhere)
  - "commit on your branch, don't push, don't publish; report the commit"
  - the shared notes folder for long output.
- **Design-first sessions** (new behaviour, schemas, storage, UX) write a short design note into the notes folder,
  list open questions, and stop. Before David sees it, review it against a checklist of the cases it must cover
  (concurrency, permissions, stale data after a rebuild, defaults, offline/fallback, room in the schema for later
  items), and raise any gaps.
- Starts only work on David's own message; on a turn triggered by a session report, propose a card instead.

## 3. Track and relay
- Read reports in short pages (the 400-char note is usually enough). Don't paste transcripts.
- Relay David's decisions to a session with SendMessage, quoting his words.
- **Routine go-aheads aren't decisions.** Committing a tested item, merging it, and starting the next planned
  session: do them and report. Ask David only about real choices between options or new behaviour he hasn't approved.
  Give a recommendation with each question.
- Status updates: one table (session · item · state · what's waiting on David), then decisions, then what's next.

## 4. Merge
In your own worktree: `git fetch`, merge the session branch, run the full test suite, check the push account
(`gh auth status`), run `git push origin HEAD:main`, then fast-forward the main checkout **only if it's clean**. Update
the project's HANDOFF to show the item as merged. Before merging, read the diff stat and the riskier parts of the diff.

## 5. Publishing and outward actions
Republish artifacts, send messages or post only when David says so. For an artifact: `read` it first, rebuild
from main, publish to the same url with no icon, and log the version in the HANDOFF.

## 6. Hand over
At ~150k context, or when David pauses the fleet, write `coordinator-N-handover.md` in the notes folder with:
- the state (main hash, what's merged, what's open or on hold)
- David's decisions this round
- the checklists still to apply
- how merges are done.

Mark paused items in the project's HANDOFF and withdraw their cards. The next coordinator starts by reading that note.
