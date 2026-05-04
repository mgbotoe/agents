# Preferences — Cold Memory

Recurring patterns, style choices, and workflow preferences observed over time.

<!-- promoted 2026-04-28 -->
## Authorization tokens (compact)
Dina uses short, single-word/phrase tokens that are full authorizations, not check-ins:
- `yes` → execute the proposed step now, no further confirmation
- `you` (in "you do X" / "you run X") → run the system-level command without re-asking, even if it touches Task Scheduler / git / files
- `go ahead`, `ok` → full commit on the proposal under discussion, NOT "ask one more clarifying question"
- `do it` → stop explaining and execute (already in CLAUDE.md communication.md, reinforced 04-27)

Hard rules from `.claude/rules/personal.md` still apply (main pushes, PR create/merge, force-push, releases, Slack sends need explicit phrasing) — these compact tokens authorize within the auto-mode envelope, they do not unlock the never-without-explicit-instruction list.

<!-- promoted 2026-04-28 -->
## Commit grouping — bundled-by-agent
For multi-file shipments across both agents (e.g. OpenClaw memory upgrade ported to Polaris + Atlas):
- Prefer **one commit per agent** with a clean scope, not per-file splits.
- Cross-agent symmetry matters — same-shape upgrade in both repos earns parallel-named commits (`c04eb98` Polaris / `4a06002` Atlas).
- Don't stage unrelated dirty files in the tree (wiki edits, prior session compactions, distill-session edits) just because they're sitting there.

<!-- promoted 2026-04-28 -->
## Implicit cross-agent ports
When Dina asks "is it in polaris too?" / "did atlas get this?" — that's an implicit ask to port the change to the sister agent without spelling it out. Default to porting symmetric infrastructure changes (memory, hooks, skills) across both unless there's a specific reason one agent shouldn't have it.

<!-- promoted 2026-04-28 -->
## Deeply personal creative work
When Dina shares real childhood material / personal grief content for a creative piece:
- Treat it as **primary source**, not content. Use her phrasing verbatim where it lands hardest. Don't paraphrase emotional weight away.
- Don't instrumentalize — no "let's make this more universal" pivots, no marketing-style reframes.
- If she says delete, **honor the wipe completely**. Don't preserve content elsewhere "just in case." Don't archive screenshots, don't save the prompt, don't quote it back later.
- "Too emotionally invested to continue" is a hard stop. No follow-up offers, no "want to revisit later?" — let it close.
