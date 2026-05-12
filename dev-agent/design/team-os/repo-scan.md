
## weekly-wdai-report

**Top-level:** `.gitignore, .nojekyll, CNAME, dashboard_template.html, index.html`

_(no readme)_


## wdai-foundation-platform

**Top-level:** `.claude/, .github/, .gitignore, .playwright-mcp/, CLAUDE.md, README.md, docs/, packages/, web/`

```
# Women Defining AI - Foundation Platform

Join our community of women and nonbinary leaders going from zero to building with AI.

A Next.js membership platform with Stripe subscriptions, member directory, resource library, and Luma events integration.

**Status:** Production-Ready MVP ✅

---

## 🚀 Quick Start

### Prerequisites
- Node.js 22+
- PostgreSQL (Supabase)
- API keys: Clerk, Stripe (test mode), Luma

### Installation (~10 minutes)

```bash
# 1. Navigate to web directory (monorepo structure)
cd web

# 2. Install dependencies
npm install

# 3. Set up environment
cp .env.example .env.local
# Edit .env.local with your API keys (see Configuration below)

# 4. Set up database
npm run db:push        # Push Prisma schema
npm run db:seed        # Seed test data

# 5. Start dev server
npm run dev
```

Visit http://localhost:3000

**Note:** This is a monorepo. The main application lives in `/web/`. All commands should be run from the `web/` directory.

---

## ⚙️ Configuration

### Required Environment Variables

```bash
# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# Supabase Database
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...
DATABASE_URL=postgresql://...6543/postgres?pgbouncer=true
DIRECT_URL=postgresql://...5432/postgres

# Stripe (create 3 products: Monthly $10, Annual $100, Donor $300)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_STRIPE_PRICE_MONTHLY=price_...
NEXT_PUBLIC_STRIPE_PRICE_ANNUAL=price_...
NEXT_PUBLIC_STRIPE_PRICE_DONOR=price_...

# Luma Events
LUMA_API_KEY=...
LUMA_TARGET_CALENDAR_ID=cal-...
LUMA_BASE_URL=https://public-api.luma.com

# Vimeo (optional - for video thumbnails)
VIMEO_TOKEN=...

# Vercel Blob Storage (for file uploads)
# Get token from: Vercel Dashboard → Storage → Create Blob Store → Settings → Read-Write Token
BLOB_READ_WRITE_TOKEN=...
```


## wdai-marketing

**Top-level:** `.agent/, .env.example, .github/, .gitignore, BUGS.md, MEMORY.md, NEXT.md, PROJECT_HISTORY.md, PROJECT_ROADMAP.md, README.md, TESTING_GUIDE.md, TESTING_PLAN.md, app/, archive/, docs/, meeting-minutes/, package-lock.json, package.json, public/, skills/, tools/, tsconfig.json, vault/, vercel.json`

```
# WDAI Marketing Vault

> This repository is the context vault and tooling layer for WDAI's marketing team. Everything Claude Code needs to do marketing work — brand identity, leader voices, promo workflows, content infrastructure — lives here.

This is the **single source of truth** for how WDAI communicates. When starting a marketing task in Claude Code, load the relevant context from this vault first.

---

## Vision

**Fully automated marketing pipeline:**

```
Luma event created/updated
  → calendar syncs automatically (GitHub Actions, daily)
  → Slack notifies #team-marketing-content-calendar with promo plan + calendar link
  → team approves plan & generates copy in the interactive calendar UI
  → AI drafts channel-specific copy (LinkedIn, email, Slack)
  → approved copy auto-publishes to Mailchimp (LinkedIn is manual copy-paste)
```

No manual copy drafting. No chasing approvals. Every WDAI event gets consistent, on-brand promotion with minimal human overhead.

---

## How It Works

The system runs autonomously — no one needs to open Claude Code for the pipeline to operate. CC is the *build tool*; GitHub Actions and Vercel are the *runtime*.

```
[1] GitHub Actions (daily, 6am UTC)
     → polls Luma API for new/changed events
     → updates vault/content-calendar.md + .html
     → posts Slack notification with promo plan + calendar link
          ↓ HUMAN TOUCHPOINT 1a: team opens calendar → Needs Approval tab (Phase 8 ✅ 2026-05-05)

[1b] Plan approval in calendar UI (Phase 8 ✅ 2026-05-05)
     → "Approve Plan" button on each pending event → calls /api/approve-plan
     → updates vault/status/{luma_id}.yaml to approved
          ↓ proceeds to [2]

[2] Copy generation (Phase 5 ✅ complete, 2026-05-01)
     → loads voice guides from vault/ as AI context
     → calls Anthropic API to draft channel-specific copy
     → stores drafts in vault/promos/<event-id>/
     → DMs each responsible leader with calendar link
          ↓ HUMAN TOUCHPOINT 2: each leader clicks link → edit, approve, or schedule in interactive UI

[3] Auto-publish (Phase 6 ✅ complete)
     → posts approved copy to WDAI LinkedIn org page (UGC API)
     → creates Mailchimp campaign drafts with email content
     → CLI: npm run calendar:publish -- --event <id> [--all] [--dry-run] [--channel <channel>]

[4] Vercel (live at https://wdai-marketing.vercel.app)
     → Interactive calendar UI: 4 tabs (By Date, By Event, Needs Approval, How to Edit)
       - **Needs Approval tab** (Phase 8): pending events + "Approve Plan" button per event
       - **By Event tab**: full channel plan per event + inline copy drafts (edit, approve, schedule, unschedule)
     → API endpoints: /api/save-copy, /api/update-status, /api/approve-plan (Phase 8), /api/slack/interactions
     → Slack notifications link directly to calendar UI (no Slack buttons; user approves in calendar)
     → 277 passing tests, 4 skipped (live API tests)
```

**The two human touchpoints are the only manual steps.** Everything before and after is automated.

---

## Ad-Hoc CC Usage (for one-off marketing tasks)

The vault/skills are also useful when you want to draft something manually — a one-off LinkedIn post, a speaker bio, an announcement. Load the relevant context into a CC or Cowork session:

**For a cohort launch:**
```
Load vault context in this order:
1. /vault/brand-guidelines.md
2. /skills/wdai-brand/SKILL.md
3. /skills/wdai-promo-programmatic/SKILL.md
4. /skills/wdai-promo-programmatic/ai-foundations.md (if AI Foundations cohort)
```

**For event/milestone promotion:**
```


## mailchimp-cc

**Top-level:** `.claude/, .env.example, .github/, .gitignore, CLAUDE.md, CONTRIBUTING.md, README.md, __tests__/, assets/, biome.json, configs/, content/, docs/, package-lock.json, package.json, runbooks/, scripts/, src/, tsconfig.json`

```
# WDAI Cohort Email Automation

Automates the creation, scheduling, and management of AI Foundations cohort emails in Mailchimp. Used by the Women Defining AI ops team to launch and run multi-week email courses.

## What this does

This tool manages the full lifecycle of cohort email campaigns:

- **Creates 12-17 email campaigns** per cohort (pre-kickoff + daily lessons) in Mailchimp
- **Sends to enrolled members** via the Cohort - Active tag in Mailchimp
- **Generates per-day callout boxes** (live session reminders, recap links)
- **Creates Google Calendars** with live session events for learners to subscribe to
- **Previews all emails locally** in the browser before anything touches Mailchimp
- **Updates campaigns mid-cohort** (e.g., adding recap recording links after each live session)

Everything runs through Claude Code with built-in safety checks: dry runs, confirmation prompts, and marker validation to prevent broken emails from going out.

## Programs supported

| Program | Lessons | Duration | Live sessions | Skill |
|---------|---------|----------|---------------|-------|
| AI Basics | 15 | 3 weeks (Mon-Fri) | 6 (Mon/Thu) | `/new-basics` |
| AI Intermediate | 10 | 2 weeks (Mon-Fri) | 4 (Mon/Thu) | `/new-intermediate` |
| AI Advanced | 15 | 3 weeks (Mon-Fri) | 9 (Mon/Wed/Fri) | `/new-advanced` |

Each program also includes 2 pre-kickoff emails sent before the course starts.

## Guided cohort launch (recommended)

The easiest way to launch a new cohort is with the interactive skills in Claude Code. Type one of:

- **`/new-basics`** — walks through creating an AI Basics cohort
- **`/new-intermediate`** — walks through creating an AI Intermediate cohort
- **`/new-advanced`** — walks through creating an AI Advanced cohort

Each skill guides you through the full process:

1. **Gather details** — start date, cohort name, live session schedule
2. **Generate config** — creates a YAML config with all settings and callouts
3. **Create Google Calendar** — generates subscribe links for learners
4. **Preview emails** — opens all emails in the browser for review
5. **Iterate** — make edits and re-preview until everything looks right
6. **Create campaigns** — pushes to Mailchimp as drafts
7. **Schedule** — schedules campaigns that are ready (recap-dependent ones stay as drafts)

## One-off actions

Beyond full cohort launches, the tool supports a range of standalone operations:

### Check cohort status
See all campaigns for a cohort — scheduled, sent, or draft:
```
cohort status --tag <tag>
```

### Update campaigns with recap links
After a live session, add the recording and transcript URLs to the next day's email:
```
campaign update --tag <tag> --set RECAP_RECORDING_1=https://... --set RECAP_TRANSCRIPT_1=https://... --yes
```

### Preview specific campaigns
Preview what emails look like with proposed changes before applying them:
```
campaign preview --tag <tag> --set RECAP_RECORDING_1=https://...
```

### Audit campaigns for hardcoded values
Find values in campaign HTML that should be turned into configurable markers:
```
campaigns audit --tag <tag>
```

### Create a live session calendar
Generate a public Google Calendar learners can subscribe to:
```
cohort create-calendar --config configs/<cohort>.yaml --yes
```

### Capture email content from Mailchimp
```


## FamilyOS

**Top-level:** `.gitignore, BOOTSTRAP.md, README.md, SETUP-CHECKLIST.md, skills/, workspace/`

```
# FamilyOS

**A household manager that runs inside Claude Cowork.**

Morning briefs. School email triage. Meal planning. Shopping lists. Home maintenance. Helper payments. And a weekly review that makes the whole system smarter over time. No coding required.

> Built on Claude Cowork's native scheduler, connectors, and file system. Inspired by [tradclaw](https://github.com/ChatPRD/tradclaw) and [clawchief](https://github.com/snarktank/clawchief).

---

## UPDATE ON COWORK CONNECTOR LIMITATIONS TO KNOW FOR FAMILYOS

Cowork and the Claude connectors are powerful, but each one has rough edges you'll hit in household use. Here's the short list of what bites first — full detail and workarounds in `workspace/TOOLS.md`.

### Slack (text-only)

- **Photos aren't readable.** Pantry/fridge/freezer/receipt/school-flyer photos dropped in the household inbox are invisible to every scheduled job. Save recurring inventory photos to `workspace/resources/pantry/photos/` (filename pattern `<location>-YYYY-MM-DD.jpg`), or attach one-offs directly in a Cowork session. The hourly inbox job logs image-referencing messages as `[NEEDS-REVIEW]` so nothing silently disappears.
- **No DMs.** The connector operates on channels the bot has been invited to — direct messages don't reach it.
- **Private channels must explicitly invite the Claude bot** before the connector can see them.
- **Thread and mention history is capped** (roughly last 20–50 messages). Don't rely on deep Slack history for context.

### Gmail

- **Attachments (PDFs, images) aren't readable.** School permission slips, field-trip forms, flyers, and receipts received by email won't parse. Save the file locally and attach it in a Cowork session, or forward the PDF to yourself and open it directly.
- **Drafts can't include attachments, and there's no send-draft tool.** Claude can write an email body but can't end-to-end send a reply with a file attached.
- **One Gmail account per connector** — no simultaneous spouse+personal inboxes in the same session.
- **Default search depth is about 3 years back** — if you ask about older threads, widen the window in the prompt.

### Google Calendar

- **Multi-calendar (shared family + personal) is spotty.** The connector tends to default to the primary calendar. If your family events live on a shared calendar, either make it the primary on the Google account Cowork is connected to, or name the calendar explicitly in prompts.
- **Event attachments (Drive links on events) aren't readable.**
- **Timezone follows the calendar's TZ setting, not the OS.** If you travel or have calendars in different zones, set TZ explicitly when asking about times.

### Cowork scheduled tasks

- **Desktop-bound.** Jobs only fire while Claude Desktop is running and the computer is awake. A closed laptop at 7 AM means the morning brief waits until you open it.
- **Permission "Always allow" can regress.** After a Claude Desktop update or occasionally on its own, scheduled runs re-prompt for folder/tool approval and silently stall. If a job stops firing, go to Cowork → Scheduled, click Run now, and re-approve. Worth doing after every Claude Desktop update.

### Local files (your FamilyOS working folder)

- **Don't keep `FamilyOS/` in a cloud-synced folder.** On macOS, anything under `~/Library/CloudStorage/` (iCloud Drive, OneDrive, Google Drive) fails to mount as a Cowork working folder. On Windows, OneDrive's on-demand "placeholder" files break the Cowork sandbox. If your Mac has iCloud Desktop & Documents sync on (the default), putting FamilyOS in `~/Documents/FamilyOS` will silently break — use `~/FamilyOS` or `~/Developer/FamilyOS` instead.
- **PDFs cap at ~30 MB and ~100 pages** for visual analysis. Large scanned PDFs need to be split.

---

### A note on all of this

These guardrails exist *for now*. Cowork and every connector are improving on the scale of **weeks, not months** — capabilities that are missing today are likely to ship in the next release. This repository is the whole point: **keep experimenting**, notice what breaks, and adapt. When something works that didn't before, delete the workaround. When something new breaks, add a note to `workspace/TOOLS.md`. The system bends toward your actual household; the tooling bends toward what's possible.

---

## What it does

FamilyOS runs four jobs automatically and gives you two more on demand.

| Job | When | What it does |
|-----|------|--------------|
| **Morning Brief** | Daily, 7 AM | Posts a 2-minute calendar + urgent email rundown to your Slack inbox |
| **Household Inbox** | Every hour | Reads your Slack drop channel, files notes into the right folder |
| **Evening Memory** | Daily, 9 PM | Reads today's log, writes learnings to memory, clears the slate |
| **Weekly OS Review** | Sundays, 6 PM | Reviews how the week went and proposes system improvements |
| School Triage | On demand | Sweeps Gmail for school emails and triages by urgency |
| Meal Planner | On demand | Builds a weekly dinner plan with a shopping list |

The Slack channel is the key piece. Throughout the day you drop things in — `"add oat milk to the list"`, `"picture day Thursday, need $12"`, `"plumber came, $180, kitchen faucet"` — and the agent files them automatically. Nothing falls through the cracks.

The weekly review is what separates FamilyOS from a static automation. Every Sunday it reads how the week went, identifies what got misfiled or missed, and proposes specific changes to improve the system. It proposes — you decide what to apply.

---

## How the system works

```
Your day
   │
   ├── Drop notes → #family-inbox (Slack)
   │                      │
   │              Hourly inbox job
   │                      │
```


## wdai-lumabot

**Top-level:** `.cursor/, .env.example, .github/, .gitignore, README.md, biome.json, docs/, package-lock.json, package.json, railway.json, src/, tsconfig.json`

```
# Lumabot - Internal Slack Luma Integration

Lumabot is a Slack bot that integrates with the Luma (lu.ma) event platform to streamline event creation, guest management, and community engagement for the Women Defining AI community. It is built with a focus on performance, reliability, and maintainability, and is deployed on Railway.

## Core Features

| Feature                  | Description                                                                                                                                                                                            | Key Files                                             |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------- |
| **Event Creation**       | A `/luma-create-event` slash command opens a Slack modal for creating events. It adds co-hosts in parallel and handles "user already a host" errors gracefully.                                          | `src/slack/commands.ts`, `src/slack/actions.ts`       |
| **Automatic Guest Approval** | A scheduled job (`node-cron`) periodically fetches **future events** (6-month window), uses Luma's server-side filters to get **pending guests**, and approves them against a cached list of active Airtable members. Includes Slack notifications for task status. | `src/scheduler/approveGuests.ts`                      |
| **Weekly Event Digest**  | A scheduled job posts a formatted, interactive summary of the upcoming week's events to a designated Slack channel.                                                                                    | `src/scheduler/fridayDigest.ts`                       |
| **App Home Dashboard**   | The bot's App Home tab provides a dynamic dashboard showing upcoming events, a link to the full Luma calendar, and a "Create Event" button for authorized users.                                        | `src/slack/home.ts`                                   |

## Technical Architecture

This bot is architected to be resilient and efficient, relying on several key patterns:

1.  **Centralized API Clients**: All interactions with external services (Luma, Airtable, Slack) are handled through dedicated, promise-based client classes. The `LumaClient` (`src/luma/client.ts`) includes built-in retry logic and rate-limiting.

2.  **Rate Limiting & Concurrency**: The [`p-limit`](https://github.com/sindresorhus/p-limit) library is used extensively to control concurrency and prevent overwhelming external APIs. This is crucial for operations that involve multiple parallel API calls, such as adding co-hosts or approving guests.

3.  **Multi-Layered Caching**: An in-memory cache (`src/cache/index.ts`) is used to minimize redundant API calls:
    - **Airtable Members**: Active member emails are cached for 5 minutes to make guest approval checks near-instantaneous.
    - **Slack User Info**: User permissions and group memberships are cached to make authorization checks extremely fast.

4.  **Robust Error Handling**:
    - Centralized `notifyError` and `notifySuccess` functions send detailed alerts to a DevOps channel for task status and failures.
    - Comprehensive error catching with detailed logging at every stage of processing.
    - Common, predictable errors (e.g., trying to add an existing co-host) are caught gracefully, logged, and do not crash the application.
    - Separate concurrency limiters prevent deadlocks in nested async operations.

5.  **Configuration & Constants**:
    - **Environment Variables**: All secrets (API keys, tokens) and environment-specific IDs (channels, user groups) are managed via a `.env` file and loaded through `src/config/index.ts`.
    - **Application Constants**: All non-sensitive, configurable values are centralized in `src/constants.ts`. This file is crucial for tuning the bot's behavior.

## Understanding `constants.ts`

For new developers, `src/constants.ts` is the primary file for tuning the bot's operational parameters without changing code.

| Constant Group  | Purpose                                                                                                                                    | Example                                          |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------ |
| `TIME_CONSTANTS`  | Defines cache lifetimes (TTLs) and `cron` schedules. Adjust these to change how often data is refreshed or how frequently jobs run.       | `CACHE_TTL_USER_PERMISSIONS: 10 * 60 * 1000` (10 minutes) |
| `RATE_LIMIT`      | Controls the bot's API usage. `*_CONCURRENT_REQUESTS` sets the maximum number of parallel API calls to an endpoint. Lower this if you hit rate limits. | `LUMA_CONCURRENT_REQUESTS: 3`                      |
| `PAGINATION`      | Defines page sizes for API queries and sets safety limits (`MAX_*_PAGES`) to prevent infinite loops when fetching paginated data.       | `LUMA_GUEST_PAGE_LIMIT: 100`                     |
| `UI_CONSTANTS`    | Governs UI elements, such as the number of events to display on the App Home.                                                              | `APP_HOME_MAX_EVENTS: 20`                          |

## Project Evolution & Key Refactors

The bot has undergone significant refactors to improve performance and reliability:

-   **Parallelization**: Moved from sequential operations (e.g., adding co-hosts one-by-one) to a parallel, concurrent model using `Promise.all` and `p-limit`.
-   **API Discovery**: Initially, we assumed the Luma API supported batch guest approvals. Through testing and error analysis, we discovered it only supports single-guest updates and refactored the code accordingly.
-   **Dependency Management**: Resolved a critical runtime crash (`ERR_REQUIRE_ESM`) by downgrading the `p-limit` dependency to a CommonJS-compatible version (v5).
-   **Deadlock Prevention** (August 2025): Fixed a critical deadlock in guest approval by using separate limiters for event processing and guest approvals.
-   **Extended Event Window** (August 2025): Increased approval window from 3 to 6 months to catch events scheduled further in advance.
-   **Enhanced Observability** (August 2025): Added comprehensive logging and Slack notifications for approval task status, including success stats and error reporting.

## Debugging & Monitoring

### Guest Approval Task
The approval task runs every 12 hours and can be triggered manually with `/luma-run-approval-task`. Key debugging points:

-   **Logging Levels**: The task includes detailed logging at each stage:
    - Event fetching and processing
    - Guest iteration and filtering  
    - Individual approval attempts
    - Success/failure statistics

-   **Slack Notifications**: The DevOps channel receives:
    - Success notifications with approval statistics
    - Error notifications with stack traces
    - Missing configuration warnings (e.g., `DEV_OPS_CHANNEL_ID`)

-   **Common Issues**:
    - **No approvals happening**: Check if events are within the 6-month window
    - **Task hanging**: Look for "All events scheduled" log - if missing, check for deadlocks
    - **No Slack notifications**: Ensure `DEV_OPS_CHANNEL_ID` environment variable is set

### Environment Variables
Required for full functionality:
```


## wdai-admin

**Top-level:** `.claude/, .env.example, .github/, .gitignore, AIRTABLE_INTEGRATION.md, CLAUDE.md, README-MEMBERBOT.md, README-WIXSYNC.md, README.md, biome.json, docs/, package.json, scripts/, src/, tsconfig.json`

```
# WDAI Admin Services

A collection of backend services built for the Women Defining AI Slack community to help manage member data across multiple systems (Wix, Slack, and Airtable).

## Project Overview

This repository contains two main services:

1. **MemberBot Service** - Manages Slack member data and synchronizes it with Airtable
2. **WixSync Service** - Processes Wix webhooks for purchases and cancellations

For detailed documentation on each service:
- [MemberBot Documentation](./README-MEMBERBOT.md)
- [WixSync Documentation](./README-WIXSYNC.md)

## Features

- Fast and lightweight web server using Fastify
- TypeScript for type safety
- API documentation with Swagger
- Code quality tools with Biome (linting, formatting)
- Hot reloading for development
- **Supabase PostgreSQL** for primary data storage (via raw `pg` client)
- **Airtable** integration for legacy data (migration period)
- Slack integration for user information and messaging
- **Stripe webhook** processing for subscription data
- Wix webhook processing for legacy subscription data (deprecated)
- Standardized API response formats for consistent client experience
- Centralized error handling and logging
- Circuit breakers for external service resilience

## Getting Started

### Prerequisites

- Node.js (v20 or higher)
- npm or yarn

### Installation

1. Clone the repository
2. Install dependencies:

```bash
npm install
# or
yarn install
```

### Development

Start the development server with hot reloading:

```bash
# Run the memberbot service (Slack integration)
npm run dev:memberbot

# Run the Wix webhook service
npm run dev:wixsync
```

The server will be available at http://localhost:3000.

### Build

Compile the TypeScript code to JavaScript:

```bash
npm run build
# or
yarn build
```

### Production

Start the production server:

```bash
# Run the memberbot service
npm run start:memberbot
```


## market-challenge-simulator

**Top-level:** `.gitignore, LICENSE, README.md, docs/, package-lock.json, package.json, postcss.config.js, src/, tailwind.config.js, tsconfig.json`

```
# Market Challenge Simulator

[**Try the live simulator here!**](https://market-challenge-simulator.vercel.app)

A Next.js application that enables business strategists to evaluate new market opportunities by simulating potential solutions and collecting persona feedback using a structured, LLM-powered simulation process.

![Main Application Screen](docs/images/mainscreenexample.png)

## Overview

The Market Challenge Strategy Simulator helps businesses explore different approaches to market challenges by:
- Generating multiple potential solutions with varied risk profiles
- Creating detailed market personas (current audience and potential new audiences)
- Simulating realistic persona feedback and risk analysis for each solution
- Calculating feasibility and return scores based on market readiness and resource requirements
- Presenting solutions with authentic first-person quotes from simulated personas

## Features

- AI-powered market analysis using GPT-4o
- Structured prompt templates with delimiter tags for consistent data extraction
- Detailed persona generation with demographic details and adoption likelihood
- Risk analysis with specific breakdowns (market readiness, resource requirements, etc.)
- Authentic first-person quotes from personas that reflect their background and priorities
- Interactive results dashboard with feasibility and return scoring
- Real-time loading state showing interim results as they are generated:

  ![Simulation Loading State](docs/images/loadingstate.png)

- Detailed final report summarizing solutions and feedback:

  ![Final Simulation Report](docs/images/finalreportexample.png)

## Tech Stack

- Next.js
- TypeScript
- Tailwind CSS
- OpenAI API integration
- Structured extraction framework for LLM-generated data

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/WomenDefiningAI/market-challenge-simulator.git
cd market-challenge-simulator
```

2. Install dependencies:
```bash
npm install
```

3. Set up your OpenAI API key:
The application uses a client-side approach where users provide their own API keys. No environment variables are required for the OpenAI integration.

4. Run the development server:
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## How It Works

The simulator operates in three main stages:

1. **Solution Generation**: Creates 5 distinct business solutions for the market challenge with varying approaches and risk levels.

2. **Persona Creation**: Develops 6 detailed market personas (3 from current audience, 3 from potential new audiences) with specific demographic details and characteristics.

3. **Feedback Analysis**: For each solution, generates comprehensive risk analysis and authentic first-person feedback from each persona.

The structured output uses delimiter tags (e.g., `[PERSONA_START]`, `[SOLUTION_ANALYSIS_START]`) to ensure consistent parsing and display of the simulation results.

## Development

- `npm run dev` - Start development server
- `npm run build` - Build for production
```


## github-intro-fun

**Top-level:** `README.md, anennya_test.md, github-101.md`

```
# GitHub Intro Fun

Welcome to this repository! This is a practice repository for learning GitHub basics.

## About This Repository

This repository is designed to help you learn fundamental GitHub operations including:
- Cloning repositories
- Making updates and commits
- Pushing changes to GitHub
- Working with public and private repositories

## Join Our Office Hours!

We'll be using this repository during our **Intro to GitHub Office Hours** event. Join us to learn:

- Setting up a repository to experiment in
- Understanding public vs private repositories
- Cloning and updating repositories
- And much more!

**📅 [Register for the event here](https://luma.com/z56kmlpi)**

The event is hosted by Women Defining AI: Community Calendar, and most of the hour will be dedicated to answering your questions. If you've never created a GitHub account, we'll help with that too!

## Getting Started

1. Clone this repository to your local machine
2. Make some changes to the files
3. Commit and push your changes
4. Practice, practice, practice!

## Resources

📚 **[GitHub 101 Guide](github-101.md)** - A comprehensive beginner-friendly guide covering core concepts, common commands, workflows, and best practices.

## Files in This Repository

- `anennya_test.md` - A test markdown file with some fun content about GitHub
- `github-101.md` - Beginner's guide to GitHub concepts and commands

---

Happy coding! 🚀
```


## claude-code-skills

**Top-level:** `.gitignore, LICENSE, README.md, agents/, commands/, skills/`

```
# Claude Code Resources Collection

A collection of Skills, Commands, and Agents to help you get more out of Claude Code.

## What's Included?

This repository provides three types of Claude Code resources:

### Skills
Add-ons that teach Claude new capabilities. Each skill is a folder containing instructions and resources that Claude can use when needed.

### Commands
Quick shortcuts that start with `/` to run common tasks. Type `/command-name` to instantly trigger a specific workflow.

### Agents
Specialized helpers with focused expertise. Claude automatically brings in the right agent when it matches what you're trying to do.

## Repository Structure

This repository is organized by resource type:

```
claude-code-resources/
├── README.md
├── LICENSE
├── skills/              # Claude Code Skills
│   ├── skill-builder/
│   ├── skill-contributor/
│   ├── frontend-ui/
│   ├── ui-ux-audit/
│   ├── code-refactoring/
│   ├── code-reviewer/
│   ├── shownotes-generator/
│   └── feature-orchestrator/
├── commands/            # Slash Commands
│   ├── improve-code.md
│   ├── plan-feature.md
│   └── README.md
└── agents/              # Custom Subagents
    ├── prompt-engineer.md
    └── README.md
```

## Available Skills

### 🛠️ Skill Builder

**Status**: ✅ Available
**Directory**: `skills/skill-builder/`
**Purpose**: A meta-skill that helps you create well-structured Claude Code Skills

**Features**:
- Step-by-step skill creation workflow
- Templates for common patterns
- Validation tools
- Best practices guidance
- Progressive disclosure strategies

[**View Documentation →**](skills/skill-builder/README.md)

**Quick Install**:
```bash
git clone https://github.com/WomenDefiningAI/claude-code-skills.git
cp -r claude-code-skills/skills/skill-builder ~/.claude/skills/
```

---

### 🤝 Skill Contributor

**Status**: ✅ Available
**Directory**: `skills/skill-contributor/`
**Purpose**: Guides contributors through adding new skills to the repository via Pull Request

**Features**:
- Step-by-step PR submission workflow
- Automated validation checks
- README.md documentation updates
- Git branch and commit automation
- Pull Request template generation
```


## wdai-hive

**Top-level:** `.github/, .gitignore, .mcp.json, Dockerfile, LICENSE, README.md, SETUP.md, biome.json, docker-compose.yml, env.example, package-lock.json, package.json, scripts/, src/`

```
# WDAI Hive 🐝

**AI Engagement & Play Tracker Slack Bot**

WDAI Hive is a Slack bot that encourages regular AI experimentation and tracks community engagement with AI tools. It sends weekly check-ins to community members, collects structured feedback about AI activities, and provides insights through an admin dashboard.

## 🎯 Features

### For Community Members
- **Weekly DM Check-ins**: Automated friendly reminders asking "Did you play with AI this week?"
- **Structured Responses**: Quick selection from predefined categories and tools
- **Custom Input**: "Other" options for unique activities and tools
- **Privacy Controls**: Opt-out options and data retention preferences

### For Admins
- **Data Export**: CSV exports with audit logging
- **API Access**: Direct database access for analytics

## 🏗️ Architecture

- **Backend**: Node.js with Slack Bolt framework
- **Database**: Supabase (PostgreSQL) with encryption
- **Deployment**: Docker containerization

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Slack App credentials
- Supabase project
- Docker (optional)

### 1. Clone & Install
```bash
git clone <repository-url>
cd wdai-hive
npm run install:all
```

### 2. Environment Setup
Create a `.env` file in the root directory:
```env
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_APP_TOKEN=xapp-your-app-token

# Supabase Configuration
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# App Configuration
PORT=3000
NODE_ENV=development

# Channel Configuration
TARGET_CHANNEL_ID=C088PDC4VRS
```

### 3. Database Setup
Run the database migration script:
```bash
node scripts/setup-database.js
```

### 4. Start Development
```bash
# Start the bot
npm run dev

```

### 5. Deploy with Docker
```bash
npm run docker:build
npm run docker:run
```
```


## claudecode-writer

**Top-level:** `.claude/, CLAUDE.md, CONTRIBUTING.md, LICENSE, README.md, context/, drafts/, rawnotes/, research/`

```
# Claude Code Writing System

## What This Template Does for Claude Code Users

**This template turns Claude Code into your personal content creation system** - a smart writing assistant that learns your unique voice and automatically adapts your ideas for every platform you use.

Think of it as having a team of specialized writers who all know exactly how you write and what your audience expects. You provide the idea, and the system handles everything from research to platform-specific optimization.

## How It Enables You to Build a Writing System

The template provides a complete, ready-to-use architecture that works immediately:

1. **Voice Learning**: Add a few examples of your existing writing, and Claude learns your style
2. **Smart Research**: Tell it your favorite sources, and it checks them first for relevant insights
3. **Automated Workflow**: Simple commands like `/research` and `/write` handle the entire process
4. **Platform Specialists**: Built-in agents that know exactly how to optimize for LinkedIn, newsletters, and social media

No coding required. No complex setup. Just add your examples and start writing.

## The Magic Workflow

1. **Capture Ideas**: Drop unorganized thoughts, voice notes, and fragments into `/rawnotes`
2. **Extract Themes**: `/extract-themes` finds patterns and develops coherent angles from your raw notes
3. **Research Once**: `/research [your topic]` finds trends, data, and unique angles from your trusted sources
4. **Write Once**: `/write` creates a comprehensive article in your voice
5. **Publish Everywhere**: Specialized agents automatically transform your article into:
   - LinkedIn posts with professional hooks and engagement drivers
   - Newsletter sections with compelling subject lines and personal touches
   - Twitter threads that maximize shares and conversations
   - Podcast Q&A scripts that sound naturally conversational

**Why This Matters:**
- **Time Savings**: What used to take hours (adapting content for each platform) now takes seconds
- **Consistency**: Your voice stays authentic across all platforms
- **Quality**: Each piece is optimized for its specific platform's best practices
- **Learning System**: The more you use it, the better it understands your style

**Perfect For:** Content creators, professionals building thought leadership, newsletter writers, or anyone tired of manually reformatting content for different audiences.

## Quick Start

### 1. Get This Template
1. Go to this repository on GitHub
2. Click the green "Use this template" button (or fork the repository)
3. Name your new repository (e.g. "my-writing-workspace")
4. Clone it to your computer:
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
   cd YOUR-REPO-NAME
   ```

### 2. Install Claude Code

Visit the official site: [anthropic.com/claude-code](https://www.anthropic.com/claude-code)

**Mac:**
```bash
# Install via Homebrew
brew install anthropics/claude/claude-code

# Or download directly
curl -fsSL https://claude.ai/install.sh | sh
```

**Windows:**
1. Download the installer from [claude.ai/code](https://claude.ai/code)
2. Run the installer and follow the prompts
3. Open Command Prompt or PowerShell

**Setup:**
```bash
# Login to your Anthropic account
claude auth login

# Navigate to your writing workspace
cd path/to/your/writing-workspace

# Start Claude Code
claude
```
```


## reading-story-creator

**Top-level:** `.cursor/, .github/, .gitignore, README.md, biome.json, components.json, docs/, eslint.config.mjs, next.config.ts, package-lock.json, package.json, postcss.config.mjs, public/, src/, tsconfig.json`

```
# Reading Story Creator

Try it live: [reading-story-creator.vercel.app](https://reading-story-creator.vercel.app/)

This is a Next.js web application designed to help parents and educators create simple, illustrated stories for young children (Kindergarten, 1st Grade, and 2nd Grade reading levels).

**Main input form**

![Input Page Screenshot](public/input-page.png)


**Example generated story panel**

![Story Panel Screenshot](public/story-panel.png)



## Core Functionality

*   **Story Generation:** Creates custom 5-panel stories with illustrations based on a user-provided topic/character and selected reading level (K, 1st, or 2nd grade).
*   **Input:** Accepts text input for the story idea. Voice input via Web Speech API is available in supported browsers.
*   **API Integration:** Uses the Google Gemini API for generating story text and illustrations (requires user-provided API key, with a helper modal linking to Google AI Studio for key generation).
*   **Vocabulary Control:** Guides story generation using grade-appropriate vocabulary lists (based on Dolch, Fry, and common high-frequency words) and constraints for sentence length and new word introduction.
*   **Interface:** Simple, mobile-friendly UI.
*   **Output:**
    *   Displays the generated story panel-by-panel.
    *   Generates a printable PDF with all panels.
*   **Footer:** Includes links to the Women Defining AI community and the project's GitHub repository.

## Getting Started

1.  **Prerequisites:** Node.js (v18+ recommended), npm/yarn/pnpm.
2.  **Clone the repository:**
    ```bash
    git clone https://github.com/WomenDefiningAI/reading-story-creator.git
    cd reading-story-creator
    ```
3.  **Install dependencies:**
    ```bash
    npm install
    # or yarn install / pnpm install
    ```
4.  **Environment Variables (Optional):** While the app allows entering the Google Gemini API key directly (stored in local storage), you can optionally create a `.env.local` file for development if preferred (note: direct local storage use is the primary method currently implemented).
    ```
    # .env.local
    # NEXT_PUBLIC_GEMINI_API_KEY=YOUR_API_KEY_HERE
    ```
5.  **Run the development server:**
    ```bash
    npm run dev
    ```
6.  **Open your browser:** Navigate to <http://localhost:3000>.
7.  **Usage:**
    *   Enter your Gemini API key (use the ' ? ' icon for help).
    *   Select a reading level (Kindergarten, 1st Grade, or 2nd Grade).
    *   Type or speak a story topic (e.g., "A brave little boat finds a friend").
    *   Click "Create Story".
    *   Once generated, view the story and click "Download PDF" to save a print-ready version.

## Project Structure

*   `src/app/`: Main application routes and layout (Next.js App Router).
*   `src/components/`: Reusable React components (UI, form, story elements, layout).
*   `src/hooks/`: Custom React hooks (speech recognition, local storage).
*   `src/lib/`: Utility functions, constants (vocabulary lists/constraints).
*   `src/services/`: API interaction (Gemini, PDF generation).
*   `src/store/`: Zustand state management store.
*   `src/types/`: TypeScript type definitions.
*   `public/`: Static assets.
*   `docs/`: Project documentation.

## Technology Stack

*   Framework: Next.js (App Router)
*   Language: TypeScript
*   Styling: Tailwind CSS
*   UI Components: Shadcn/ui
*   State Management: Zustand
*   Linting/Formatting: Biome.js
*   APIs: Google Gemini (Client-Side), Web Speech API
```


## ai-slackbot

**Top-level:** `.env.example, .github/, .gitignore, LICENSE.md, Procfile, README.md, app/, pyproject.toml, run.py, uv.lock`

```
# Talk to an LLM in Slack (Slackbot template from WDAI)

A Slack bot that uses OpenAI's GPT-4o model to respond to messages, analyze images, process CSV data, and extract information from PDFs.  Originally created for the purposes of enabling more AI experiments in-channel for our Women Defining AI micro-learning program participants, this repo is a templatized version of our Slackbot implementation that is open so that others can build their own AI Slackbot

## 🚀 Getting Started (For Beginners)

If you're new to coding or GitHub, this section will help you get started:

1. **Fork this template**: Click the "Use this template" button at the top of this GitHub page to create your own copy of this repository.

2. **Get your API credentials**: 
   - Create a [Slack App](https://api.slack.com/apps) (Instructions in the "Create a Slack App" section below)
   - Get an [OpenAI API key](https://platform.openai.com/api-keys)

3. **Deploy your bot**: This template is set up for easy deployment on [Railway](https://railway.app/), a hosting platform that doesn't require technical expertise.

4. **Test and enjoy**: Once deployed, invite your bot to a Slack channel and start interacting with it!

Need more detailed instructions? Follow the step-by-step guides in the sections below.

## Features
This template relies on OpenAI APIs for LLM capabiltiies, but you can continue to expand on these capabilities by integrating other LLM and providers for various features.
- **AI-Powered Conversations**: Responds to messages using OpenAI's GPT-4o model
- **Conversation Memory**: Maintains context by tracking conversation history in threads
- **Multi-Modal Capabilities**:
  - **Image Analysis**: Describes and answers questions about images
  - **Image Generation**: Creates custom images using DALL-E 3 based on text prompts
  - **CSV Processing**: Analyzes tabular data shared in CSV format
  - **PDF Extraction**: Extracts and summarizes content from PDF documents
  - **Text File Handling**: Processes plain text files

## Setup and Deployment

### Prerequisites

- **Slack Workspace with Admin privileges**: You need admin access to a Slack workspace to create and install a bot. You can create a free Slack team for testing purposes if needed.
- **OpenAI API Key**: Create an account at [OpenAI](https://platform.openai.com/) and generate an API key
- **Railway account**: Sign up at [Railway](https://railway.app/) for deploying your bot (free tier available)
- **GitHub account**: Required to fork this template and connect with Railway

### Environment Variables

Environment variables are settings that need to be configured for your bot to work. You'll set these up in Railway during deployment:

- `SLACK_BOT_TOKEN`: Your Slack Bot User OAuth Token (you'll get this when creating your Slack App)
- `SLACK_SIGNING_SECRET`: Your Slack App Signing Secret (also provided when creating your Slack App)
- `OPENAI_API_KEY`: Your OpenAI API Key
- `MAX_THREAD_HISTORY` (optional): Maximum number of messages to retrieve from a thread (default: 10)
- `ALLOWED_CHANNEL` (optional): Channel ID where the bot is allowed to respond (if not set, bot works in all channels)
- `LOG_DIR` (optional): Directory where logs will be stored (default: `logs`)
- `LOG_LEVEL` (optional): Minimum log level to record (default: `INFO`)
- `RATE_LIMIT_ENABLED` (optional): Enable or disable rate limiting (default: `true`)
- `USER_RATE_LIMIT_WINDOW` (optional): Time window in seconds for user rate limiting (default: `60`)
- `USER_RATE_LIMIT_MAX` (optional): Maximum number of requests per user in the window (default: `10`)
- `TEAM_RATE_LIMIT_WINDOW` (optional): Time window in seconds for team rate limiting (default: `60`)
- `TEAM_RATE_LIMIT_MAX` (optional): Maximum number of requests per team in the window (default: `100`)

### ⚠️ Security Warning

**IMPORTANT**: Never commit your actual `.env` file or any file containing real API keys, tokens, or secrets to your repository. Only commit the `.env.example` file with placeholder values.

- **API Tokens**: If you accidentally expose your API tokens, immediately rotate them (create new ones and invalidate the old ones) in the respective dashboards.
- **Environment Variables**: Always use environment variables for sensitive information, especially in production.
- **Git Practices**: Make sure `.env` is included in your `.gitignore` file to prevent accidental commits.

### 🔒 Enhanced Security Features

#### PII Redaction in Logs

This bot includes an advanced logging system that automatically redacts personally identifiable information (PII) from log files, including:

- Email addresses
- IP addresses
- Phone numbers
- Social Security Numbers
- Credit card numbers
- API keys and tokens

This prevents sensitive information from being exposed in log files while still providing useful debugging information. All logs are stored in the `logs/bot_activity.log` file by default.
```


## harborai-tedai2024winner

**Top-level:** `.eslintrc.json, .gitignore, .prettierrc, LICENSE, README.md, package-lock.json, package.json, public/, readme/, relay-server/, src/, tsconfig.json`

```
# OpenAI Realtime Console

The OpenAI Realtime Console is intended as an inspector and interactive API reference
for the OpenAI Realtime API. It comes packaged with two utility libraries,
[openai/openai-realtime-api-beta](https://github.com/openai/openai-realtime-api-beta)
that acts as a **Reference Client** (for browser and Node.js) and
[`/src/lib/wavtools`](./src/lib/wavtools) which allows for simple audio
management in the browser.

<img src="/readme/realtime-console-demo.png" width="800" />

# Starting the console

This is a React project created using `create-react-app` that is bundled via Webpack.
Install it by extracting the contents of this package and using;

```shell
$ npm i
```

Start your server with:

```shell
$ npm start
```

It should be available via `localhost:3000`.

# Table of contents

1. [Using the console](#using-the-console)
   1. [Using a relay server](#using-a-relay-server)
1. [Realtime API reference client](#realtime-api-reference-client)
   1. [Sending streaming audio](#sending-streaming-audio)
   1. [Adding and using tools](#adding-and-using-tools)
   1. [Interrupting the model](#interrupting-the-model)
   1. [Reference client events](#reference-client-events)
1. [Wavtools](#wavtools)
   1. [WavRecorder quickstart](#wavrecorder-quickstart)
   1. [WavStreamPlayer quickstart](#wavstreamplayer-quickstart)
1. [Acknowledgements and contact](#acknowledgements-and-contact)

# Using the console

The console requires an OpenAI API key (**user key** or **project key**) that has access to the
Realtime API. You'll be prompted on startup to enter it. It will be saved via `localStorage` and can be
changed at any time from the UI.

To start a session you'll need to **connect**. This will require microphone access.
You can then choose between **manual** (Push-to-talk) and **vad** (Voice Activity Detection)
conversation modes, and switch between them at any time.

There are two functions enabled;

- `get_weather`: Ask for the weather anywhere and the model will do its best to pinpoint the
  location, show it on a map, and get the weather for that location. Note that it doesn't
  have location access, and coordinates are "guessed" from the model's training data so
  accuracy might not be perfect.
- `set_memory`: You can ask the model to remember information for you, and it will store it in
  a JSON blob on the left.

You can freely interrupt the model at any time in push-to-talk or VAD mode.

## Using a relay server

If you would like to build a more robust implementation and play around with the reference
client using your own server, we have included a Node.js [Relay Server](/relay-server/index.js).

```shell
$ npm run relay
```

It will start automatically on `localhost:8081`.

**You will need to create a `.env` file** with the following configuration:

```conf
OPENAI_API_KEY=YOUR_API_KEY
REACT_APP_LOCAL_RELAY_SERVER_URL=http://localhost:8081
```
```
