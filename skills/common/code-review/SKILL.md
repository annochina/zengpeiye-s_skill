---
name: code-review
description: Review a diff for correctness, regressions, edge cases, compatibility, security, performance, maintainability, and test coverage. Use when reviewing a patch, pull request, staged changes, or a requested code review; do not modify the code unless explicitly asked.
---

# Code Review

Review the proposed change, not the codebase in the abstract. Findings must be evidence-based and actionable.

## Workflow

1. Inspect `git status`, the diff, the base commit, and `git diff --check`. Confirm the intended scope and preserve unrelated user changes.
2. Read each changed file in context, including callers, contracts, neighboring error handling, configuration, and relevant tests. Use `change-impact-analysis` when the diff changes an interface or shared behavior.
3. Check, in order: correctness and control flow; state, concurrency, resource lifetime, and error paths; boundary and malformed inputs; compatibility and protocol/schema behavior; security and sensitive data; performance; maintainability; and test adequacy.
4. Run focused checks or tests when they are safe and available. Do not hide failures or infer passing behavior from a test that was not run.
5. Report findings first, ordered by severity: blocker, high, medium, low. Include file and line references, the failure mechanism, impact, and a concrete fix direction. Separate findings from questions and praise.

## Review Rules

- Do not report style preferences as defects unless they violate a project rule or create a real risk.
- Do not speculate about unreachable paths without showing how the path is reached.
- Check tests for false positives, missing assertions, and untested failure modes.
- If no actionable findings exist, say so and list residual test or environment risks.

Do not edit, stage, commit, push, or open a PR during review unless the user explicitly requests that follow-up action.
