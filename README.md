# claude-skills

David's Claude Code plugin marketplace (`david-skills`). Plugins here work in any repo, local or cloud.

| Plugin | What it does |
|---|---|
| `coordinate-sessions` | Run a list of work items as a fleet of side sessions from one coordinator session (`/coordinate-sessions`). |
| `fable-prompt` | Build a paste-ready Claude Fable prompt and a facts-only context pack for any project and goal (`/fable-prompt`). |

## Use it in a repo (works in cloud sessions)

Add to the repo's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "david-skills": { "source": { "source": "github", "repo": "circlenostar23-cloud/claude-skills" } }
  },
  "enabledPlugins": { "coordinate-sessions@david-skills": true }
}
```

The same two keys in `~/.claude/settings.json` enable it for every local project.

## Add a skill

Add `plugins/<name>/.claude-plugin/plugin.json` and `plugins/<name>/skills/<name>/SKILL.md`, list the plugin in
`.claude-plugin/marketplace.json`, and bump `version` when you change a plugin.
