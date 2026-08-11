# CHANGELOG Entry Format

Use the project's existing Markdown style. The following format works with common Keep a Changelog layouts.

## Date Heading

Keep one date heading per local calendar date. Match the repository's existing style, for example:

```markdown
## - 2026-08-11
```

## Bug / Fixed Entry

```markdown
### Fixed

- **BUG-001: Short title** — one-line symptom and outcome.
  - Root cause: explain the first divergence and mechanism.
  - Attempted: record rejected or insufficient approaches.
  - Final solution: describe the selected fix and compatibility impact.
  - Modified files: `path/to/file.py:Symbol`.
  - Verification: tests, commands, logs, or observed behavior.
  - Early detection: the signal that should identify this issue quickly next time.
```

## Architecture Entry

```markdown
### Architecture

- **ARCH-001: Short title** — durable fact about modules, entry points, data flow, lifecycle, protocol, or build constraints.
  - Evidence: files, symbols, tests, or configuration that establish the fact.
  - Impact: what future changes must preserve.
```

## Decision Entry

```markdown
### Decisions

- **DEC-001: Short title** — selected decision.
  - Context: why a decision was needed.
  - Options: alternatives considered.
  - Tradeoffs: cost, compatibility, performance, or maintenance impact.
  - Revisit when: conditions that would justify changing it.
```

## Rules

- Preserve historical entries; mark old attempts as rejected instead of deleting them.
- Use stable IDs only when they help cross-reference a meaningful entry.
- Use repository-relative paths and exact commands.
- Never store credentials, tokens, or private customer data.
