#!/bin/sh
# Print David's global rules into cloud sessions only. On his Mac, ~/.claude/CLAUDE.md
# is a symlink to RULES.md and Claude Code loads it natively, so this stays silent there.
[ "$CLAUDE_CODE_REMOTE" = "true" ] || exit 0
printf '%s\n\n' "These are David's global rules, which apply in every project (the same file is ~/.claude/CLAUDE.md on his Mac):"
cat "${CLAUDE_PLUGIN_ROOT}/RULES.md"
