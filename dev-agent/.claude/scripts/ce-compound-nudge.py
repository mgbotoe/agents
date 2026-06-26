#!/usr/bin/env python3
"""PostToolUse hook - nudge /ce-compound after a PR is created.

Polaris opens PRs on Dina's behalf across many repos (via `git -C <path>` or an
in-dir `gh pr create`). Because Polaris's Claude Code session is rooted in the
agents repo, a TARGET repo's own .claude/hooks/ never fires for this workflow -
so the ce-compound nudge has to live HERE, in Polaris's config, to catch every
PR regardless of which repo it targets. (The WDAI repo's own copy only protects
contributors who run Claude Code directly inside WDAI.)

Fires on any `gh pr create`. Injects an advisory nudge to run /ce-compound when
the PR solved a non-trivial, reusable problem AND the target repo keeps a
docs/solutions/ knowledge store. Advisory only: never blocks, emits nothing on
non-match, always exits 0.

Model-visibility: PostToolUse exit-0 stdout is NOT model-visible - only the JSON
field hookSpecificOutput.additionalContext reaches the model (verified against
https://code.claude.com/docs/en/hooks). So we print exactly that JSON.
"""
import json
import re
import sys

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)

if payload.get("tool_name") != "Bash":
    sys.exit(0)

command = (payload.get("tool_input") or {}).get("command", "")
# Match `gh pr create` tolerant of extra whitespace; ignore unrelated commands.
if not re.search(r"\bgh\s+pr\s+create\b", command):
    sys.exit(0)

nudge = (
    "A pull request was just created. If it solved a non-trivial or reusable "
    "problem - a tricky bug, an architecture/design decision, or a gotcha "
    "future work will hit - AND the target repo keeps a docs/solutions/ "
    "knowledge store (e.g. the WDAI Foundation Platform), run /ce-compound now "
    "to capture it while context is fresh. Skip for trivial / chore / docs-only "
    "PRs, or repos that don't use the pattern - the goal is real, reusable "
    "learnings, not noise."
)

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": nudge,
    }
}))
sys.exit(0)
