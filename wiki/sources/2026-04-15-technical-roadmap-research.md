# Technical Roadmap Research

**Date:** 2026-04-15
**Context:** Research for WDAI technical roadmap slide — scaling from 1 dev to volunteer contributors
**Sources:** ProdPad, Atlassian, Aha!, ProductPlan, Amplitude, Product School, airfocus, LaunchNotes

---

## 1. Technical Roadmap vs Product Roadmap

| Dimension | Product Roadmap | Technical Roadmap |
|-----------|----------------|-------------------|
| **Owns** | The "why" and "what" | The "when" and "how" |
| **Audience** | External (customers, partners, execs) | Internal (engineering, ops, IT) |
| **Focus** | Customer problems, features, market fit | Infrastructure, architecture, systems, platforms |
| **Items** | User-facing capabilities and outcomes | Technical enablers, migrations, debt payoff, tooling |
| **Built by** | Product managers | Engineering/tech leads |
| **Level** | Strategic — broad themes and outcomes | Tactical — component, system, and process plans |

**Key insight:** They are two halves of a whole. The product roadmap says "we need real-time notifications for users." The technical roadmap says "we need to implement WebSocket infrastructure and a notification service to enable that." A technical roadmap explains how the technology will evolve to support the product roadmap.

For WDAI specifically: you likely need a **hybrid** — a single roadmap that communicates both the "what we're building for the community" and "the technical platform work that enables it," since stakeholders are both technical and non-technical.

---

## 2. Roadmap vs Backlog/Task List — The Critical Distinction

**A roadmap is NOT:**
- A list of tasks or tickets
- A Gantt chart of deliverables
- A project plan with deadlines
- A feature request list

**A roadmap IS:**
- A strategic communication tool
- A statement of direction and priorities
- A framework for making trade-off decisions
- A living document that changes as you learn

### The Abstraction Hierarchy

```
VISION          "Democratize AI education for women globally"
  |
THEMES          "Developer Experience" / "Community Scale" / "Content Platform"
  |
OUTCOMES        "Contributors can onboard in under 30 minutes"
  |
EPICS           "Contributor onboarding flow" / "Local dev environment setup"
  |
FEATURES        "CLI scaffolding tool" / "Contribution guide"
  |
TASKS           "Write Dockerfile" / "Add ESLint config" / "Create PR template"
```

**What belongs on a roadmap:** Themes and Outcomes (the top 2-3 levels).
**What belongs in a backlog:** Epics, Features, and Tasks (the bottom 3 levels).

The fatal mistake is putting tasks on a roadmap. "Write Dockerfile" is a task. "Containerized development environment for instant contributor onboarding" is a roadmap item.

---

## 3. Now-Next-Later Framework

Invented by Janna Bastow (ProdPad CEO). The key innovation: **replaces fixed dates with commitment levels.**

### Structure

| Column | Commitment | Detail Level | Typical Count |
|--------|-----------|-------------|---------------|
| **Now** | High — validated, in progress | Specific outcomes with clear scope | 2-4 items |
| **Next** | Medium — in/pending discovery | Directional, scope still forming | 3-5 items |
| **Later** | Low — aspirational | Broad themes, may never happen | 3-6 items |

### Rules
- Only "Now" is a commitment. "Next" and "Later" are direction, not promises.
- Items flow left-to-right as they gain clarity and validation.
- Review every ~6 weeks (half a quarter).
- "Later" items may be discarded — that's the point.

### Why This Works for WDAI
- No false precision with dates (you have volunteers, not employees)
- Communicates priorities without making promises you can't keep
- Non-technical stakeholders can understand it immediately
- Forces focus — if everything is "Now," nothing is

---

## 4. Outcome-Based vs Output-Based Roadmaps

### Output-based (bad)
Lists features to ship. Success = "did we build it?"
- "Add search functionality"
- "Build notification system"
- "Migrate to new database"
- "Create admin dashboard"

### Outcome-based (good)
Lists problems to solve or results to achieve. Success = "did it work?"
- "Contributors can find relevant projects in under 60 seconds"
- "Team leads are notified of stalled PRs before they go stale"
- "Database queries return in <200ms at 10x current load"
- "Non-technical admins can manage content without developer help"

### The Conversion Formula
Take any feature request → ask "what problem does this solve?" → phrase the answer as a measurable outcome.

| Output (bad) | Outcome (good) |
|-------------|----------------|
| "Build CI/CD pipeline" | "Code changes reach production within 1 hour of merge" |
| "Add contributor docs" | "New contributors submit their first PR within one session" |
| "Implement design system" | "UI changes are consistent and take 50% less dev time" |
| "Set up monitoring" | "We detect and respond to outages before users report them" |
| "Create API documentation" | "External integrators can build against our API without support tickets" |

---

## 5. Technical Roadmap Specifically — What Belongs

Technical roadmaps cover:

1. **Platform/Infrastructure** — cloud, hosting, CI/CD, environments
2. **Architecture** — system design, service boundaries, data flow
3. **Developer Experience** — tooling, onboarding, local dev, testing
4. **Tech Debt** — migrations, upgrades, refactoring
5. **Security & Compliance** — auth, data protection, audits
6. **Scalability** — performance, capacity, observability
7. **Integrations** — third-party services, APIs, data pipelines

### For WDAI's Context (Nonprofit, Volunteer Contributors)

Priority themes likely include:
- **Contributor Experience** — How easy is it to start contributing?
- **Platform Reliability** — Can we trust what's deployed?
- **Content Infrastructure** — How does educational content flow from creation to delivery?
- **Operational Efficiency** — Can a small team maintain this without burnout?

---

## 6. Common Mistakes

1. **Putting tasks on the roadmap** — "Install Redis" is not a roadmap item. "Sub-second response times for real-time features" is.

2. **Too many items** — If your roadmap has 30 items, it's a backlog. A roadmap should have 8-15 items across all time horizons.

3. **Fixed dates on everything** — Dates create false precision. Use time horizons (Now/Next/Later or Q1/Q2/H2) instead of specific dates unless you have genuine deadlines.

4. **No connection to strategy** — Every roadmap item should trace back to a strategic goal. If you can't explain why an item matters, cut it.

5. **Never updating it** — A roadmap that doesn't change is either fiction or a project plan. Review quarterly at minimum.

6. **Too technical for the audience** — "Migrate from REST to GraphQL" means nothing to a board member. "Reduce data loading times by 3x" does.

7. **Treating it as a promise** — A roadmap is a plan, not a contract. Especially "Next" and "Later" items.

8. **No outcomes, just outputs** — Listing features without articulating the value they deliver.

---

## 7. Practical Example: WDAI Technical Roadmap (Now-Next-Later)

### NOW (Current Quarter — High Confidence)
- **Streamlined contributor onboarding** — New volunteers can set up their dev environment and submit a first PR within one session
- **Automated quality gates** — Every code change passes linting, tests, and review before merge, without manual intervention
- **Platform documentation** — Architecture, conventions, and contribution guidelines are discoverable and current

### NEXT (Next 1-2 Quarters — Medium Confidence)
- **Scalable content pipeline** — Course content flows from creation through review to publication without developer bottleneck
- **Observability foundation** — Team can see what's deployed, what's broken, and how the platform is performing without SSH-ing into servers
- **Design system v1** — Consistent UI components that volunteers can assemble without design expertise

### LATER (6+ Months — Exploratory)
- **API-first architecture** — Platform capabilities exposed as APIs for community-built integrations
- **AI-assisted content creation** — Leverage AI to help scale educational content production
- **Self-service admin tools** — Non-technical team members can manage users, content, and settings without developer support

---

## 8. Key Principles Summary

1. **Roadmaps communicate strategy, backlogs track execution.** If it's actionable this sprint, it's a backlog item, not a roadmap item.
2. **Theme > Outcome > Feature > Task.** Roadmaps live at the theme and outcome level.
3. **8-15 items total** across all time horizons. More than that and you've lost focus.
4. **Now-Next-Later > fixed dates** for teams without predictable capacity (like volunteer teams).
5. **Outcome-phrased items** ("contributors onboard in one session") beat output-phrased items ("write setup docs").
6. **Review every 6 weeks.** Items should flow between columns as you learn.
7. **One roadmap per audience.** Technical stakeholders get more detail; board members get themes and outcomes only.
8. **Every item traces to strategy.** If you can't connect it to a goal, it doesn't belong.

---

## Sources

- [ProdPad: Why I Invented the Now-Next-Later Roadmap](https://www.prodpad.com/blog/invented-now-next-later-roadmap/)
- [ProdPad: Outcome-Based Roadmaps](https://www.prodpad.com/blog/outcome-based-roadmaps/)
- [Atlassian: Technology Roadmap](https://www.atlassian.com/agile/project-management/technology-roadmap)
- [Aha!: Product Roadmap vs Technology Roadmap](https://www.aha.io/blog/the-product-roadmap-vs-the-technology-roadmap)
- [Amplitude: Feature-less Roadmap](https://amplitude.com/blog/feature-less-roadmap)
- [ProductPlan: Three Example Technology Roadmaps](https://www.productplan.com/learn/three-example-technology-roadmaps/)
- [ProductPlan: Theme-Based Roadmap](https://www.productplan.com/learn/theme-based-roadmap/)
- [Product School: Outcome-Based Roadmaps](https://productschool.com/blog/product-strategy/outcome-based-roadmap)
- [airfocus: Now-Next-Later Roadmap](https://airfocus.com/blog/now-next-later-roadmap/)
- [LaunchNotes: Technical vs Product Roadmap](https://www.launchnotes.com/blog/technical-roadmap-vs-product-roadmap-understanding-the-differences-and-importance)
- [Avion: How to Build Now-Next-Later Roadmaps](https://www.avion.io/blog/now-next-later-roadmaps/)
- [Savio: Outcome-Based Roadmap Guide](https://www.savio.io/product-roadmap/outcome-based-roadmap/)
