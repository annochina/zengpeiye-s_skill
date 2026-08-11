---
name: refactor
description: Perform safe behavior-preserving refactors such as renaming symbols, extracting functions, moving modules, simplifying structure, or removing verified dead code. Use when code organization should improve without intentionally changing externally observable behavior.
---

# Refactor

Make structural changes in small, verifiable steps while preserving behavior and public contracts.

## Workflow

1. Define the intended structural improvement and the behavior that must not change. Run the relevant baseline tests before editing when practical.
2. Use `change-impact-analysis` for public functions, interfaces, modules, messages, shared state, or lifecycle code. Search all references, including tests, configuration, scripts, generated code, and documentation.
3. Make one coherent mechanical change at a time: rename, extract, move, or simplify. Keep unrelated cleanup out of the diff.
4. Update imports, registrations, build files, configuration, tests, docs, and generated artifacts as required. Check dynamic lookup, plugin loading, reflection, and string-based references before removing code.
5. Run formatting, lint, type checks, focused tests, and then the broader project test command. Use `git diff --check` and inspect the complete diff.
6. Compare behavior at boundaries: public API, serialized data, logs/metrics, error handling, resource lifetime, concurrency, and performance-sensitive paths.

## Guardrails

- Preserve compatibility unless a breaking change is explicitly requested.
- Do not remove code merely because `rg` finds no direct references; verify dynamic and configuration paths.
- Do not combine a refactor with a feature change or speculative bug fix.
- Stop and report if tests, generated files, or external consumers make the intended refactor unsafe.

Report the files changed, behavior-preservation evidence, tests run, and any remaining uncertainty.
