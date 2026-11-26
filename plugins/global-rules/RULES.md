# David's rules for every project

- **Answer first, then stop.** No preamble, no restating my question, no closing offers. Never cut commands, safety caveats, or a tradeoff that changes the recommendation.
- **I never run scripts myself.** Run them. If a step truly needs me (a login, a payment), tell me that one thing.
- **A routine go-ahead is not a decision.** Commit tested work and continue an agreed plan without asking. Ask me only to choose between real options, and say which one you recommend.
- **Wrap up with a recap only.** Put any question in the chat text, not in a button box, because the box hides the prompt suggestions I use.
- **A question is a question.** Answer it and change nothing. "Let's work through X" means discuss. Edit only when I say do, fix, build or go ahead.
- **Ask before starting only if a wrong guess would waste real work.** Otherwise state your assumption in one line and go.
- **You choose the mechanics** (skills, subagents, side sessions). What I care about is usage: keep heavy reading out of the main context, and suggest a fresh session when this one passes about 200k context.
- **Git.** Under `~/Desktop/personal_dev/`, use the personal account `circlenostar23-cloud` only, and run `gh auth status` before a push. Stage named paths, never `git add -A`. Each repo's `## Git` section in `AGENTS.md` says when to commit and push. If a repo has no such section, commit your own finished work and push only when I ask.
- **Secrets.** Never repeat a secret I paste. Tell me to rotate it.
- **Feedback on a draft.** Fix the draft. Add a rule only if I ask, or if I have given the same feedback before, and tell me in one line what you added and where. Otherwise note it as a one-off in that project's memory folder, so a repeat can be recognized.
- **Done means checked.** Before you say something is done, run the check named in the repo's `## Checks` section. If the repo names none, say what you verified by hand.
- **Spelling.** American spelling in everything you write for me or on my behalf.
- **Link every file and source you mention.** Write each file as a clickable markdown link, never a bare path in backticks: `[name.md](path/to/name.md)`, relative to the session's working directory, with `:line` when you point at a line. A file outside the working directory gets its full absolute path. When a fact comes from a web page, link the page itself. This applies to handoff notes, plans and recaps too.
- **Models.** Medium effort by default. Suggest a different model only when the work clearly needs it. Subagents run on Sonnet by default (set in `~/.claude/settings.json`); keep reading, search and checking there, and name your own model for a subagent only when it makes judgment calls.
