# claude-skills

David's Claude Code plugin marketplace (`david-skills`). Plugins here work in any repo, local or cloud.

| Plugin | What it does |
|---|---|
| `coordinate-sessions` | Run a list of work items as a fleet of side sessions from one coordinator session (`/coordinate-sessions`). Its context-check hook tells every session its real context size: coordinators at 150k (hand over), others at 200k (suggest a fresh session). |
| `model-prompt` | Build a paste-ready prompt for a stronger model (Fable, or Opus when preparing on Sonnet) and a facts-only context pack for any project and goal (`/model-prompt`). |
| `global-rules` | David's global rules, in [RULES.md](plugins/global-rules/RULES.md). On the Mac, `~/.claude/CLAUDE.md` is a symlink to that file and loads natively. In cloud sessions, which can't see it, a startup hook prints it (only when `CLAUDE_CODE_REMOTE=true`). Edit RULES.md, then commit and push so cloud sessions get the change. |

## Install (user scope)

Add to `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "david-skills": { "source": { "source": "github", "repo": "circlenostar23-cloud/claude-skills" } }
  },
  "enabledPlugins": {
    "coordinate-sessions@david-skills": true,
    "model-prompt@david-skills": true
  }
}
```

This turns the plugins on for every local project and worktree. After a release, run
`claude plugin marketplace update david-skills` and then `claude plugin update <plugin>@david-skills`.

### `global-rules` is the one plugin enabled in each repo

Every repo under `personal_dev` (except Gabriel's) enables `global-rules` in its `.claude/settings.json`, because
cloud sessions see only repo settings. A new repo should get the same two entries:

```json
{
  "extraKnownMarketplaces": {
    "david-skills": { "source": { "source": "github", "repo": "circlenostar23-cloud/claude-skills" } }
  },
  "enabledPlugins": { "global-rules@david-skills": true }
}
```

On the Mac its hook does nothing, so a stale project-scope copy there is harmless.

### Don't enable the other plugins in a repo's `.claude/settings.json`

Repo settings only matter for cloud sessions, which clone just the repo. Neither of the other plugins is useful there:
`coordinate-sessions` starts side sessions from the desktop app, and `model-prompt` scouts across local projects.
Repo settings also create a separate project-scope install for every folder and worktree. Each one is pinned
to the version current at the time and goes stale on the next release.

## Add a skill

Add `plugins/<name>/.claude-plugin/plugin.json` and `plugins/<name>/skills/<name>/SKILL.md`, list the plugin in
`.claude-plugin/marketplace.json`, and bump `version` when you change a plugin.
