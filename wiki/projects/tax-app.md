---
name: Tax App
type: personal app
status: active
path: C:\Workspace\Personal Projects\tax-app
tags: [personal, finance, app, active]
---

# Tax App

Personal tax/finance application. Related to `tax-projection-engine` in the same workspace.

## Workspace
- `C:\Workspace\Personal Projects\tax-app\`
- `C:\Workspace\Personal Projects\tax-projection-engine\`

## Technical Details

### Tax App
- **Stack:** Next.js 16, React, TypeScript (strict), Tailwind CSS, Biome
- **Database:** PostgreSQL via Prisma (migrated from SQLite)
- **AI:** Claude API for insights
- **Key patterns:** App Router, tax engine with federal/CA calculations, Decimal.js for precision math, responsive sidebar layout, action-based data mutations
- **Recent work:** 8 calculation bug fixes, major refactor (deleted scenarios table), backdoor Roth, deduction optimizer, withholding pace features

### Tax Projection Engine
- **Stack:** Python FastAPI + SQLAlchemy (backend), React + Vite + TypeScript + Tailwind (frontend)
- **Database:** PostgreSQL
- **Key patterns:** Full-stack with separate backend/frontend, tax rules in YAML config, concurrent dev script
- **Recent work:** 401k/retirement features, W4 calculator, year comparison, contribution limits widget
