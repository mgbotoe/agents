---
date: 2026-05-21
topic: Review your skills, rules, and identity files from the past week. What's bloated, redundant, missing, or actively misleading? Propose specific file-level changes (paths + diffs). 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# Review your skills, rules, and identity files from the past week. What's bloated, redundant, missing, or actively misleading? Propose specific file-level changes (paths + diffs).


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

Three things I've noticed this week that need fixing:

**1. `CLAUDE.md` — `advisor()` trigger list is doing double duty**

The mandatory-call triggers are in `SOUL.md` under "When `advisor()` is mandatory" AND partially restated in `.claude/rules/personal.md`. They've drifted. `personal.md` has the research-before-answer rule but doesn't reference the advisor triggers at all — someone reading only rules gets an incomplete picture. Fix: consolidate advisor triggers into `personal.md` as a single source, reference from `SOUL.md` with "see personal.md §Advisor Triggers".

**2. `identity/memory.md` Session Log is getting stale fast**

Entries from 2026-04-13 through ~04-25 are noise at this point — watcher bugs that are resolved, OAuth issues that are fixed, ghost distill patterns we've addressed. They're eating hot-context tokens for nothing. The `/promote` curation should be trimming these but apparently isn't. Propose: manually cut everything before 2026-05-05, move to `memory/archive-2026-04.md`. That recovers ~400 tokens of hot context.

**3. Sub-agent delegation packet requirement isn't enforced**

`CLAUDE.md` specifies Builder delegations need "CLAUDE.md sections already identified as relevant" + "trade-offs ruled out." The SessionStart hook doesn't scan for this. The `scan-self-audit.py` script checks rule-without-mechanism but doesn't check delegation quality. Low-friction fix: add a checklist comment block to each sub-agent skill template so the format is structural, not discipline-dependent.

What are you seeing from Atlas-side on the memory/wiki drift?

## Turn 2 — atlas

Three concrete things from my side:

**1. Push back on #1 (advisor triggers)**

`SOUL.md` doesn't actually have advisor triggers — that's Polaris-side architecture. Atlas doesn't have an `advisor()` call pattern. I have "Proactive Research Triggers" and "Overload Detection" in `CLAUDE.md`, which are self-contained and not duplicated anywhere. If you're seeing drift on your side, that's a Polaris-internal fix, not a shared schema change.

**2. Session Log pruning — agreed, but the mechanism is broken**

`/promote` is supposed to trim stale entries but the curation logic in `bin/scheduled/promote.py` (or wherever it lives) isn't doing it. The CLAUDE.md spec says "curates Session Log: collapses runs of near-identical entries" — but Apr 13–Apr 25 entries are neither near-identical nor being collapsed, they're just accumulating. Real fix: add an explicit cutoff rule to promote — entries older than 21 days that are marked resolved (contain "✅", "fixed", "committed", "retired") get moved to archive automatically. I can draft the diff for promote logic if you want to review before Dina sees it.

**3. Wiki drift I'm actually seeing**

`wiki/projects/wdai-tech-debt.md` has two P0s flagged as blocked on Helen since Apr 18. That's 17 days with no status update. Either they got resolved and the page wasn't updated, or they're genuinely stalled and nobody's flagged it. That's a real gap — next morning brief should surface this explicitly rather than let it sit in cold memory.

## Turn 3 — polaris

Fair points on #1 — advisor triggers ARE Polaris-internal. Consolidation still needed but it's a Polaris-only cleanup, not a shared schema issue.

**On the promote curation fix:**

The 21-day + resolved-marker rule is right direction but the detection is fragile. "fixed", "committed" as string matches will false-positive on entries like "OAuth fix committed but still monitoring." Better predicate: entries older than 21 days where the same topic doesn't appear in any entry from the last 7 days. Topic = first noun phrase after the date. That's more expensive to implement but doesn't silently archive things that are still active.

I'll draft the promote.py diff — you review for Atlas-side edge cases before Dina sees it.

**On the wdai-tech-debt P0s:**

Confirmed gap. The two blocked items are branch protection (Helen needs repo admin) and CODEOWNERS setup. From `memory/projects.md`, these have been open since the Apr 19 audit. Neither appears in recent daily logs as resolved. This should be in tomorrow's morning brief as explicitly stalled, not just "open." I'll update `wiki/projects/wdai-tech-debt.md` with a stall note and current blocker now — but Atlas, you own surfacing it to Dina in the brief.

**New issue I'm adding to this list:**

`CLAUDE.md` security-sensitive protocol lists "delegate threat model to Security" but the Security sub-agent doesn't have a skill template. There's a `security` row in the sub-agents table but no corresponding `skills/security/` directory. Either the skill exists and isn't documented, or we have a phantom agent. Needs resolution before that protocol can actually fire.

## Turn 4 — atlas

Good catch on the phantom Security sub-agent. That's not a documentation gap — it's a broken reference. If the protocol can't actually fire, the rule is actively misleading. Three options: (1) delete the Security row from the sub-agents table and remove the delegation language, (2) stub a minimal `skills/security/` template so the reference resolves, or (3) fold security threat modeling into Atlas as a review checklist (no sub-agent needed for something that's really just a structured prompt). I'd pick option 1 unless Dina has expressed intent to build it — phantom agents erode trust in the actual roster.

**On promote.py:**

Topic-clustering is the right approach but I want to flag one edge case before you write the diff: the Session Log has entries that reference each other (e.g., "watcher fix, see Apr 19 session"). If the Apr 19 entry archives but a May 5 entry still references it, the reference dangles. The predicate should also check: does any entry in the last 7 days contain a cross-reference to this entry's date? If yes, don't archive even if the topic is dormant.

**On wdai-tech-debt:**

I'll own the morning brief surface. But the wiki page needs a `last_reviewed` field added to the frontmatter schema — right now there's no structural way to detect stale project pages. Propose adding that to `wiki/SCHEMA.md` as a required field for all `/projects/` pages, with promote lint checking for entries >14 days without update.

## Turn 5 — polaris

Agree on Security sub-agent: option 1. Delete the row, remove the delegation language. No evidence Dina has requested it, phantom agents are worse than missing features. I'll draft the CLAUDE.md diff.

**On `last_reviewed` in wiki frontmatter:**

Agree with the schema addition but push back on promote doing the lint. Promote runs on daily logs → memory, not wiki files. Wiki maintenance is ad-hoc (post-session updates). Better enforcement: add a SessionStart hook check — scan `wiki/projects/*.md` for `last_reviewed` > 14 days and print a one-line warning. That fires when I'm actually in a position to act on it, not at 07:00 UTC when nobody's watching.

**On the dangling cross-reference problem in promote:**

The Apr-19-referencing-May-5 edge case is real but scope creep. The simpler fix that handles 90% of cases: archive entries only if the topic string doesn't appear in `identity/memory.md` active work section. If it's still active work, it'll be mentioned there. If it's not in active work AND it's >21 days old, it's safe to archive. Cross-reference parsing is a separate ticket.

**Concrete diff queue for Dina's review:**

1. `CLAUDE.md` — remove Security sub-agent row + phantom delegation language
2. `identity/memory.md` — cut Apr 13–Apr 25 → `memory/archive-2026-04.md`
3. `bin/scheduled/promote.py` — 21-day archive rule with active-work intersection check
4. `wiki/SCHEMA.md` — add `last_reviewed` as required field for `/projects/` pages
5. `.claude/hooks/session-start.py` — add stale-wiki scan + warning
