---
name: fable-prompt
description: Build a paste-ready prompt for a stronger Claude model, plus a facts-only context pack, so the stronger model spends its usage on judgment instead of exploration. Two targets - Claude Fable (prepared on Opus or Sonnet) and Claude Opus (prepared on Sonnet). It clarifies the goal, scouts the projects on the current cheaper model, writes the pack, drafts the prompt from a template with a reading budget, named permissions and one deliverable, and checks both before handing over. Use when David says "fable prompt", "prompt for fable", "set up a fable run", "use my fable usage on X", "opus prompt", "prompt for opus", "set up an opus run", or wants a higher-capability model to review, audit, plan or research a project or goal in any repo.
---

# Build a prompt for a stronger model

You prepare a run for a stronger model than the one you're on. You don't run it. You do the cheap work on the current model so the expensive model spends its usage on judgment:

1. Pick the target and clarify the goal.
2. Scout the projects.
3. Write a **context pack** of facts only.
4. Draft the **prompt**.
5. Check the pack and the prompt.
6. Give run instructions.

## Pick the target

| Target | When | Read |
|---|---|---|
| **Fable** | David names Fable, or wants the strongest model. This is the default. | `targets/fable.md` |
| **Opus** | David names Opus, or you're on Sonnet and Fable isn't available. | `targets/opus.md` |

The target file sits next to this one. Read it before Step 1. It holds what's true of that model (price, effort, how it reads a prompt) and the settings the steps below refer to as "the target file": when to skip the skill, the reading-budget opener, the subagent line, when to add the finishing text, the executors to assume, and the extra run instructions.

## Step 1: Clarify

Get these from the conversation first. Ask only for what's missing, in one `AskUserQuestion` call at most:

- **Goal:** the outcome David wants, such as "more interviews" or "fewer production incidents", not just "review the repo".
- **Scope:** which folders or repos are in scope, and who the work is for.
- **Kind of run:**
  - *Review or audit*: read-only, ends in a report. This is the default.
  - *Plan*: read-only, ends in a plan file.
  - *Build*: edits allowed. Needs explicit permissions and a branch.
  - *Research*: web allowed.
- **Deliverable:** where the output file goes, and whether a chat summary is wanted.
- **Decisions already made:** choices David has settled and options he has rejected, with the reason if he gave one. A stronger model that doesn't know them will recommend them again.
- **Who carries it out:** will agents execute the result, for example through the `coordinate-sessions` skill? If so, which models will be available then? Use the target file's assumption unless David says otherwise.
- **Off-limits:** private data, archives, compensation, anything the repos' `AGENTS.md` / `CLAUDE.md` protect.

## Step 2: Scout cheaply

Stay on the current model. Use shell calls that measure. Read file contents only where a bullet below says to: the outcome files, and the first lines of plan and decision files.

Keep the scout mechanical, so the pack carries no view of yours. Every number you record keeps the command or path that produced it. Where a bullet asks you to choose items, choose by the stated rule, not by what looks interesting.

Find:

- **Size and shape:** file counts, and the largest text files with their sizes (`find … -type f`, `wc -c`, `du`). Any file over about 50 KB gets a "read by section" instruction. Note any helper that prints a table of contents.
- **Archives and bulk folders to skip:** exports, extracted text, media, vendored code, `.zip` files, `node_modules`, data dumps.
- **Ground truth for the goal:** the files that record *outcomes*, not just activity. Examples: an applications tracker with results, an incident log, test results, analytics, a changelog. Read these and pull the actual numbers. This is the most valuable part of the pack.
- **Where effort goes:** count `git log --since=<about 3 months> --format=%s` subjects by keyword, and count rows in the main logs or trackers. Record the keywords you used next to the counts. Report the counts and nothing else: whether they line up with the outcomes is for the stronger model to judge.
- **Setup map:** rule files (`AGENTS.md`, `CLAUDE.md`), skills and agents directories, handoff or TODO files at the root. When there are several projects, diff their skill lists to see what one has that another lacks.
- **Open plans:** every handoff, work-items, plan and review file in the projects in scope that isn't marked done, with its date and whether work on it has started (`git log -1 --format=%cs -- <file>`, and a look at its first lines). Include a run-order file in the parent workspace's `docs/` if there is one. Reviews written days apart otherwise plan changes to the same files without knowing about each other.
- **Recorded decisions:** any file or section that records David's decisions on those plans (`grep -il "decision" docs/ *.md`, and `git log --format=%s | grep -i decision`). Note the path and heading. Don't restate them from memory.
- **Sample candidates:** the 3 most recent items with a good outcome and the 3 most recent with a bad one, by the date in the outcome file. Check that each path exists. If the outcome file has no good/bad field, list the 6 most recent items and say so.
- **Git state:** the current branch and `git status --short` in each repo, so the stronger model knows which uncommitted or untracked files were already there before its run.
- **Execution facts** (only when agents will carry out the result). These decide how sessions can be started, and the stronger model shouldn't spend usage finding them:
  - which of the working files are git-ignored (`git check-ignore -v <paths>`, and read `.gitignore`), since a worktree won't contain them
  - whether there is a test command
  - what the agent docs say about commits, pushes, and scripts that reach outside services

Respect the evidence and privacy rules in the projects' instruction files while you scout.

**Then apply the target file's "when to skip the skill" check** to the sizes you measured. If it says to skip, tell David in two lines, give him a short direct prompt, and stop.

## Step 3: Write the context pack

Write it to a **durable path that the target session can read**, normally `docs/<TOPIC>-CONTEXT-PACK-<YYYY-MM>.md` in the workspace that session will open. Don't use the scratchpad: the other session can't see it, and a reboot can clear it. Leave the pack uncommitted unless David asks, and say it can be deleted after the run.

Rules for the pack:

- **Facts only.** No findings or recommendations. If you add interpretation, the stronger model sees the project through your framing, and that defeats the point of using it. Say at the top that counts come from text matching and should be checked against the source.
- **Every number has its source** beside it: the path, or the command that produced it.
- **Sections:**
  1. Outcomes, with numbers and short quotes from the source
  2. Where the effort goes (a table of counts, with the keywords used)
  3. Decisions already made: what David told you in Step 1 in his words, and the paths of any recorded decisions
  4. Setup map: rules, skills, handoff files, the open plans with their dates and state, the section headings of the large files, a one-line git state per repo (branch, count of uncommitted or untracked paths), and the execution facts if you gathered them
  5. Sample paths, all checked, with the rule that picked them
- **Short.** Aim for under 10 KB. It replaces exploration; it is not a summary of everything.
- Leave out secrets, compensation and anything the repos mark private.

## Step 4: Draft the prompt

Fill in the template below. Keep it short, around 400 to 700 words, or up to about 850 with the work-items block. Write it in plain words and give the goal, not procedures. Show it in full in your closing message inside a fenced `markdown` block, after `wrap_up` if the app uses it.

```markdown
# Goal

<One paragraph: which projects (paths), what they exist to achieve, what you want from this run.>

<Define the key term of the run, e.g. what "structural" or "risk" means here, and what's out of scope.>

# Start here

Read `<context pack path>` first. It has <one line on what it contains>. Check a number against its source before you build a finding on it. The pack collects facts and doesn't judge, so form your own view.

The outcome data is in <the ground-truth files>. Findings tied to <that data> rank above findings based on general advice.

The pack lists decisions I've already made. Treat them as settled. If the evidence says one is wrong, say so once under Open questions, and don't plan around reversing it.

The orientation files are <rule files, handoffs>. <If there are several projects: note where one has solved something the other hasn't.>

# Reading budget

<Reading-budget opener from the target file>

- <Large files>: don't read them whole. Use <toc helper / headings / grep>, then read only the sections you need.
- Skip <archives and bulk folders, listed by name>.
- Sample <items>. Start with the ones the pack lists, and add others only where a finding needs them.
- <Subagent line from the target file><, and don't search the web>.

# What you may do

<Review/plan:> You may read any file in scope and run read-only commands (<list>). Writing the deliverable below is the only file write allowed. Don't modify or delete existing files, commit, or run <scripts that call outside services, named>.
<Research: as review/plan, plus web search and fetching pages <on what topics or sites>. Don't sign in to sites, submit forms, or download files.>
<Build: list the allowed actions by name, the branch to work on, the actions that still need a go-ahead, and the test command that must pass.>

# Deliverable

Write <one report / plan> to `<durable path>`, then give me a short summary in chat. Aim for about <target length, e.g. 1,500 words>; any proposed rule or instruction text (`AGENTS.md`, `CLAUDE.md`, skills) should stay under <N> lines.

<Structure, e.g.:>
1. **Top findings, ranked by expected effect on <goal>.** For each: the problem, the evidence (paths, data), why it matters, the fix, and the rough effort. <N> findings are enough. Say how confident you are in each.
2. <Per-project or per-area section.>
3. **What's working:** things to keep, so a later cleanup doesn't break them.
4. **Open questions:** what you couldn't judge from the files.

<Only when agents will carry out the result:>
Also write a work-items file to `<same path>-work-items.md` for a coordinator running my `coordinate-sessions` skill, and put a three-line pointer to it near the top of the report. Keep model routing out of the report itself. The coordinator reads only that file, so it must stand alone. Assume <the executors from the target file, or what David said>. It needs:
- Where this repo differs from a code repo with tests: ignored files a worktree won't have, no test suite, limits on commits, pushes or scripts.
- The rules that go in every session's brief.
- My own items (decisions, anything done by hand), each with what it blocks.
- Overlaps with the open plans listed in the context pack: each file this work would write that another plan also writes, and which should go first.
- A table of sessions: items, model and effort, wave, depends on, worktree or main checkout. Use as few sessions as the work allows. An edit of a few lines is not a session.
- For each session: what to read first with line ranges, the task, the files it may write, what done looks like, and a check the coordinator can run.
Route by input size and stakes: the strongest available model for short, high-stakes drafting, and the cheapest reliable one for mechanical work over large inputs.

Write for a reader who hasn't seen your tool calls or the files you opened. Put the key points first, use plain words and full sentences, and don't use labels you made up during the work.
```

**Why a separate work-items file.** `coordinate-sessions` starts by reading an item list and follows any model table in it. A separate file gives it that directly, and the coordinator never loads the full report. A model table at the top of the report pushes the findings down and is the wrong shape for the coordinator.

**Finishing text.** Add this under a `# Finishing work` heading only when the target file says to:

> Please avoid stopping while you still owe work the user asked for. Carry on with work that doesn't depend on the user's answer. When you meet ordinary obstacles like errors, timeouts or failing tools, diagnose them and work through them rather than stopping. Leave deliberate blockers alone, such as files marked not to be touched or withheld access, and say plainly what you found. This doesn't override the need for confirmation on risky or destructive actions.

## Step 5: Check the pack and the prompt

Run these before you show anything. Fix what fails, then re-run that check.

1. **Paths exist.** `ls` every path named in the pack and the prompt.
2. **Numbers have sources.** Each number in the pack has a path or command beside it. Re-run two of the commands and compare.
3. **The pack doesn't judge.** `grep -inE "should|needs? to|problem|issue|weak|strong|better|worse|too (many|much|few|little)|recommend|suggest|unfortunately|clearly" <pack>`. Rewrite each hit as a plain fact or delete it. A hit inside a quote from a source file can stay.
4. **Pack size.** `wc -c <pack>` is under about 10,000.
5. **Prompt length.** Write the draft to the scratchpad and run `wc -w`. It's within the limit in Step 4.
6. **Forbidden actions appear once.** One list under "What you may do". No "be careful", no "IMPORTANT", no capitals for emphasis, no warning repeated in another section.
7. **No procedure.** Outside the deliverable structure, the prompt has no numbered steps and no "first… then…" ordering of the work.

## Step 6: Run instructions for David

Close with these, adapted to the run, followed by the target file's own run instructions:

- Start a **fresh session** whose working folder includes every project in scope. This is often the parent workspace, so that all the projects and their rule files load.
- Make follow-ups specific, such as "expand finding 3". A bare "continue" makes it re-plan.
- After the run, offer to delete the context pack. The report is uncommitted too: commit or move it if David keeps it, delete it if not.

## Don't

- Don't run the target session yourself, or switch this session to the target model.
- Don't put findings in the pack.
- Don't paste large file contents into the prompt. Point to paths.
- Don't tell the target to "think less" or "be brief in reasoning". Use effort for that.
- Don't add stacked cautions. Name the forbidden actions once.
- Don't ask for a model table inside the report. Routing goes in the work-items file.
