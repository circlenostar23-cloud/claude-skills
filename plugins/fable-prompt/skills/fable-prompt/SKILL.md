---
name: fable-prompt
description: Build a paste-ready prompt for a Claude Fable session, plus a facts-only context pack, so Fable spends limited usage on judgment instead of exploration. It clarifies the goal, scouts the projects on the current cheaper model, writes the pack, and drafts the prompt from a Fable-tuned template with a reading budget, named permissions and one deliverable. Use when David says "fable prompt", "prompt for fable", "set up a fable run", "use my fable usage on X", or wants a high-capability model to review, audit, plan or research a project or goal in any repo.
---

# Build a Fable prompt

You prepare a run for **Claude Fable** (`claude-fable-5-2` or later). You don't run it. You do the cheap work on the current model so the expensive model spends its usage on judgment:

1. Clarify the goal.
2. Scout the projects.
3. Write a **context pack** of facts only.
4. Draft the **prompt**.
5. Give run instructions.

David's Fable usage is limited, often a promo allowance. Every token Fable spends finding files, reading archives or starting subagents is a token it doesn't spend thinking about the goal.

## What drives Fable cost, and what makes it work well

These facts were checked against the `claude-api` skill on 2026-11-13. If that skill is available and a newer Fable model exists, re-check its "Migrating to Claude Fable" section before you rely on them.

- **Price.** Fable costs about twice as much per token as Opus 5.5 ($8 / $40 per million input/output tokens against $4 / $20). Thinking is always on, and its turns can run for many minutes.
- **Effort.** Start at **High**. Most of the gain arrives by High, and gains above it are uneven while costing many more tokens. Use xhigh only for the hardest long agentic coding where a gain has been measured. Never use max for a review. Effort barely changes reply length, so set length in the prompt.
- **Lines telling it to think less don't work** at medium and above. Lower the effort instead.
- **Overly prescriptive prompts make it worse.** Give the goal, what "good" means, and the constraints. Don't give step-by-step procedures.
- **It delegates readily when invited.** Subagents can be a large share of a session's cost. Say "don't start subagents" unless the task needs parallel work.
- **It applies approval rules literally.** Name what's allowed and what isn't. A vague caution like "be careful with X" makes it hold back routine work.
- **Caution piles up.** Rules, memory and handoff notes carried into context add up, and it follows them closely. For a read-only run, say "read-only" once and list the forbidden actions. Don't stack warnings.
- **It may stop early on long tasks** at low or medium effort. Add the finishing text (below) only for agentic build work at those levels. A review at High doesn't need it.
- **Reports can come out dense.** Always add the clear-communication paragraph to the deliverable section.

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
- **Who carries it out:** will agents execute the result, for example through the `coordinate-sessions` skill? If so, which models will be available then? Assume Sonnet and Opus, not Fable, unless David says otherwise: his Fable access is often gone by the time the plan is executed.
- **Off-limits:** private data, archives, compensation, anything the repos' `AGENTS.md` / `CLAUDE.md` protect.

## Step 2: Scout cheaply

Stay on the current model. Keep it to a handful of shell calls that measure; don't read file contents. Find:

- **Size and shape:** file counts, and the largest text files with their sizes (`find … -type f`, `wc -c`, `du`). Any file over about 50 KB gets a "read by section" instruction. Note any helper that prints a table of contents.
- **Archives and bulk folders to skip:** exports, extracted text, media, vendored code, `.zip` files, `node_modules`, data dumps.
- **Ground truth for the goal:** the files that record *outcomes*, not just activity. Examples: an applications tracker with results, an incident log, test results, analytics, a changelog. Pull the actual numbers. A finding backed by outcomes beats generic advice, and this is the most valuable part of the pack.
- **Where effort goes:** sort `git log --since=<about 3 months> --format=%s` into rough keyword groups, and count rows in the main logs or trackers. A mismatch between where the work goes and where the outcomes come from is often the headline finding.
- **Setup map:** rule files (`AGENTS.md`, `CLAUDE.md`), skills and agents directories, handoff or TODO files at the root. When there are several projects, diff their skill lists to see what one has that another lacks.
- **Sample candidates:** 2 to 3 items with good outcomes and 2 to 3 with bad ones, for Fable to read closely. Check that each path exists.
- **Git state:** the current branch and `git status --short` in each repo, so Fable knows which uncommitted or untracked files were already there before its run.
- **Execution facts** (only when agents will carry out the result). These decide how sessions can be started, and Fable shouldn't spend usage finding them:
  - which of the working files are git-ignored (`git check-ignore -v <paths>`, and read `.gitignore`), since a worktree won't contain them
  - whether there is a test command
  - what the agent docs say about commits, pushes, and scripts that reach outside services

Respect the evidence and privacy rules in the projects' instruction files while you scout.

## Step 3: Write the context pack

Write it to a **durable path that Fable's session can read**, normally `docs/<TOPIC>-CONTEXT-PACK-<YYYY-MM>.md` in the workspace Fable will open. Don't use the scratchpad: Fable's session can't see it, and a reboot can clear it. Leave the pack uncommitted unless David asks, and say it can be deleted after the run.

Rules for the pack:

- **Facts only.** No findings or recommendations. If you add interpretation, Fable sees the project through your framing, and that defeats the point of using a stronger model. Say at the top that counts come from text matching and should be checked against the source.
- **Sections:**
  1. Outcomes, with numbers and short quotes from the source
  2. Where the effort goes (a table)
  3. Setup map: rules, skills, handoff files, the section headings of the large files, a one-line git state per repo (branch, count of uncommitted or untracked paths), and the execution facts if you gathered them
  4. Suggested sample paths, all checked
- **Short.** Aim for 2 to 5 KB. It replaces exploration; it is not a summary of everything.
- Leave out secrets, compensation and anything the repos mark private.

## Step 4: Draft the prompt

Fill in the template below. Keep it short, around 400 to 700 words, or up to about 850 with the work-items block. Write it in plain words and give the goal, not procedures. Show it in full in your closing message inside a fenced `markdown` block, after `wrap_up` if the app uses it.

```markdown
# Goal

<One paragraph: which projects (paths), what they exist to achieve, what you want from this run.>

<Define the key term of the run, e.g. what "structural" or "risk" means here, and what's out of scope.>

# Start here

Read `<context pack path>` first. It has <one line on what it contains>. Check a number against its source before you build a finding on it. The pack collects facts and doesn't judge, so form your own view.

Start from <the ground-truth data>: <what to look at>. Then work backward to find where <the system> falls short of the goal. A finding backed by <outcome data> beats one based on general advice.

After the pack, read <orientation files>, then <what else matters>. <If there are several projects: compare them, and note where one has solved something the other hasn't.>

# Reading budget

I'm on a limited usage allowance, so read selectively:

- <Large files>: don't read them whole. Use <toc helper / headings / grep>, then read only the sections you need.
- Skip <archives and bulk folders, listed by name>.
- Sample <items>. Start with the ones the pack suggests, and add others only where a finding needs them.
- Don't start subagents<, and don't search the web>.

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
Also write a work-items file to `<same path>-work-items.md` for a coordinator running my `coordinate-sessions` skill, and put a three-line pointer to it near the top of the report. Keep model routing out of the report itself. The coordinator reads only that file, so it must stand alone. Assume <the models available for execution, normally Sonnet and Opus, not Fable>. It needs:
- Where this repo differs from a code repo with tests: ignored files a worktree won't have, no test suite, limits on commits, pushes or scripts.
- The rules that go in every session's brief.
- My own items (decisions, anything done by hand), each with what it blocks.
- A table of sessions: items, model and effort, wave, depends on, worktree or main checkout. Use as few sessions as the work allows. An edit of a few lines is not a session.
- For each session: what to read first with line ranges, the task, the files it may write, what done looks like, a check the coordinator can run, and a budget.
Route by input size and stakes: the strongest available model for short, high-stakes drafting, and the cheapest reliable one for mechanical work over large inputs.

Write for a reader who hasn't seen your tool calls or the files you opened. Put the key points first, use plain words and full sentences, and don't use labels you made up during the work.
```

**Why a separate work-items file.** `coordinate-sessions` starts by reading an item list and follows any model table in it. A separate file gives it that directly, and the coordinator never loads the full report. A model table at the top of the report pushes the findings down and is the wrong shape for the coordinator.

**Build runs at low or medium effort only.** Add this under a `# Finishing work` heading:

> Please avoid stopping while you still owe work the user asked for. Carry on with work that doesn't depend on the user's answer. When you meet ordinary obstacles like errors, timeouts or failing tools, diagnose them and work through them rather than stopping. Leave deliberate blockers alone, such as files marked not to be touched or withheld access, and say plainly what you found. This doesn't override the need for confirmation on risky or destructive actions.

## Step 5: Run instructions for David

Close with these, adapted to the run:

- Start a **fresh session** whose working folder includes every project in scope. This is often the parent workspace, so that all the projects and their rule files load.
- Choose **Fable** in the model picker, with effort set to **High**.
- Check usage about 10 minutes in. If it's burning fast, stopping costs less than letting it finish.
- Make follow-ups specific, such as "expand finding 3". A bare "continue" makes it re-plan.
- You can't see David's Fable quota, so don't estimate how much of it the run will use.
- **If Fable access is ending soon,** ask Fable in the same session to draft the one piece of the plan that most needs it, usually the short, high-stakes writing. Its context is already loaded, so that costs mostly the writing. Then have it update the work-items file so no session redoes the draft, and mark in the report which findings now have a draft.
- After the run, offer to delete the context pack. Fable's report is uncommitted too: commit or move it if David keeps it, delete it if not.

## Don't

- Don't run the Fable session yourself, or switch this session to Fable.
- Don't put findings in the pack.
- Don't paste large file contents into the prompt. Point to paths.
- Don't tell Fable to "think less" or "be brief in reasoning". Use effort for that.
- Don't add stacked cautions. Name the forbidden actions once.
- Don't ask for a model table inside the report. Routing goes in the work-items file.
