# Pass 1 · Process flows and user journeys

> **Status:** Last updated 2026-05-12 · Confidence: **mixed** — sequence diagrams reflect code-of-record where probed, illustrative ops journeys (Lauren's, Helen's morning brief, member lifecycle) explicitly flagged in-section.

**Part of the Pass 1 split.** See `01-system-context.md` for framing, the 7 Pass-3 design questions, and the C4 system overview. This file is one of the supplementary surfaces.

**Important framing:** "team-OS" throughout these documents refers to a **proposed future federation** that Pass 3 will design. It does not exist today. Phrasings like "Pass 3 must X" mean "X is a constraint surfaced by current state."

---

## Member surface — what's downstream of the WDAI boundary

Anchors the journeys below. The flows that follow connect to this surface from upstream (ops side) and from within (member experience side).

```mermaid
flowchart LR
    Members([~1180 Members])
    Portal[WDAI Portal]
    SlackWS[Slack workspace]
    MCEmail[Mailchimp emails]
    LumaReg[Luma registration]
    Voicemail[Twilio voicemail line]

    subgraph Programs[Programs]
        AIF[AI Foundations · Basics/Intermediate/Advanced]
        BT[Build TogetHER]
        SDT[Show Don't Tell]
        Geo[17+ Geo chapters]
        Affinity[Affinity groups]
    end

    subgraph MemberBots[Member-facing automations · only 3 currently]
        Newswire[WDAI Newswire welcome]
        BadgeBot[BadgeBot MVP]
        Hive[wdai-hive engagement]
    end

    Members --> Portal
    Members --> SlackWS
    Members --> MCEmail
    Members --> LumaReg
    Members -.-> Voicemail
    Portal --> Programs
    LumaReg --> Programs
    SlackWS -.-> Newswire
    AIF -.-> BadgeBot
    BT -.-> Hive

    classDef member fill:#fef3c7,stroke:#a16207
    classDef entry fill:#dcfce7,stroke:#166534
    classDef prog fill:#bbf7d0,stroke:#15803d
    classDef bot fill:#dbeafe,stroke:#1e40af
    class Members member
    class Portal,SlackWS,MCEmail,LumaReg,Voicemail entry
    class AIF,BT,SDT,Geo,Affinity prog
    class Newswire,BadgeBot,Hive bot
```

**Three takeaways anchored here:**

1. **Members have FIVE entry points, not one.** Portal, Slack workspace, Mailchimp emails, Luma registration, Twilio voicemail line. Programs are reached via Portal AND Luma (not Portal-only). Newswire posts are triggered by profile completion in Portal but the member sees them in Slack. Members never touch WDAI internal repos, agent stacks, or admin surfaces — but they touch MORE than one consumer-facing surface.

2. **Only THREE member-facing automations currently exist** — Newswire (welcome to community post on profile complete · platform-hosted Slack app · paradigm 4c), BadgeBot (MVP · cohort badges), wdai-hive (Build TogetHER weekly engagement DM · paradigm 2 Railway).

3. **Any Pass 3 federation lives upstream of this diagram.** The member surface is downstream of WDAI Operational Surface — the team-OS would produce programs; members consume them. Federation must not bleed into the member surface unless explicitly scoped to add a member-experience capability (which would inherit member-uptime expectations that paradigm 4 may not be able to meet — see SLA constraint in `03-operational-architecture.md`).

For the full inventory of member touch points (~30 surfaces — every API route, every Slack channel a member is in, every email cadence, every external integration), see `../deep-dive-member-surface.md`. The diagram above is the medium-resolution view; the deep-dive is the granular catalog; the C4 L1 in `01-system-context.md` is the single-arrow abstraction.

---

## Process flows (sequence diagrams)

How the system actually OPERATES — running flows that connect multiple containers.

### Member signup (Stripe checkout to first Slack post)

```mermaid
sequenceDiagram
 actor U as New member
 participant M as Marketing site
 participant S as Stripe
 participant P as Platform /api/stripe/webhook
 participant DB as Supabase
 participant C as Clerk
 participant N as Newswire
 participant AB as Admin Bot

 U->>M: visits /membership
 U->>S: checkout
 S-->>U: success redirect
 S->>P: webhook stripe.subscription.created
 P->>DB: create Membership
 P->>C: update publicMetadata.isMember
 P->>N: postProfileIntro · after profile complete
 P->>AB: postNewMemberAlert
 N->>Slack: post to #intros
 AB->>Slack: post to admin channel
```

Shows the multi-system dance behind one signup. A Pass 3 federation would not insert into this flow unless the design adds member-related capability — out-of-scope by default.

### Cohort kickoff (mailchimp-cc skill invocation)

```mermaid
sequenceDiagram
 actor B as Brigitte or Helen
 participant CC as Claude Code
 participant Skill as /new-basics skill
 participant Cfg as configs YAML
 participant Cal as Google Calendar
 participant MC as Mailchimp
 participant Preview as Browser preview

 B->>CC: /new-basics
 CC->>Skill: guided workflow start
 Skill->>B: ask for start date, cohort name, live session schedule
 B-->>Skill: provides details
 Skill->>Cfg: write YAML config
 Skill->>Cal: create public calendar
 Skill->>Preview: render all 15 emails locally
 B->>Preview: review
 B->>Skill: approve
 Skill->>MC: create 15 draft campaigns
 Skill->>MC: schedule ready campaigns
 Skill->>B: report status
```

7-step guided workflow. Each step has safety gates (dry-run, confirmation, marker validation). This is the Q4 onboarding pattern in action.

### Marketing copy generation (wdai-marketing pipeline)

```mermaid
sequenceDiagram
 participant Cron as GH Action 6am UTC · PAUSED 2026-04-21
 participant Luma
 participant Vault as vault/content-calendar.md
 participant Slack as #team-marketing-content-calendar
 participant UI as Vercel calendar UI
 participant DRI as DRI · Sandhya or Sheena
 participant AI as Anthropic API
 participant Promos as vault/promos
 participant MC as Mailchimp
 participant LI as LinkedIn

 Cron->>Luma: poll events
 Luma-->>Cron: events delta
 Cron->>Vault: write content-calendar.md
 Cron->>Slack: post calendar update with Approve/Edit buttons
 DRI->>UI: open calendar
 DRI->>UI: click Approve Plan
 UI->>AI: copy-generator · channel-specific
 AI-->>Promos: drafts saved
 UI->>DRI: DM with edit links
 DRI->>UI: approve copy
 UI->>MC: publish · campaign drafts
 UI->>LI: post to WDAI org page
```

Currently runs by manual `workflow_dispatch` since 2026-04-21. Two-touchpoint approval (plan, then copy). All state in flat-file YAML in the repo.

---


## Member-side program journeys

The three sequences above are ops-facing. Members never see them. These are the journeys members actually experience — and they reveal which containers a Pass 3 federation would need to leave alone (member-facing) vs which it might safely instrument (ops-facing).

### AI Foundations cohort experience (15 lessons · 3 weeks)

The flagship program — ~80% of cohort load. Touches the most containers.

```mermaid
sequenceDiagram
 actor M as Member
 participant Portal
 participant Luma
 participant MC as Mailchimp
 participant SlackCh as #aifoundations1-basics
 participant GMeet as Google Meet
 participant RecCron as Platform cron · collect-recordings
 participant UpCron as Platform cron · process-uploads
 participant Vimeo
 participant CourseRefl as Course Reflections bot
 participant DB as LessonProgress

 M->>Portal: enroll in AI Basics
 M->>Luma: register for cohort
 SlackCh-->>M: added to cohort channel
 MC->>M: pre-kickoff email · T-3 days
 MC->>M: pre-kickoff email · T-1 day

 loop Each weekday for 3 weeks
 MC->>M: daily lesson email with link
 M->>Portal: open lesson
 Portal->>DB: track LessonProgress
 opt Live session day · Mon and Thu
 Luma->>M: reminder
 M->>GMeet: join live session
 GMeet->>RecCron: daily midnight UTC drain + sweep
 RecCron->>UpCron: RecordingUpload row queued
 UpCron->>Vimeo: upload recording (every 2hr)
 UpCron->>MC: campaign update — add recap link
 end
 opt Member shares reflection
 M->>Portal: share lesson reflection
 Portal->>CourseRefl: shareReflectionToSlack
 CourseRefl->>SlackCh: post reflection · tags member
 end
 end

 MC->>M: post-cohort survey
```

**What this reveals:** a single cohort touches **Portal + Luma + Mailchimp + Slack + Google Meet + platform's collect-recordings cron + process-uploads cron + Vimeo + Course Reflections (platform Slack app) + LessonProgress DB**. Nine containers per member per cohort, all platform-hosted on Vercel paradigm 4b. **Constraint surfaced for Pass 3:** any federation design must not insert into these — they're all member-facing and working today.

**Probe-verified 2026-05-12:** the Meet→Vimeo pipeline is **NOT** on Helen's Mac mini. It is `web/app/api/cron/collect-recordings/route.ts` (daily midnight UTC, three phases: Drain · Tracked · Sweep) + `web/app/api/cron/process-uploads/route.ts` (every 2hr odd hours). The "Wit" label that earlier Pass 1 drafts used for this pipeline was misattributed to an OpenClaw agent; the actual implementation is platform paradigm 4b. **No SPOF on Helen's hardware here** — the pipeline runs in Vercel even if Helen's Mac mini is off.

### course-update-agent monthly autonomous PR flow (Q2 reference)

**15th of the month** at 9am UTC (verified `cron: '0 9 15 * *'` in `course-content-agent.yml`). Companion `website-content-agent` runs on the **1st** at 9am UTC (`0 9 1 * *`). The canonical "agent proposes, human approves" loop running in production today.

```mermaid
sequenceDiagram
 participant Cron as GH Actions cron · 15th 9am UTC
 participant Agent as course-update-agent
 participant DB as Supabase · AGENT_DATABASE_URL limited role
 participant Anth as Anthropic API
 participant Repo as wdai-foundation-platform repo
 participant PR as Pull Request
 participant CODEOWNERS as CODEOWNERS reviewers
 participant Helen

 Cron->>Agent: workflow start · concurrency-locked
 Agent->>DB: collect-content.js — snapshot lessons
 DB-->>Agent: content-snapshot.json
 Agent->>Anth: analyze + propose updates
 Anth-->>Agent: proposed changes
 Agent->>Repo: write ContentChangeBatch + ContentChangeProposal entities
 Agent->>PR: open PR with proposed updates
 PR->>CODEOWNERS: require review
 CODEOWNERS-->>Helen: notify
 alt Helen approves
 Helen->>PR: merge
 PR->>Repo: deploy via Vercel
 else Helen declines
 Helen->>PR: close
 Note over PR: proposals discarded · agent retries next month
 end
```

**What this reveals:** the autonomous agent has its OWN database connection (`AGENT_DATABASE_URL` — verified as a separate GH Actions secret in the workflow files). The name implies a scoped role; **actual DB privileges (read-only vs read-write, table-level grants) are not directly verified** — flagged in audit gaps. **The CODEOWNERS gate is the approval primitive.** PR review is non-optional. Two of these run monthly: **website-content-agent on the 1st, course-update-agent on the 15th** (probe-verified 2026-05-12 — earlier Pass 1 drafts had these reversed). Same shape, different content domain.

### Atlas → Polaris transcript pipeline (Q6 reference — working in Madina's stack)

How Madina's OpenClaw stack currently routes Granola transcripts AND enriches them with surrounding context. This is the per-user Granola consumption pattern Helen's design doc proposes scaling org-wide — but Atlas pulls more than just Granola to do it well.

```mermaid
sequenceDiagram
 actor Madina
 participant GranolaAcct as Granola
 participant Gmail
 participant GCal as Google Calendar
 participant Drive as Google Drive
 participant Atlas
 participant Wiki as wiki/sources/
 participant Log as wiki/log.md
 participant Memory as identity/memory.md
 participant Slack as #polaris-tl
 participant Polaris
 participant WikiProj as wiki/projects/

 Note over Atlas: hourly cron · 7am-3pm PT
 Atlas->>GranolaAcct: list_meetings · last hour
 GranolaAcct-->>Atlas: meeting metadata + transcript
 Atlas->>GCal: pull calendar context · attendees, prior meetings
 Atlas->>Gmail: scan related threads · invite, follow-ups
 opt meeting references a doc
 Atlas->>Drive: read referenced doc
 end
 Atlas->>Memory: read prior context · who, why, history
 Atlas->>Atlas: assess routing · technical/strategic/operational
 Atlas->>Wiki: write YYYY-MM-DD-slug.md · frontmatter + summary
 Atlas->>Log: append entry
 Atlas->>Memory: update relevant memory facts
 opt routing technical
 Atlas->>Slack: ping #polaris-tl with link
 end
 Note over Polaris: on session start
 Polaris->>Log: read recent entries
 alt has technical entry
 Polaris->>Wiki: read source frontmatter
 Polaris->>GranolaAcct: get_meeting_transcript · full
 Polaris->>WikiProj: update technical sections
 Polaris->>Memory: update technical memory if needed
 end
```

**What this reveals:** Atlas doesn't just route transcripts — it **enriches them** by pulling Calendar (who was there, what's the recurring context), Gmail (what threads led to this meeting, what follow-ups landed after), Drive (referenced docs), and Memory (who this person is, what we already know). The wiki entry is the OUTPUT of a multi-source synthesis, not just a transcript copy.

**Why this matters for Pass 3:** Helen's design doc proposes Granola → wiki as the pipeline. **Reality is richer.** A federation that ingests only Granola misses the Calendar/Gmail/Drive context that makes the wiki entry actually useful. Pass 3 must decide whether to:
- Federate Granola only (loses enrichment context)
- Federate Granola + enrichment sources (multiplies cross-account auth surface)
- Federate only the synthesized wiki output (sidesteps the per-user-account problem entirely)

**Constraint:** the pipeline is one-way (sources → wiki). No write-back into Granola/Gmail/Calendar/Drive. The wiki is the consolidation tier.

**The dedup problem when scaled:** Madina's Atlas reads Madina's Gmail+Cal+Drive+Granola. If Helen joins the team-OS, Helen's Syl reads Helen's Gmail+Cal+Drive+Granola. Two parallel synthesis pipelines for the same meeting produce overlapping but non-identical wiki entries. **This is the Q6 federation gap made concrete.**

### Member churn flow (surfaces the Wix → Stripe in-flight migration)

```mermaid
sequenceDiagram
 actor M as Member
 participant Portal
 participant StripePortal as Stripe Billing Portal
 participant Stripe
 participant WebhookHandler as platform /api/stripe/webhook
 participant DB as Supabase Membership
 participant Clerk
 participant AdminBot
 participant AdminCh as #devops-admin-mgmt
 participant Helen

 M->>Portal: click cancel subscription
 Portal->>StripePortal: redirect to Stripe customer portal
 M->>StripePortal: confirm cancel
 StripePortal-->>M: confirmation email
 Stripe->>WebhookHandler: subscription.canceled event
 WebhookHandler->>DB: update Membership.cancelAtPeriodEnd
 WebhookHandler->>Clerk: update publicMetadata
 WebhookHandler->>AdminBot: postChurnAlert · slack-admin.ts
 AdminBot->>AdminCh: post churn alert
 Helen->>AdminCh: triage / outreach
 Note over M: Wix retired 2026-05 · WixSync code may remain as dead code
```

**What this reveals:** the Stripe-webhook → AdminBot flow is **paradigm 4c** (platform-hosted Slack app). Wix is retired as of 2026-05 (user-confirmed) — earlier "WixSync parallel-run until cutover" claim is stale. WixSync code in `wdai-admin` is now dead path until cleanup. **The Airtable → Supabase migration still pending and remains the Lumabot guest-approval hazard.**

### Schema migration via Expand-Contract (Q5 reference pattern)

Documented in `wdai-foundation-platform/CLAUDE.md` golden rule: *"Code can be reverted. Database migrations cannot."* The canonical safe-migration pattern.

```mermaid
sequenceDiagram
 actor Eng as Engineer · Madina or Helen
 participant PR1 as PR 1 · Expand
 participant Deploy1 as Deploy
 participant Verify1 as Verify on staging Supabase
 participant PR2 as PR 2 · Migrate code
 participant Deploy2 as Deploy
 participant Stable as Stability check 1+ days
 participant PR3 as PR 3 · Contract

 Eng->>PR1: add new column · keep old · code reads both writes both
 PR1->>Deploy1: merge
 Deploy1->>Verify1: Vercel preview against staging Supabase
 Verify1-->>Eng: green
 Eng->>PR2: code now reads/writes only new column
 PR2->>Deploy2: merge
 Deploy2->>Stable: monitor 24-48h
 alt staging stable
 Eng->>PR3: drop old column
 PR3->>Deploy2: merge · irreversible
 else regression
 Eng->>PR2: revert
 Note over Eng: old column still there · safe rollback
 end
```

**What this reveals:** the platform team has a discipline for cross-repo migrations BUT the same discipline isn't enforced cross-repo. **The Airtable → Supabase migration affects Lumabot, which doesn't even have its own DB migration story** (lumabot deep-dive: no tests, no migrations directory). Expand-Contract works inside the platform; it doesn't extend to other repos that depend on shared external data sources.

### Helen's morning briefing (Syl + Gumloop · OpenClaw paradigm 1 in practice)

**Illustrative.** Helen has spoken about Syl + Gumloop in `#topic-openclaw`-style channels and her design doc; the specific cron time (6am PT), the dual-Gmail-address calendar read (`helen@womendefiningai.com` per platform `.env.local` + a personal Gmail inferred from her `helenlkupp` GitHub handle), and the exact sequence of API calls below are **inferred from her stated tool stack and not directly observed from her config files**. Helen committed her OpenClaw config files to a repo Apr 9 — verification would require reading that repo.

```mermaid
sequenceDiagram
 participant Cron as Mac mini cron · 6am PT
 participant Syl
 participant GMailAPI as Gmail historyId cursor
 participant GCal as Google Calendar
 participant Mailchimp as Mailchimp campaigns
 participant LinearMCP as Linear MCP
 participant SlackPersonal as Helen-personal Slack channel
 participant Gumloop as Gumloop daily briefing
 participant TeamAgents as #team-agents

 Cron->>Syl: morning brief task
 Syl->>GMailAPI: fetch new since last cursor
 GMailAPI-->>Syl: new threads
 Syl->>GCal: read calendar · helen@womendefiningai.org + helenlkupp@gmail.com
 Syl->>Mailchimp: check today's campaign queue
 Syl->>LinearMCP: read backlog status
 Syl->>SlackPersonal: post morning brief · calendar + priorities
 Note over Gumloop: separate parallel flow
 Gumloop->>TeamAgents: daily Gumloop briefing post
 Note over Helen: Helen consumes both
```

**What this reveals:** Helen runs **two parallel briefing systems** — Syl (OpenClaw on Mac mini) for personal/work synthesis, and a Gumloop briefing for `#team-agents` workspace context. **They don't share state.** Q1's runtime question is partly "do we collapse this into one or accept the two-runtime cost." The OpenClaw side is laptop-bound (Mac mini must be on); the Gumloop side is vendor-cloud (works regardless of Helen's machine).

### Generic event journey (Build TogetHER · Show Don't Tell · guest speakers)

Same shape across all monthly/ad-hoc events. The marketing pipeline drives announcement; the event runs through Luma + Google Meet + Wit; recap goes via Mailchimp.

```mermaid
sequenceDiagram
 actor M as Member
 participant MktAction as wdai-marketing GH Action
 participant SlackEvents as #events
 participant LinkedIn as WDAI LinkedIn
 participant Luma
 participant GMeet
 participant Wit
 participant Vimeo
 participant Newswire
 participant MC as Mailchimp

 MktAction->>SlackEvents: announcement · with calendar link
 MktAction->>LinkedIn: org page post
 MktAction->>MC: campaign drafts
 Note over M: discovers via Slack, LinkedIn, or email
 M->>Luma: register
 Luma-->>M: calendar invite
 Luma->>M: reminder T-1h
 M->>GMeet: attend live
 GMeet->>Wit: end-of-day pipeline
 Wit->>Vimeo: upload recording
 Wit->>Newswire: postRecordingApprovalRequest
 Note over Newswire: Helen approves recording in admin channel
 MC->>M: recap email with recording link
```

**What this reveals:** the same Wit/Vimeo/Newswire pipeline serves every event type. The marketing pipeline (currently paused cron, manual `workflow_dispatch`) is the entry point. **If the marketing cron stays paused, no events get auto-announced — they fall back to manual Slack posts.**

### Build TogetHER engagement loop (the wdai-hive layer)

Build TogetHER has a unique engagement primitive — the `wdai-hive` bot DMs members weekly "Did you play with AI this week?" and tracks responses. Different from other programs.

```mermaid
sequenceDiagram
 actor M as Member of #programs-buildtogether
 participant Hive as wdai-hive bot
 participant SupabaseHive as Supabase wdai-hive DB
 participant Admin as Admin dashboard

 Note over Hive: cron · weekly check-in
 Hive->>M: DM "Did you play with AI this week?"
 alt Member responds
 M->>Hive: structured response · category + tool + optional "Other"
 Hive->>SupabaseHive: store response
 else No response
 Note over Hive: opt-out / retention preference respected
 end
 Note over Admin: Helen or staff exports CSV with audit log
 Admin->>SupabaseHive: CSV export
```

**What this reveals:** wdai-hive runs as its own paradigm-2 service (Railway-deployed per repo README) with its own Supabase tier. **It's the only program-level engagement-tracking instrument in WDAI.** AI Foundations and Show Don't Tell don't have equivalent loops — they rely on Mailchimp open/click data and Pattern's weekly metrics report.

### Cross-program member lifecycle (journey diagram)

**Illustrative.** A member's *typical* arc through WDAI programs over months. Emotion scores (1-5) are notional — they're not from member-survey data, they represent qualitative judgment of which stages feel rewarding vs friction-heavy. The container-coverage claim that follows is real; the emotional shape is hypothesis.

```mermaid
journey
    title A member's path through WDAI programs
    section Discovery
      Marketing site visit: 3: Member
      LinkedIn post or friend ref: 4: Member
    section Onboarding
      Pricing then Stripe checkout: 4: Member
      Clerk auth and portal account: 5: Member
      Slack invite click: 4: Member, Newswire
      Profile complete and Newswire intro: 5: Member, Community
    section First cohort
      Enrolls AI Foundations Basics: 5: Member
      3 weeks of daily emails: 4: Member
      Live sessions on Mon and Thu: 5: Member
      Shares reflections to cohort channel: 4: Member, Community
    section Ongoing engagement
      Build TogetHER monthly: 4: Member, Community
      Show Don't Tell speaker series: 4: Member
      Geo chapter local meetup: 5: Member
      Affinity group ongoing: 5: Member
    section Deeper participation
      Intermediate cohort: 5: Member
      Advanced cohort: 5: Member
      Becomes cohort mentor: 5: Member, Community
    section Possible exit
      Survey response: 3: Member
      Churn via Stripe portal: 2: Member
      AdminBot churn alert: 5: Helen
```

**What this reveals:** a member's journey spans **8+ container surfaces over 6+ months**. **Constraint surfaced for Pass 3:** any federation design must respect this arc — internal automations cannot interrupt or disrupt these member-facing touchpoints.

**Critical: there is no team-OS instrumentation at the journey level today.** Each container tracks its own metrics (Mailchimp opens, LessonProgress, EventRsvp, churn alerts). No view connects them into a per-member journey timeline. Pattern's weekly report aggregates but doesn't trace individual journeys.

---


## Programs-side ops journey (Lauren · Programs lead)

Lauren runs cohorts week-to-week. Her ops journey shows how a non-engineer leader currently navigates the system.

```mermaid
sequenceDiagram
 actor L as Lauren · Programs lead
 participant Helen
 participant Cursor as Cursor + Claude Code
 participant MCC as mailchimp-cc CLI
 participant ConfigYAML as configs/cohort.yaml
 participant GCal as Google Calendar
 participant LumaUI as Luma admin UI
 participant MailchimpUI as Mailchimp UI
 participant SlackCh as #aifoundations1-basics

 Note over L: ~3 weeks before cohort
 L->>Helen: confirms cohort dates + live session schedule
 L->>Cursor: /new-basics skill
 Cursor->>L: walks through 7-step guided workflow
 L->>ConfigYAML: provides cohort name, dates, live session times
 Cursor->>MCC: generate config + render emails locally
 L->>Cursor: review preview, iterate copy
 Cursor->>GCal: create public subscribe calendar
 Cursor->>MailchimpUI: create 15 draft campaigns
 Cursor->>L: scheduled status report

 Note over L: During cohort
 L->>LumaUI: live session attendance
 L->>SlackCh: monitors cohort channel
 L->>Cursor: campaign update with recap links

 Note over L: After cohort
 L->>MailchimpUI: post-cohort survey send
 L->>Helen: retro chat
```

**What this reveals:** This diagram is an **illustrative ops journey** — Lauren is documented as Programs & Ops lead (wiki) and is the most likely owner of cohort kickoff, but whether she personally runs `/new-basics` end-to-end (vs Brigitte or Helen) is **not directly verified**. The cohort-kickoff sequence diagram above lists actor as "Brigitte or Helen" — the two diagrams haven't been reconciled against a single source of truth for who runs which step. The pattern itself (skill-driven, guided, browser-preview-before-commit) is real; the role attribution is inferred. If the `mailchimp-cc` tiered model does work for non-engineers, this is the kind of journey that would prove it.

If a Pass 3 onboarding plan can match this UX (guided slash-command workflow, preview before commit, browser+CLI mix), it will work for Sandhya / Sheena / Brigitte. If it requires writing TypeScript, it will not.

---
