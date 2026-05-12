# Comprehensive Bot/Agent Registry — WDAI Slack Workspace

_Audit covers 82 unique channels across 87 file reads + 4 inline-only channels (devops-twilio-alerts, team-marketing-content-calendar, ops-edu-content-on-social, test-module3-recipeflow)._

> **🛑 CORRECTION (post-platform inspection):**
>
> Two of the bots cataloged below — **WDAI Newswire** (`B0A4747GZ2A`) and **AdminBot** (`B08GF1SGGNL`) — are NOT external Slack apps. They are **Slack apps whose implementation code lives inside `wdai-foundation-platform`**:
> - **WDAI Newswire** code: `web/lib/slack.ts` — 10+ posting functions (postProfileIntro, postNewEvent, postNewResource, postWeeklyEventsDigest, postCronAlert, postWebhookFailureAlert, postStaleCacheAlert, shareReflectionToSlack, postToChannel, formatReflectionMessage).
> - **AdminBot legacy** code: `wdai-admin/src/services/memberbot.ts` (Fastify on Railway) — **deprecating**.
> - **AdminBot new** code: `web/lib/slack-admin.ts` — 6 functions: postNewMemberAlert, postChurnAlert, postUnsubscribedJoinAlert, postWeeklyStatsAlert, postRecordingApprovalRequest, postRecordingUploadFailed.
>
> A paradigm-2→paradigm-4 migration is in flight: Slack-admin.ts header verbatim: *"This replaces the Railway internal webhook relay — notifications are now sent directly from Vercel instead of routing through Railway's MemberBot service."*
>
> See `platform-hosted-bots.md` for the full correction.

## Headline


**34 unique bots/agents found across the workspace, spread over 6 execution paradigms** (audit later surfaced Perplexity Computer Spaces as paradigm 6, plus paradigm 4 splits into 4a GitHub Actions / 4b Vercel Cron / 4c Platform-hosted Slack apps). All Gumloop flows share ONE Slack user_id (U089ZGUGCUR / bot_id B0896A6N147) — they are indistinguishable from Slack's perspective. Per-flow identity only exists inside Gumloop's own UI (each flow has a gumloop.com/agents/<id> URL).


## Execution paradigm classification


| Paradigm | Bots | Notes |
|---|---|---|

| **1 · OpenClaw desktop** (Helen's Mac mini) | Syl, Pattern, Wit (Wit silent in channels read) | Personal credentials, scheduled tasks, laptop-bound |

| **2 · Production microservices** | AdminBot (`wdai-admin` Fastify), Lumabot (`wdai-lumabot` Railway, not seen in channel — runs scheduled), Foundation Platform (Vercel) | Always-on, service credentials |

| **3 · SaaS workflow agents (Gumloop)** | All under bot_id B0896A6N147 — daily briefing, website-feedback router, voicemail transcription, recipe picker, member intro/welcome (separate from Newswire), `/gummie add` agents like 'Optimistic Nova' | Single Slack identity for many flows. Auditable only inside Gumloop UI. |

| **4 · Cloud cron / GitHub Actions** | WDAI Marketing Content Calendar (B0B1J2S4D2R, daily 6am UTC, calendar updates), WDAI Newswire (B0A4747GZ2A, welcome messages), WDAI Scheduler (B091451E5G8) | Code-defined, free GH infra |

| **5 · Slack Workflow Builder** | Educational Content - Reminder (B07FZCMDKNC, weekly since Dec 2024) | Native Slack, no code. Likely more — only one surfaced |

| **Personal Slack apps (member-built)** | Akshita's Assistant (B0AL5HUS679), Anennya/Maninder/Simi/Carolyn/etc personal apps in #automation-test, Polly (B06451SB6RJ — poll bot) | Each member's own integration |


## Full bot registry (sorted by message volume)


| user_name | bot_id | app_id | Channels | Total msgs | First seen | Last seen |
|---|---|---|---|---|---|---|

| AdminBot | `B08GF1SGGNL` | `A08FSHDC467` | devops-admin-mgmt(197) | 197 | 2026-01-01 | 2026-01-09 |
| Gumloop | `B0896A6N147` | `A066JDWQV0V` | team-agents(35), helen-slack-triage(27), ops-customer-support-emails(18), gtmops-newsletter(11), devops-website-alerts(1) | 92 | 2025-11-11 | 2026-05-04 |
| WDAI Newswire | `B0A4747GZ2A` | `A0A46V3SB6J` | intros(28), events(22), share-demos-and-examples(11), team-programs(10) | 71 | 2026-04-16 | 2026-05-12 |
| Syl | `B0AETEBQFFT` | `A0AEEGV8GTU` | team-agents(47) | 47 | 2026-02-11 | 2026-03-09 |
| Slackbot | `BSLACKBOT` | `-` | topic-openclaw(3), topic-product(2), topic-vibecoding(2), geo-london(2), geo-sf-bay-area(2), geo-seattle(2), topic-lovable(2), website-feedback(1), topic-people(1), topic-founders(1), topic-marketing( | 20 | 2026-02-25 | 2026-03-15 |
| Educational Content - Reminder (Slack Workflow) | `B07FZCMDKNC` | `A07D9KP9R2Q` | ops-edu-content-on-social(20) | 20 | 2024-12-27 | 2025-09-19 |
| Pattern | `B0AKLSACYMR` | `A0AKBPQG1RD` | ops-website(10), team-core(6), devops-website-alerts(2) | 18 | 2026-03-11 | 2026-05-11 |
| Computer | `B0AMWHW76CW` | `A07NV1D07QT` | devops-website-alerts(18) | 18 | 2026-04-29 | 2026-05-10 |
| Slackbot | `B09HYPKG22K` | `-` | aifoundations-mentors(18) | 18 | 2026-03-26 | 2026-05-01 |
| Slackbot | `-` | `-` | ext-plus-one-beta(15), ext-wdai-charter(1), ext-bolt-wdai-partnership(1) | 17 | 2025-11-14 | 2026-05-11 |
| Carolyn Roth | `B08QFEEE6BS` | `A024R9PQM` | programs-showdonttell(16) | 16 | 2025-10-03 | 2026-04-28 |
|  | `B0A3QG90R0V` | `-` | aifoundations1-basics(13) | 13 | 2026-05-07 | 2026-05-11 |
| Slackbot | `B01` | `-` | gtmops-newsletter(4), wdai-admin(4), book-club(3) | 11 | 2025-07-07 | 2026-04-28 |
| Gumloop (voicemail flow) | `B0896A6N147` | `A066JDWQV0V` | devops-twilio-alerts(10) | 10 | 2025-11-27 | 2026-02-25 |
| Anennya Veeraraghavan | `B08UCA6FU4B` | `A07FPU6DA9E` | automation-test(7) | 7 | 2025-05-30 | 2025-05-30 |
|  | `B0A3QGWTXPX` | `-` | aifoundations2-intermediate(7) | 7 | 2026-03-18 | 2026-04-07 |
|  | `B0A4N9GRT08` | `-` | aifoundations3-advanced(5) | 5 | 2026-04-22 | 2026-05-08 |
| WDAI Marketing Content Calendar | `B0B1J2S4D2R` | `(GH Actions)` | team-marketing-content-calendar(5) | 5 | 2026-05-05 | 2026-05-05 |
| Maninder Paul | `B08DQ5Z7XSB` | `A07FPU6DA9E` | automation-test(4) | 4 | 2025-02-26 | 2025-02-26 |
|  | `B0ATSGY9L20` | `-` | team-marketing-workstream2-content-ideas(4) | 4 | 2026-05-04 | 2026-05-04 |
|  | `B09A1UTL6AX` | `-` | team-agents(2), ops-customer-support-emails(1) | 3 | 2026-01-27 | 2026-02-06 |
| Helen Lee Kupp | `B05PNPUDJNS` | `A0F827J2C` | topic-hermes(1), team-core(1), ext-bolt-wdai-partnership(1) | 3 | 2025-11-14 | 2026-05-01 |
| Helen Lee Kupp | `B09J9S88C3D` | `A066JDWQV0V` | team-core(1), gtmops-newsletter(1), helen-slack-triage(1) | 3 | 2025-11-16 | 2026-01-31 |
| Akshita's Assistant | `B0AL5HUS679` | `A0ALJUJC7FY` | akshita-assistant(3) | 3 | 2026-03-14 | 2026-03-14 |
| Simi Kaur | `B08P10UD4BS` | `A07FPU6DA9E` | automation-test(2) | 2 | 2025-04-16 | 2025-04-16 |
| Claude | `B09JB0P7ZN2` | `A08SF47R6P4` | team-agents(1) | 1 | 2026-02-07 | 2026-02-07 |
| WDAI Scheduler | `B091451E5G8` | `A0907BR6YKG` | automation-test(1) | 1 | 2025-06-06 | 2025-06-06 |
| BadgeBot | `B09RZ66FS9F` | `A09RBKJHWQG` | gig-badges-n-beyond(1) | 1 | 2026-02-20 | 2026-02-20 |
| donald | `BFXJBSRL7` | `A0F827J2C` | ext-bolt-wdai-partnership(1) | 1 | 2025-11-14 | 2025-11-14 |
| Slackbot | `B08NDJZPYEQ` | `-` | general(1) | 1 | 2026-04-29 | 2026-04-29 |
| Looking for Show Don't Tell Presenters | `B08UG73U7PA` | `A08TVV2P2G4` | share-demos-and-examples(1) | 1 | 2026-05-11 | 2026-05-11 |
| Polly | `B06451SB6RJ` | `A04E6JX41` | geo-dallas(1) | 1 | 2025-07-08 | 2025-07-08 |
| Optimistic Nova (Gumloop agent in #test-module3-recipeflow) | `B0896A6N147` | `A066JDWQV0V` | test-module3-recipeflow(1) | 1 | 2026-02-17 | 2026-02-17 |
| Gumloop Recipe Picker (in #tests-busola-oladapo) | `B0896A6N147` | `A066JDWQV0V` | tests-busola-oladapo(1) | 1 | 2026-04-12 | 2026-04-12 |


## Samples per bot


### AdminBot · `B08GF1SGGNL` · `app:A08FSHDC467`
- [devops-admin-mgmt] :tada: New Member for WDAI Dot ORG: Sade J Owoye (Monthly)
- [devops-admin-mgmt] :tada: New Member for WDAI Dot ORG: Sasha Mathew (Annual)

### Gumloop · `B0896A6N147` · `app:A066JDWQV0V`
- [team-agents] ---  *:fire: TODAY'S CRITICAL PRIORITY — Tuesday, January 27*  &gt; *WIN AI Challenge Grant is due TOMORROW (January 28)*  This is the $5M proposal targeting 50,000 learners. Everything else today should serve or not interfere with grant co
- [team-agents] ---  :fire: *TODAY'S #1 PRIORITY: WIN CHALLENGE DEADLINE*  Helen, here's the critical picture:  ---  *:date: CALENDAR REALITY — Wednesday, January 28*  • :fire: *WIN Challenge Deadline is TODAY* • Your calendar is otherwise clear — no meeti

### WDAI Newswire · `B0A4747GZ2A` · `app:A0A46V3SB6J`
- [intros] Welcome to the community, Patty OBrien Novak!
- [intros] Welcome to the community, Evelyn Wong!

### Syl · `B0AETEBQFFT` · `app:A0AEEGV8GTU`
- [team-agents] Syl test ping: if you see this, outbound Slack posting works; mention intake may still need one more setting.
- [team-agents] Board meeting doc — first-pass feedback notes for Helen to edit tomorrow:  • Narrative arc: Wins → Risks → Decisions Needed • Metrics table per key KPI: baseline, current, target, owner • Scope control: explicitly state what WDAI is not doi

### Slackbot · `BSLACKBOT` · `app:-`
- [topic-openclaw] <@U0AH4HRB1PY> joined #topic-openclaw. They’re also new to WomenDefiningAI.
- [topic-openclaw] <@U0AHLA6K45U> joined #topic-openclaw. They’re also new to WomenDefiningAI.

### Educational Content - Reminder (Slack Workflow) · `B07FZCMDKNC` · `app:A07D9KP9R2Q`
- [ops-edu-content-on-social] Pick 1 item from the last two weeks and share with Rocci for Monday's LinkedIn post — Slack Workflow Builder, weekly since Dec 2024

### Pattern · `B0AKLSACYMR` · `app:A0AKBPQG1RD`
- [team-core] <https://weekly-wdai-report.vercel.app> (commit a146f97): 43 new signups against 12 cancellations, for net growth of 31, with churn still elevated versus recent weeks. The main activation bottleneck remains post-Slack onboarding: 46.5% of n
- [team-core] <https://weekly-wdai-report.vercel.app> | commit 5f1c4e4 Growth outpaced churn this week, with 63 new signups against 5 cancellations, so net member momentum stayed clearly positive. The main activation bottleneck is setup completion, not S

### Computer · `B0AMWHW76CW` · `app:A07NV1D07QT`
- [devops-website-alerts] *WDAI On-Call — Sentry probe still skipping (3rd day): retro + real fix*  Today's 1pm cron skipped Sentry again. Yesterday's "fix" did not actually take. Honest retro:  *Why yesterday's fix didn't work* I patched two files — the bundled `bo
- [devops-website-alerts] *WDAI On-Call — cron task body rewritten (real fix this time)*  The `schedule_cron` tool became available this session, so I rewrote the cron task itself instead of just patching downstream files. The Apr 27/28/29 silent-Sentry-skip pattern

### Slackbot · `B09HYPKG22K` · `app:-`
- [aifoundations-mentors] 
- [aifoundations-mentors] 

### Slackbot · `-` · `app:-`
- [ext-wdai-charter] *e* from *The San Francisco Standard* was added to this channel by *helenlkupp*. You can review their permissions in Channel Details. Happy collaborating!
- [ext-plus-one-beta] *b&amp;n atelier* has removed themselves from this channel.

### Carolyn Roth · `B08QFEEE6BS` · `app:A024R9PQM`
- [programs-showdonttell] Thank you to everyone who joined 'Show, Don’t Tell'!  HUGE thank you to our presenters. We appreciate you!  You can find the recording here: &lt;<https://vimeo.com/1122998170?share=copy>  (password: let-the-demo-speak-for-itself!)  Full res
- [programs-showdonttell] Thank you to everyone who joined 'Show, Don’t Tell'!  HUGE thank you to our presenters. We appreciate you!  You can find the recording here: &lt;<https://vimeo.com/1130982096?share=copy&amp;fl=sv&amp;fe=ci>  (password: let-the-demo-speak-fo

###  · `B0A3QG90R0V` · `app:-`
- [aifoundations1-basics] New reflection from Katie Shay Perault: This was helpful - but it worked best when I also added the "magic words" from a previous lesson. On...
- [aifoundations1-basics] New reflection from Beatrice Stonebanks: I tested both on a real company post — announcing Team Playlists on the YouTube channel. Which captu...

### Slackbot · `B01` · `app:-`
- [gtmops-newsletter] Reminder: End of month recap of community discussions and highlights are coming up :sparkles: . How is the internal community conversations round up going?
- [gtmops-newsletter] Reminder: End of month recap of community discussions and highlights are coming up :sparkles: . How is the internal community conversations round up going?

### Gumloop (voicemail flow) · `B0896A6N147` · `app:A066JDWQV0V`
- [devops-twilio-alerts] :telephone_receiver: New Voicemail Received — Twilio voicemail transcriptions, since Dec 2025

### Anennya Veeraraghavan · `B08UCA6FU4B` · `app:A07FPU6DA9E`
- [automation-test] Vote for a meeting time
- [automation-test] Vote for a meeting time

###  · `B0A3QGWTXPX` · `app:-`
- [aifoundations2-intermediate] New reflection from Anna Schocket: I am not going to lie.  This was my most involved lesson so far in all of the coursework.  Between r...
- [aifoundations2-intermediate] New reflection from Nina Cooper: We are already using projects for product descriptions and blog posts but I can see that there are s...

###  · `B0A4N9GRT08` · `app:-`
- [aifoundations3-advanced] New reflection from Kristen E Clarke: Day 7: Oh my gosh, it worked!! I can't believe after all the struggles I had last week on the JSON l...
- [aifoundations3-advanced] New reflection from Anna Schocket: This was really fun!  I created an app (https://picky-eater-chef.lovable.app) to help identify kid f...

### WDAI Marketing Content Calendar · `B0B1J2S4D2R` · `app:(GH Actions)`
- [team-marketing-content-calendar] :date: Content Calendar Update — events with Approve/Edit buttons, paradigm-4 GitHub Action posting

### Maninder Paul · `B08DQ5Z7XSB` · `app:A07FPU6DA9E`
- [automation-test] Email was successfully sent to Maninder
- [automation-test] Email was successfully sent to Maninder

###  · `B0ATSGY9L20` · `app:-`
- [team-marketing-workstream2-content-ideas] 📅 Content Calendar Update *Community Meet + Greet* Type: `other` | Start: May 7 DRI: Sheena *Channel Plan:* • Slack — Apr 23 — Announce event in #general • LinkedIn · WDAI — Apr 27 — LinkedIn announcement • Slack — May 4 — Final reminder ✅
- [team-marketing-workstream2-content-ideas] 📅 Content Calendar Update *Community Meet + Greet* Type: `other` | Start: May 7 DRI: Sheena *Channel Plan:* • Slack — Apr 23 — Announce event in #general • LinkedIn · WDAI — Apr 27 — LinkedIn announcement • Slack — May 4 — Final reminder ✅

###  · `B09A1UTL6AX` · `app:-`
- [team-agents] :white_check_mark: Gummie 'Smart Dash' is now active in this channel! Mention <@U089ZGUGCUR> to start chatting.
- [team-agents] :wastebasket: Agent 'Smart Dash' removed from this channel.

### Helen Lee Kupp · `B05PNPUDJNS` · `app:A0F827J2C`
- [topic-hermes] hermes bag
- [team-core] cave dweller

### Helen Lee Kupp · `B09J9S88C3D` · `app:A066JDWQV0V`
- [team-core] *Draft for leads - working version drafted with Gumloop assistance*  ---  *WDAI 2026: The Messy Middle*  Hey everyone—  I've been meaning to write this for a while, but it's been a crazy start to the new year so apologies for the delay!  20
- [gtmops-newsletter] :mega: *Newsletter 2026 Strategy Meeting — Tomorrow!*  <@U07CKC07L9H> <@U09225TV4P8> <@U07RXP20FFB> — Ahead of our meeting tomorrow (Thursday 1/29, 12:30 PM PST), I wanted to share some thinking on where we might take the newsletter this ye

### Akshita's Assistant · `B0AL5HUS679` · `app:A0ALJUJC7FY`
- [akshita-assistant] Personal Slack app — bot owned by Akshita Ganesh, NOT Gumloop

### Simi Kaur · `B08P10UD4BS` · `app:A07FPU6DA9E`
- [automation-test] Email was successfully sent to Simi
- [automation-test] Email was successfully sent to Atharv

### Claude · `B09JB0P7ZN2` · `app:A08SF47R6P4`
- [team-agents] Got it. I've read your operating manual. Here's my honest assessment based on everything I've observed:  *Where you're being authentic:*  Your zero-to-one strength is undeniable. You built WDAI from nothing, created automation systems, stoo

### WDAI Scheduler · `B091451E5G8` · `app:A0907BR6YKG`
- [automation-test] <@U05HPDCV076> has suggested these times to meet. Please vote on what works for you and a meeting invite will follow. *Option 1* June 7th, 2025 at 4:00 AM PDT *Option 2* June 16th, 2025 at 3:53 PM PDT *Option 3* June 30th, 2025 at 3:53 PM P

### BadgeBot · `B09RZ66FS9F` · `app:A09RBKJHWQG`
- [gig-badges-n-beyond] :books: *Lesson 1: Brief intro to GenAI*  Share your reflections below! :thought_balloon:

### donald · `BFXJBSRL7` · `app:A0F827J2C`
- [ext-bolt-wdai-partnership] hi

### Slackbot · `B08NDJZPYEQ` · `app:-`
- [general] 

### Looking for Show Don't Tell Presenters · `B08UG73U7PA` · `app:A08TVV2P2G4`
- [share-demos-and-examples] :meow_attention: Looking for 'Show, Don't Tell' presenters!  _What is 'Show, Don't Tell'?_  'Show, Don’t Tell' is a quick informal 30-min monthly webinar where WDAI members share real AI use cases and workflows.  Each presenter has 10 minut

### Polly · `B06451SB6RJ` · `app:A04E6JX41`
- [geo-dallas] *This polly is closed.* *Sheena Miles* (Polly Sender: <@U06R9QYUW68>) has a polly for you!

### Optimistic Nova (Gumloop agent in #test-module3-recipeflow) · `B0896A6N147` · `app:A066JDWQV0V`
- [test-module3-recipeflow] :warning: No agent has been added — gumloop.com/agents/p7ztoanTKSbSzJMQJHKNCL

### Gumloop Recipe Picker (in #tests-busola-oladapo) · `B0896A6N147` · `app:A066JDWQV0V`
- [tests-busola-oladapo] :knife_fork_plate: This week's recipe picks are in! 5 dinner options with reply numbers


## Critical findings


1. **Gumloop is internally anonymous.** One Slack user_id for ALL Gumloop flows. The team-OS spec needs to either (a) require flow names in message text, (b) migrate critical flows off Gumloop to paradigms with per-bot identity, or (c) accept the audit gap and document.


2. **Slack Workflow Builder is a fifth paradigm I hadn't named.** Educational Content reminder has been firing weekly since Dec 2024. Native Slack, no code, no commit history. Worth a separate inventory pass — there are likely more.


3. **Helen has TWO bot identities for herself.** `B05PNPUDJNS` (app A0F827J2C, an old Zapier 'donald' bot) and `B09J9S88C3D` (Gumloop app, posts AS Helen). The auth confusion from Feb 13 is a real architectural issue — Gumloop's personal-API-key model lets flows impersonate humans.


4. **Member-built personal apps are a parallel pattern.** Akshita's Assistant, Anennya's bot, Maninder's bot, Simi's bot, Carolyn Roth (B08QFEEE6BS) — members deploy their own Slack apps. This is bottom-up federation already happening, just not captured anywhere central.


5. **Polly poll bot (B06451SB6RJ) exists in WDAI** — third-party integration for voting/polls. Used in event scheduling.


6. **WDAI Marketing Content Calendar bot is the paradigm-4 reference fully operational.** Posts daily-generated event approval cards into team-marketing-content-calendar. The `wdai-marketing` repo's daily 6am GitHub Action firing into Slack. This is the team-OS pattern already shipping in one pillar.


7. **'WDAI Scheduler' (B091451E5G8) on #marketing-content-calendar** — separate bot from Marketing Content Calendar bot. Suggesting time slots for meetings. Another distinct paradigm-4 flow.


8. **Many channels have NO bots.** All geo-* channels are pure member chatter. All topic-* channels (chatgpt/gemini/copilot/lovable/etc.) are pure discussion. Member-facing channels mostly bot-free. **The bot ecosystem is concentrated in: team-* private channels, ops/devops channels, automation-test, member-bot-test channels, marketing channels, programs channels.**


## Channels NOT read (low priority deferred)


Bolt hackathon team channels (10x boltteam-*, bolt-hack-* — short-lived hackathon teams, low bot signal expected): boltteam-subscriptions, boltteam-moodfood, boltteam-potluck, boltteam-contract-evolution-engine, boltteam-meno, boltteam-aipowereditinerary, boltteam-nextwage, boltteam-couples_finance, bolt-hack-vote-vibe, bolt-hack-waste-wizard


UK hackathon team channels (5x uk-hackathon-*): uk_hackathon_leads, uk-hackathon-ai-coach-money, uk-hackathon-gp-appt, uk-hackathon-slt-access, uk-hackathon-moving-assistant


Personal/family channels (private to Helen): helen-shawn-womendefiningai, family-ops


Single-person test channels: weather, recipes, leads, content-tracker, new-member-troubleshooting, speed-networking-pilot, network-gies, women-slackers, sf-east-bay-dining-group, geo-miami(partial), geo-pittsburgh(partial), geo-austin(partial), martha-gumloop-agent(partial)


Verdict: deferring these is safe for Pass 1; they're low-signal for federation architecture.
