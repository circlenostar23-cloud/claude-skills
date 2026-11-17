# Target: Claude Opus

Use this file when the prompt is for **Claude Opus** (`claude-opus-5-5` or later), prepared on Sonnet.

The economics differ from a Fable run. Opus costs twice what Sonnet does, not four times, and it isn't on a scarce allowance. So the prep is a larger share of the total, and the pack was written by a model further below the reader. Both push the same way: a thinner pack, and more checking by Opus.

## What drives Opus cost, and what makes it work well

These facts were checked against the `claude-api` skill on 2026-11-17 ("Migrating to Claude Opus 5.5" and the prompt-audit reference). That skill says little about prompting Opus 5.5 itself and tells you to re-test what it carries over from Opus 5, so each line says which it is. Re-check when a newer Opus exists.

- **Price** (Opus 5.5). $4 / $20 per million input/output tokens, against $2 / $10 for Sonnet 5.5. Thinking is always on.
- **Effort** (Opus 5.5). Start at **medium** and test the levels next to it. Use xhigh and max only where a gain has been measured.
- **Reply length** (carried over from Opus 5). Effort isn't the lever for length. Set length in the prompt.
- **Thinking less** (Opus 5.5). Lower the effort before adding a line that asks for less thinking. Lowering effort is the more reliable of the two.
- **Procedures** (general guidance for current models). State outcomes, constraints and how to verify. Keep numbered steps only where the order truly matters.
- **Subagents** (carried over from Opus 5). It reaches for them freely, which multiplies cost. Tell it to delegate rarely, and give a cap on how many it may start.
- **Emphasis** (general guidance). Capitals and repeated warnings make a model cautious and hedging. State each limit once in plain words.
- **Reports** (Opus 5.5). Its closing reports are clearer by default than earlier models'. The clear-communication paragraph at the end of the deliverable section is optional: cut it first if the prompt is over length.
- **Don't ask it to write out its reasoning** (Opus 5.5). That request can be declined. Asking for a short explanation of a finding, or how confident it is, is fine.
- **Don't add "double-check your answer" lines** (carried over from Opus 5). They cause over-verification. Name the check that must pass instead.
- **Progress notes** (Opus 5.5). If David wants updates during a long run, say when and what they should contain. Don't add "don't narrate" or "hold all findings" lines.
- **Not covered for Opus 5.5:** whether it applies approval rules as literally as Fable, and whether carried-over cautions pile up. Naming the allowed and forbidden actions once costs nothing either way, so keep that part of the template as it is.

## Settings for the shared steps

The thresholds and effort choices below are starting points from judgment, not measurements. Change them when a run shows they're off.

- **When to skip the skill:** skip when all three hold: one repo is in scope, its tracked files total under 200 KB (`git ls-files -z | xargs -0 wc -c | tail -1`, leaving out any single tracked data or log file over 1 MB, which the target would skip anyway), and no agents will carry out the result. Don't skip if the goal depends on git-ignored working data, such as a `data/` folder: the tracked size doesn't measure that. Opus reads that much for well under the cost of the prep. Give David a direct prompt of a few lines (goal, what's allowed, the deliverable) and stop.
- **Reading budget opener:** "Read what you need to be sure of a finding. These limits are about not wasting effort, not about reading less than the work needs:"
- **How far to trust the pack:** treat it as a map. Add this line to "Start here" in place of the sentence "Check a number against its source before you build a finding on it.": "A cheaper model wrote the pack, so confirm any number or path in it against the source before you rely on it, and tell me in the report if the pack was wrong."
- **Subagents:** for a run on one or two repos, "Don't start subagents." For an audit across several repos, "Start at most two subagents, and only for reading that would otherwise fill your context."
- **Effort:** medium for a review or research run with a bounded scope. High for a plan or audit across repos. High also for any run that writes the work-items file, even on one repo.
- **Finishing text:** for build runs at medium, don't use the long paragraph in Step 4, which was written for Fable. Add this one line to the deliverable section instead: "Finish the whole task, not just the easy part of it, and report completion only when it's fully done."
- **Executors to assume in the work-items block:** Sonnet and Haiku. Opus only for short, high-stakes drafting, unless David says otherwise.

## Notes for the model preparing the pack

You're probably Sonnet at medium effort. Two things about that, from the same `claude-api` check:

- You follow "minimize tool calls" lines literally. Step 2 doesn't cap the number of shell calls on purpose. Run every measurement it lists.
- Step 5 matters more here than on a Fable run prepared by Opus. Don't skip a check because the draft looks fine.

## Run instructions to add

- Choose **Opus** in the model picker, with the effort from "Settings" above for this kind of run.
- If a run at medium comes back thin on evidence, re-run the same prompt at high before rewriting the prompt. If it was already at high, rewrite the prompt rather than going to xhigh or max.
