---
name: architecture-exploration
description: Explore an unfamiliar repository before making changes by mapping its entry points, modules, runtime flow, dependencies, configuration, tests, and project conventions. Use when first entering a codebase, taking over an unfamiliar service or firmware project, or needing a reliable architecture overview.
---

# Architecture Exploration

Build a concise, evidence-based map of an unfamiliar project before editing it.

## Workflow

1. Identify the repository root, active branch, dirty worktree, and likely generated or vendor directories. Preserve all existing user changes.
2. Read the top-level README, contribution notes, build manifests, dependency manifests, container files, launch files, and CI configuration.
3. Inventory the source tree with `rg --files`. Locate executable entry points, service nodes, CLI commands, `main` functions, application bootstrap code, and hardware-facing boundaries.
4. Trace the normal runtime or data flow from entry point through major modules. Read the caller and callee around important boundaries instead of reading every file.
5. Locate configuration, environment variables, message or API definitions, persistence, external services, generated code, and test fixtures.
6. Find the project-standard commands for build, lint, test, packaging, deployment, and local execution. Prefer documented commands over guesses.

## Report

Return a compact map containing:

- repository root and build/runtime entry points;
- module or package responsibilities;
- control flow and important data or message paths;
- external dependencies, protocols, configuration, and generated artifacts;
- test locations and verified commands;
- uncertain areas, risks, and the next files worth reading.

Do not modify production code during exploration. If a follow-up change is requested, use the map to select the smallest relevant scope and run `change-impact-analysis` before editing an interface.
