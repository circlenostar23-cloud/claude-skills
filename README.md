# claude-skills

David's Claude Code plugin marketplace (`david-skills`). Plugins here work in any repo, local or cloud.

| Plugin | What it does |
|---|---|
| `coordinate-sessions` | Run a list of work items as a fleet of side sessions from one coordinator session (`/coordinate-sessions`). |
| `model-prompt` | Build a paste-ready prompt for a stronger model (Fable, or Opus when preparing on Sonnet) and a facts-only context pack for any project and goal (`/model-prompt`). |

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

### Don't enable these plugins in a repo's `.claude/settings.json`

Repo settings only matter for cloud sessions, which clone just the repo. Neither plugin is useful there:
`coordinate-sessions` starts side sessions from the desktop app, and `model-prompt` scouts across local projects.
Repo settings also create a separate project-scope install for every folder and worktree. Each one is pinned
to the version current at the time and goes stale on the next release.

## Add a skill

Add `plugins/<name>/.claude-plugin/plugin.json` and `plugins/<name>/skills/<name>/SKILL.md`, list the plugin in
`.claude-plugin/marketplace.json`, and bump `version` when you change a plugin.
