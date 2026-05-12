# Preferences — Cold Memory

Recurring patterns, style choices, and workflow preferences observed over time.

<!-- promoted 2026-04-28 -->
## Authorization tokens (compact)
Dina uses short, single-word/phrase tokens that are full authorizations, not check-ins:
- `yes` → execute the proposed step now, no further confirmation
- `you` (in "you do X" / "you run X") → run the system-level command without re-asking, even if it touches Task Scheduler / git / files
- `go ahead`, `ok` → full commit on the proposal under discussion, NOT "ask one more clarifying question"
- `do it` → stop explaining and execute (already in CLAUDE.md communication.md, reinforced 04-27)
- `Naw let just ship as is` / `ok let see the new content` → terminate iteration cleanly; want an explicit checkpoint before pushing substantive PR edits

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

<!-- promoted 2026-05-09 -->
## Code review discipline (external repos)
- **Don't speculate on what reviewers mean** — if a comment is ambiguous (e.g. "a detail about how we show the event"), tag the reviewer to ask rather than projecting intent.
- **Vercel preview blockers from contributor commit-email mismatches** aren't reviewer-actionable — that's an access-grant problem (Helen's domain), not the PR author's commit to fix. Don't lead with procedural blockers contributors can't resolve.
- **Pressure-test recommendations before posting.** Steelman alternative architectures and offer options (B vs C) rather than dictating one. Especially important in collaborative repos with non-developer contributors.
- **Run advisor pass on every external-repo review** — catches wrong flags before they go public (retracted M1 hydration, downgraded H3 on PR #598).

<!-- promoted 2026-05-11 -->
## PR scope + docs discipline (Dina's lean-PR culture)
- WDAI PRs should be lean: typical 1–5 files. Real test isn't lines but **"how many separable concerns surface"** — bundled architectural artifacts inflate cognitive load even when net code is small.
- When a plan/doc is superseded by working code, **delete it in the same commit** — don't leave 968-line artifacts that survived 4 pivots.
- Prefer **in-PR setup detail over linked docs** when the linked doc is mostly standard ops repetition. Keep PRs self-contained for things specifically introduced by that PR.
- Wants an **explicit checkpoint before pushing substantive PR edits** — confirm new content before rewrite.
