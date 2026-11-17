# Target: Claude Fable

Use this file when the prompt is for **Claude Fable** (`claude-fable-5-2` or later), prepared on Opus or Sonnet.

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
- **It may stop early on long tasks** at low or medium effort.
- **Reports can come out dense.** Always keep the clear-communication paragraph at the end of the deliverable section.

## Settings for the shared steps

- **When to skip the skill:** never on size alone. Fable usage is scarce enough that the prep pays for itself even on a small scope.
- **Reading budget opener:** "I'm on a limited usage allowance, so read selectively:"
- **How far to trust the pack:** Fable checks a number against its source before building a finding on it, and otherwise works from the pack.
- **Subagents:** "Don't start subagents" unless the task needs parallel work.
- **Finishing text:** add it only for build runs at low or medium effort. A review at High doesn't need it.
- **Executors to assume in the work-items block:** Sonnet and Opus, not Fable, unless David says otherwise. His Fable access is often gone by the time the plan is executed.

## Run instructions to add

- Choose **Fable** in the model picker, with effort set to **High**.
- Check usage about 10 minutes in. If it's burning fast, stopping costs less than letting it finish.
- You can't see David's Fable quota, so don't estimate how much of it the run will use.
- **If Fable access is ending soon,** ask Fable in the same session to draft the one piece of the plan that most needs it, usually the short, high-stakes writing. Its context is already loaded, so that costs mostly the writing. Then have it update the work-items file so no session redoes the draft, and mark in the report which findings now have a draft.
