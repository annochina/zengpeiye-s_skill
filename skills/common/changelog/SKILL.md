---
name: changelog
description: Maintain a project's root CHANGELOG.md as durable engineering memory for meaningful bugs, architecture discoveries, and design decisions. Record symptoms, root cause, failed attempts, final solution, modified files, verification, and early detection clues. Use when a problem is solved, a non-obvious project fact is learned, or a decision should remain available to future Codex sessions.
---

# CHANGELOG

Use the consuming project's root `CHANGELOG.md` as the single record for both release history and durable development knowledge. Do not create separate side logs for the same project.

## Workflow

1. Read the project's existing `CHANGELOG.md` before adding an entry. Preserve its date and category conventions.
2. Record only durable knowledge: non-obvious bugs, root-cause investigations, architecture facts, protocol or lifecycle constraints, and design decisions. Do not record routine edits or raw logs.
3. Classify the entry under the existing date heading using `Fixed`, `Changed`, `Added`, `Architecture`, or `Decisions`. Create the current local date heading only when needed.
4. For a bug, capture the symptom, reproduction, root cause, failed attempts, final solution, modified files, verification, and early detection clue.
5. For architecture, capture entry points, module responsibilities, data flow, boundaries, constraints, and evidence.
6. For a decision, capture context, options, selected choice, tradeoffs, compatibility impact, rejected alternatives, and revisit conditions.
7. Link to repository-relative files and symbols. Remove secrets, tokens, personal data, and unstable machine-specific paths.
8. Keep one durable entry per problem, fact, or decision. Extend an existing entry when new evidence belongs to the same issue instead of creating duplicates.

## Entry Pattern

Use [references/log-format.md](references/log-format.md) for the detailed format. Keep entries concise enough to scan and specific enough to prevent the same investigation from being repeated.

## Relationship to Streak

The global `streak` Skill tracks the daily challenge and repository modification cadence. This Skill records the engineering knowledge learned during that work. Both write to `CHANGELOG.md`, using the existing date heading and separate category bullets where appropriate.
