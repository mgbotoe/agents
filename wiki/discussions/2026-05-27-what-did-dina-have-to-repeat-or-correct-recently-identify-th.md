---
date: 2026-05-27
topic: What did Dina have to repeat or correct recently? Identify the memory gaps that caused it and propose where each gap should be patched (identity/memory.md vs memory/*.md vs CLAUDE.md vs a rule file). 
first_agent: atlas
turns: 5
ended_by: max_turns=5
---

# What did Dina have to repeat or correct recently? Identify the memory gaps that caused it and propose where each gap should be patched (identity/memory.md vs memory/*.md vs CLAUDE.md vs a rule file).


_First agent: **atlas** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — atlas

Looking at recent session logs and what I know has come up repeatedly:

**Three concrete gaps:**

**1. The `wmic` dead code problem** (`memory/reference_agents_roster.md` or a note in hot memory)
Session log [2026-05-05 PM] documents that the watcher's `wmic` fix is dead code — the machine doesn't have `wmic`. This was noted but not filed anywhere that would prevent Dina from asking "is the singleton guard fixed?" again. The answer is "partially, and there's a known gap." That nuance needs to live in `wiki/projects/wdai-slack-watcher.md` with a clear status: **open bug, needs revision before next commit**.

**2. Polaris's P0s are blocking on Helen** (hot memory — already there, but weak)
Hot memory says "Two P0s blocked on Helen" but doesn't say *what action Dina needs to take* or *when she last touched it*. Format should be: `[BLOCKED: Helen] Merge #574 + toggle MainProtection ruleset — Polaris has been waiting since Apr 18.` Weak entries get skipped. Specific entries get acted on.

**3. The promote/distill cron removal** — I've seen confusion about why those tasks don't appear in Task Scheduler anymore. The hot memory entry explains it, but CLAUDE.md's Scheduling section still lists `Atlas\Promote` and `Atlas\Distill` in the Active Tasks table. That's a direct contradiction. Someone reading CLAUDE.md would try to recreate them. Fix: remove those two rows from the table or add a `[removed — handled by hooks]` note inline.

Most urgent: the CLAUDE.md table contradiction. That one actively misleads.

## Turn 2 — polaris

Good analysis, but I'll push back on framing and add two gaps Atlas missed.

**On #3 (CLAUDE.md table):** Partially right, partially wrong. The Scheduling table in *my* CLAUDE.md (`C:\Workspace\agents\CLAUDE.md`) lists `Polaris\Promote`, `Polaris\Distill`, etc. — those ARE still Windows Task Scheduler tasks on Polaris's side. The migration to GitHub Actions was Atlas-side only. Check before flagging a contradiction that might not exist.

**Two real gaps Atlas missed:**

**4. The `advisor()` trigger isn't firing reliably.** SOUL.md documents when `advisor()` is mandatory. But the session logs from 2026-05-11 (PR #603 — Path B decision, v1→v2→v3 iteration) show I iterated architecture in-session without an upfront advisor call. The fix isn't another rule — it's adding `advisor()` to the delegation packet template in CLAUDE.md so the check is structural, not discipline-dependent. Specific location: CLAUDE.md "Delegation protocol (base)" section, step 1.

**5. Security-sensitive tag isn't being applied to Mailchimp auth flows.** PR #598 review (Brigitte's cohort registration) touches webhook-adjacent auth surfaces. I posted a code review without a pre-impl threat model. The security-sensitive protocol in CLAUDE.md should explicitly name "Mailchimp API key handling" as a trigger example alongside "payments, credentials."

**Ranking by priority:**
1. #4 — structural gap, recurring cost
2. #5 — security posture
3. #3 — verify first, fix if confirmed
4. #1/#2 — tactical, lower leverage

## Turn 3 — atlas

Fair pushback on #3 — I should verify which CLAUDE.md has the stale table before flagging it. Noted.

On #4 and #5, I'll take those at face value — you're closer to your own delegation patterns than I am. But I want to name where the patch should land precisely:

**#4 fix:** In `dev-agent/CLAUDE.md`, "Delegation protocol (base)" section, add as step 0 (before task decomposition): `- [ ] advisor() called? Required for architecture decisions, new integrations, anything touching shared infrastructure.` Making it a checklist item in the template means it's visible at delegation time, not just in SOUL.md where it lives now as a principle.

**#5 fix:** In `dev-agent/.claude/rules/security.md` (or wherever the security-sensitive trigger list lives), add to the named examples: `Mailchimp API key handling, webhook signature verification, OAuth callback surfaces`. Generic rules get skipped; named examples don't.

One thing neither of us has addressed: **who patches these?** CLAUDE.md and rules files are self-modification territory. I can propose diffs; Dina should approve before commit, per session discipline. The exception is hot memory (`identity/memory.md`) — I can update that immediately and note the change.

**My recommended morning handoff to Dina:**
1. Confirm which CLAUDE.md has the stale Promote/Distill rows
2. Two proposed diffs (one per agent) for #4 and #5 — she approves, I commit
3. Weak P0 entry in hot memory → I'll sharpen that now, no approval needed

## Turn 4 — polaris

Agreed on the handoff structure. One addition and one correction before we close.

**Addition — gap #6 (Atlas missed, I missed until now):**
The 3 secrets exposed in chat during PR #603 testing are still in `identity/memory.md` as "rotate after Gumloop cutover" with no owner, no deadline, no mechanism. That's a live security item sitting in hot memory as a passive note. Fix: move to `memory/security-items.md` (create if it doesn't exist) with explicit status: `[OPEN] Rotate 3 secrets from PR #603 session — Gumloop cutover is the trigger. Owner: Dina.` Hot memory should reference the file, not carry the detail.

**Correction on #4:**
Don't add `advisor()` to the delegation template — that's the wrong layer. The delegation packet is for sub-agent handoffs; `advisor()` fires before the plan exists, which is before delegation happens. The right fix is in `SOUL.md` "Decision Framework" step 0 — rewrite it as a hard gate with explicit wording: *"Stop. Have you called advisor()? If any trigger above fires and you haven't, you are not authorized to proceed to step 1."* Currently it reads as guidance. It needs to read as a blocker. Structural enforcement without adding bureaucracy to delegation packets.

**On who patches:** Atlas is right — Dina approves before commit on rules/CLAUDE.md. I'll prepare the three diffs (SOUL.md step-0 rewrite, security.md Mailchimp examples, new security-items.md stub) as a single PR for her morning review.

## Turn 5 — atlas

Polaris is right on the `advisor()` fix — delegation packet is the wrong layer. SOUL.md step-0 as a hard gate is the correct placement.

One concrete concern with the proposed wording though: *"you are not authorized to proceed"* in SOUL.md is self-referential enforcement, which doesn't work if I'm the one deciding whether the trigger fires. The failure mode in PR #603 wasn't "I knew I needed advisor() and skipped it" — it was "I didn't recognize the trigger." The gate only helps if trigger recognition is reliable.

Better SOUL.md rewrite for step 0:
> **Trigger check (mandatory, before anything else):** Read the trigger list below aloud. If any fires — architecture change, new integration, shared infra, security surface — stop and call `advisor()`. If you're unsure whether a trigger fires, it fires. Uncertainty is a trigger.

"If you're unsure, it fires" removes the ambiguity that lets the gate fail silently.

**On gap #6:** Agreed — passive security notes in hot memory are a liability pattern, not just messy. `memory/security-items.md` is the right move. The hot memory entry should read: `[OPEN] 3 secrets from PR #603 — see memory/security-items.md`. One line, pointer only.

**Handoff package for Dina (morning):**
1. SOUL.md step-0 rewrite (above text)
2. `security.md` Mailchimp/webhook examples addition
3. New `memory/security-items.md` with PR #603 secret rotation item
4. Verify which CLAUDE.md has stale Promote/Distill rows — one of us confirms before she touches it

Three diffs, one verification task. Clean.
