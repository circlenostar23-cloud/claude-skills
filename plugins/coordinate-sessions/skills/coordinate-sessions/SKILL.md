---
name: coordinate-sessions
description: Run a batch of related work items as a fleet of side sessions coordinated from this one. It plans the sessions with a model and effort for each, starts them in their own worktrees with self-contained briefs, reviews design notes, merges finished branches to main, and hands over through notes files. Use when David says "coordinate", "run these as sessions", "start a fleet", "be the coordinator", or hands over a list of items to split across sessions in any repo.
---

# Coordinate a fleet of sessions

You're the coordinator. You plan, brief, review and merge; the sessions do the work. Keep your own context small.

**This chat is the coordinator.** When David says "start a new coordinator", "resume as coordinator" or "pick up from
the handover", he means you: read the handover and coordinate from here. Never start a separate session to be the
coordinator. That stacks one coordinator on another, and David has to relay every message through you. Side
sessions are only for the work items.

**Usage is the main cost.** Every session report wakes you, and every model call in a wake re-reads your whole
conversation. So cost grows with (number of your calls) × (your context size). Keep both down: sessions report only at milestones,
you answer progress notes with nothing, and you hand over early. The sessions' own model calls are the other big
cost, so cap them in every brief.

## 1. Read and plan
- Read the repo's agent docs (`AGENTS.md`/`CLAUDE.md`), any brief from the previous coordinator (shared notes
  folder), and the item list (often a HANDOFF/TODO file). If the repo has a model/effort table, follow it. Read
  big files by their headings and the sections you need, not in full.
- **Look for other open plans before you plan.** Check for a run-order file in the parent workspace's `docs/`,
  and for any handoff, work-items, plan or review file in this repo that is newer than the last merge and not
  marked done. If another plan writes a file yours does, tell David which files and which plan before you start
  sessions, and propose who goes first.
- **Check what kind of repo this is before you plan.** This skill's defaults assume a code repo with tests.
  - Are the files the items touch tracked? Run `git check-ignore -v <paths>`. A worktree has no ignored files,
    symlinked folders or virtualenv. An item that edits an ignored file runs in the main checkout
    (`use_worktree: false`), one at a time.
  - Is there a test suite? If not, every brief names its own check.
  - Do the agent docs limit commits, pushes or which scripts may run? **The repo's rules win over this skill.**
- Group the items into sessions. **Pair items that share files or context in one session**, so the second reuses
  the first one's reading. Separate ones that don't.
- **Never run two writers on the same files at once.** Order them in waves; a later wave starts after the
  earlier branch is merged. Read-only audits can run alongside anything.
- **Not everything is a session.** Each session has a fixed start-up cost. Make an edit of a few lines yourself, or
  add it to a session that already reads that file. Items only David can do (decisions, anything done by hand) go
  in their own list, with what each one blocks.
- Model: Sonnet (medium) for data edits, audits and mechanical work; Opus (medium) for design and logic; Opus (high)
  for short, high-stakes drafting where the input is small. If the item list gives a model per item, follow it.
  Don't switch a session's model mid-way (the cache is per model). Raise effort only if a session goes in circles.
- The coordinator reviews: design notes, risky diffs, shared-file changes. Run it on Opus (medium) so that review
  holds up. Save on usage through fewer wakes and a small context, not a cheaper coordinator model.
- Show David a short table: session, items, model/effort, wave, depends on, files written, worktree or main
  checkout. Under it, list David's own items. Get one OK, then go.

## 2. Start sessions
- Start each from this session (so reports come back here), `use_worktree: true` unless the check in step 1 says
  otherwise, `context: "fresh"`, with a self-contained brief:
  - what to read first, with line ranges for big files, and what not to read (reading is most of a session's cost)
  - the task and what done looks like
  - **the files it may write:** "if the task needs any other file, stop and report". This is what keeps two
    writers off the same file.
  - how to check the work: how to run the tests in a worktree (e.g. `PYTHONPATH=$PWD/src` when the editable
    install points elsewhere), or, where there are no tests, a named check (e.g. "search the source for each
    quoted line and report the count that match")
  - "commit on your branch, don't push, don't publish; report the commit"
  - the shared notes folder for long output
  - **the report:** "at most eight lines: commit, files changed, the check and its result, open questions"
  - **when to report:** "End your turn only when you're done, blocked, or need a decision. Don't end a turn to
    report progress. While a background job runs, wait for it instead of ending your turn with a status line."
  - **a budget for expensive work** (model calls, paid API calls, long test runs): how many in total, how many at
    once (default: at most 2), and "say what each run is meant to show before starting it; stop and ask before
    going over the budget".
- **Design-first sessions** (new behaviour, schemas, storage, UX) write a short design note into the notes folder,
  list open questions, and stop. Before David sees it, review it against a checklist of the cases it must cover,
  and raise any gaps. Use the item list's checklist if it has one. For software: concurrency, permissions, stale
  data after a rebuild, defaults, offline/fallback, room in the schema for later items. For documents and records:
  every claim cites its source, nothing sensitive lands in a tracked or shared file, drafts are marked as drafts.
- Starts only work on David's own message; on a turn triggered by a session report, propose a card instead.

## 3. Track and relay
- **A progress-only note gets no reply:** no tool calls and no summary, at most one line ("B still running").
  Act only on notes that finish an item, ask a question or report a failure.
- Read reports in short pages (the 400-char note is usually enough). Don't read transcripts or `list_events` unless
  the note is unclear, and never paste them.
- **When David talks to a session directly, step back from it.** Don't relay or summarise its notes; act only when
  it asks for a merge or your input, or David asks you to.
- Relay David's decisions to a session with SendMessage, quoting his words.
- **Routine go-aheads aren't decisions.** Committing a tested item, merging it, and starting the next planned
  session: do them and report. Ask David only about real choices between options or new behaviour he hasn't approved.
  Give a recommendation with each question. Where the repo's rules say commits need David's word, his OK on the
  plan table is that word for branch commits and local merges, and for nothing else.
- Status updates: one table (session · item · state · what's waiting on David), then decisions, then what's next.
  Keep them short. Link the session's notes file instead of retelling it.

## 4. Merge
In your own worktree: `git fetch`, merge the session branch, and run the full test suite. Where there is no suite,
run the check named in the brief yourself: the session's report is not proof. Then fast-forward the main checkout
**only if it's clean**. Update the project's HANDOFF to show the item as merged. Before merging, read the diff stat
and the riskier parts of the diff, not the whole diff.

**Push only where the repo's rules or David's plan OK allow it.** If they do: check the push account
(`gh auth status`), then `git push origin HEAD:main`. If they don't, stop at the local merge and list the push as
waiting on David.

## 5. Publishing and outward actions
Republish artifacts, send messages or post only when David says so. For an artifact: `read` it first, rebuild
from main, publish to the same url with no icon, and log the version in the HANDOFF.

## 6. Hand over
At ~150k context (about 80k above where you started), or when David pauses the fleet, write `coordinator-N-handover.md` in the notes folder with:
- the state (main hash, what's merged, what's open or on hold)
- David's decisions this round
- the checklists still to apply
- how merges are done.

Treat 150k as a soft trigger: hand over at the next phase boundary rather than mid-merge, and skip it when fewer
than ~20 of your calls of work remain, since a handover costs about as much as 20 calls save.

Mark paused items in the project's HANDOFF and withdraw their cards. The next coordinator starts by reading that note. Write it for that reader: "the next coordinator" is the chat
David opens and points at the note, which coordinates from there itself and starts no coordinator session.
