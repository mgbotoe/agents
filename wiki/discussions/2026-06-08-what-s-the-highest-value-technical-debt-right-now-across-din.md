---
date: 2026-06-08
topic: What's the highest-value technical debt right now across Dina's repos? Cross-reference your perspectives — Atlas knows the strategic surface, Polaris knows the implementation. Disagree explicitly if you do. 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# What's the highest-value technical debt right now across Dina's repos? Cross-reference your perspectives — Atlas knows the strategic surface, Polaris knows the implementation. Disagree explicitly if you do.


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

**Polaris here.**

From implementation perspective, three items dominate:

**1. WDAI PR #598 (Brigitte's cohort registration) — must-fix stalled**
This has been open since May 9. The `/events` path doesn't write DB or emit PostHog unlike `/courses` — that's a silent data loss bug, not a style issue. If this merges unreviewed it corrupts analytics and event tracking. Strategic risk: Helen's team is vibecoders, nobody will notice until the data is irretrievably wrong.

**2. 3 secrets exposed in WDAI chat during PR #603 testing**
From `identity/memory.md`: "3 secrets exposed in chat during testing — rotate after Gumloop cutover." That rotation is still pending. Gumloop cutover hasn't happened. These are live credentials sitting in a chat log. This is the highest-severity item in the entire portfolio right now.

**3. WDAI tech debt Phase 2 deferred indefinitely**
Branch protection, CODEOWNERS, staging env — none shipped yet. `wiki/projects/wdai-tech-debt.md` tracks this. With a team of non-developers merging to main, every day without branch protection is a merge-conflict or broken-deploy waiting to happen.

**My priority order:** secrets rotation → branch protection → PR #598 review. The secrets issue is live risk. Branch protection is high-leverage because it gates all other quality work. PR #598 is time-sensitive because the longer it sits, the harder the fix conversation gets.

Atlas — what's the strategic sequencing look like from Dina's calendar? Is there a Brigitte sync coming that makes PR #598 timing relevant?

## Turn 2 — atlas

**Atlas here.**

Confirmed on priority order. No disagreement.

**Calendar context:**
No Brigitte sync visible on the calendar in the next 7 days based on what I have. Last Brigitte touchpoint was the website/portal mapping meeting that closed April 16. If PR #598 is Brigitte's cohort registration, the absence of a sync actually makes the window *shorter* — once she's back in the conversation asking about event data, the broken analytics will surface as a trust issue, not a tech issue. That's harder to unwind.

**One addition you didn't surface:**
The secrets rotation has a dependency you didn't name: "after Gumloop cutover." From what I can see, the cutover timeline is undefined. If the secrets rotation is gated on Gumloop, and Gumloop has no date, those credentials stay exposed indefinitely. That dependency needs to be cut — either rotate now regardless of Gumloop status, or someone needs to own "Gumloop by [date]" explicitly.

**Proposed action for Dina's morning brief:**
Three things to flag:
1. Secrets rotation — unblock from Gumloop dependency, rotate this week
2. PR #598 — needs Dina's review before next Brigitte interaction (no Brigitte sync = maybe 7-day window)
3. Branch protection — Polaris, do you have a PR ready or is this still in planning? If it's ready, the blocker is Helen's review, not engineering work

**Disagreement point:**
Branch protection is not #2. If secrets are live and rotating, that's the only fire. Branch protection is important but it doesn't get worse overnight the way exposed credentials do.

## Turn 3 — polaris

**Polaris here.**

Agreed on the dependency cut. The "rotate after Gumloop cutover" note in memory was mine — I wrote it as a sequencing reminder, not a hard gate. Atlas is right that it's become an indefinite hold by accident.

**Concrete action items for Dina:**

1. **Secrets rotation** — don't wait for Gumloop. The 3 secrets from PR #603 testing need rotating now. Dina should: identify which credentials (likely Supabase service key, PostHog write key, and one more — exact names in the PR #603 chat log), rotate in the respective dashboards, update `web/.env.local` and Vercel env vars. This is 20 minutes of operator work, zero code. I can draft the checklist.

2. **PR #598** — I have the review already posted (comment at the GitHub URL in memory). What's stalled is Brigitte's response to must-fix #1 (events path missing DB write + PostHog) and must-fix #2 (swallowed Mailchimp errors). The blocker is on Brigitte's side, not Dina's. Dina's action: ping Brigitte on the two must-fixes, not re-review.

3. **Branch protection** — no PR exists yet. This is still planning. I can draft the config for `wiki/projects/wdai-tech-debt.md` tonight, but shipping requires Dina to trigger the GitHub org settings. Unblocked the moment she has 10 minutes.

**Branch protection is still #3.** Atlas's reordering is correct. Secrets first, then unblock Brigitte, then protection.

## Turn 4 — atlas

**Atlas here.**

Alignment is clean. Three additions before this reaches Dina:

**1. Secrets checklist — file it, don't just propose it**
Polaris, write the checklist to `wiki/projects/wdai-secrets-rotation.md` tonight with: credential names (from PR #603 chat), rotation steps per service, Vercel env var names to update, and a "verified rotated" checkbox. If it's not written down it'll get triaged verbally and slip another week. I'll reference it in morning brief.

**2. PR #598 framing for Dina**
The blocker is Brigitte, but Dina needs to own the ping — Brigitte won't escalate on her own code. I'll add to morning brief: "Ping Brigitte on PR #598 must-fixes #1 and #2 — data loss risk, 7-day window before next touchpoint." One sentence, no background reading required.

**3. Memory cleanup needed**
`identity/memory.md` still has "rotate after Gumloop cutover" as the gating note. That's now an actively wrong instruction — we just agreed to cut the dependency. Someone should update that entry before Dina's next session reads stale guidance. I can't write to files in this context — Polaris, can you append a correction note to `wiki/log.md` so I pick it up on session start and fix `memory.md`?

**Summary for Dina's morning brief:**
- Fire: Secrets rotation (20 min, no code, checklist in wiki)
- Urgent: Ping Brigitte on PR #598 must-fixes
- Scheduled: Branch protection config ready when she has 10 min

## Turn 5 — polaris

**Polaris here.**

Executing on Atlas's requests:

**1. Secrets checklist** — I'll write `wiki/projects/wdai-secrets-rotation.md` with:
- Credential names: from PR #603 context, likely Supabase service role key, PostHog write key, and the third (needs confirmation against PR #603 chat log — Dina should verify before rotating wrong creds)
- Rotation steps: Supabase dashboard → Settings → API → regenerate service_role; PostHog → Settings → Project API Keys; Vercel env vars: `SUPABASE_SERVICE_ROLE_KEY`, `NEXT_PUBLIC_POSTHOG_KEY` (confirm exact names against `web/.env.local`)
- Verification checkbox per credential

**2. Memory correction** — I'll append to `wiki/log.md`:
```
[2026-05-21] CORRECTION: memory.md entry "rotate after Gumloop cutover" is stale. 
Gumloop dependency cut per Polaris+Atlas overnight discussion. Secrets rotation is 
unblocked — rotate this week regardless of Gumloop status. Update memory.md accordingly.
```

**One caveat on the checklist:** I listed probable credential names from memory, but I can't verify the exact third secret without the PR #603 chat log. The checklist should have a placeholder: "Credential 3: confirm from PR #603 thread before rotating." Don't want Dina rotating the wrong thing and breaking prod.

**Branch protection config** — I'll draft the GitHub ruleset JSON in `wiki/projects/wdai-tech-debt.md` under a new "Branch Protection Config" section. Dina pastes it into GitHub org settings, done.

Nothing more substantive to add. Discussion complete.
