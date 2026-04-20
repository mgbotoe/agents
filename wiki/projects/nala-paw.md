---
name: Nala Paw
org: personal
type: personal app
status: active
path: C:\Workspace\Personal Projects\nala-paw
tags: [personal, app, active, nala]
---

# Nala Paw

Pet/diet tracker for Nala (German Shepherd). Pivoted from daily logging to exception-based notes.

## Workspace
`C:\Workspace\Personal Projects\nala-paw\`

## Technical Details
- **Stack:** Vite + React + TypeScript + shadcn/ui + Tailwind CSS + Vitest
- **Origin:** Lovable-generated project
- **Key patterns:** SPA (not Next.js), component-based with form hooks, exception-based note model
- **Toast system:** Sonner only (radix toast removed 2026-04-17 — was dead-mounted alongside Sonner with zero callers)
- **Recent work:**
  - 2026-04-17: Defrag pass — removed dead radix toast stack (~360 lines, dropped `@radix-ui/react-toast` dep). Fixed timezone bug in WeightSection + TrainingFormDialog (`toISOString().slice(0,10)` was returning UTC date for late-evening PDT users; now uses `date-fns format()`). Report at `.claude/defrag/20260417-205800-report.md`.
  - Earlier: Pivot to exception-based notes, a11y improvements (aria-pressed), cleanup of 74 console.log calls
- **Known fragmentation (deferred, not yet fixed):** 4 sections (Bathing/Exercise/Medications/Vaccinations) share an identical form scaffold — extraction candidate `useEntryForm<T>`. 11 of 14 stores share an identical Supabase CRUD shape — extraction candidate `createSupabaseStore<T>` factory.
