---
name: bug-investigation
description: Investigate a bug from symptoms to a reproducible, evidence-backed root cause without making speculative code changes. Use when behavior is wrong, a test or service fails, logs show an unexpected state, or the user asks to locate a bug before fixing it.
---

# Bug Investigation

Separate diagnosis from repair. Establish what is happening, prove why it happens, and only implement a fix when the user asks for one.

## Workflow

1. Capture the symptom precisely: expected behavior, actual behavior, trigger, frequency, environment, recent changes, and exact error or log text.
2. Reproduce with the smallest safe command or test. Record the command, inputs, observed output, and whether the reproduction is deterministic.
3. Trace the failing path from the entry point through callers, state transitions, I/O, protocol boundaries, and error handling. Use `rg` for definitions and references.
4. Form a small set of falsifiable hypotheses. Rank them by evidence, then test one hypothesis at a time with read-only inspection, focused tests, logs, or temporary instrumentation.
5. Compare expected and actual values at the earliest point where they diverge. Distinguish the root cause from downstream symptoms and unrelated warnings.
6. Check whether the issue is caused by configuration, environment, timing, concurrency, stale artifacts, an API contract, or data assumptions before blaming a single line of code.

## Report

Report:

- minimal reproduction and environment;
- evidence and the first divergence point;
- confirmed or most likely root cause with confidence;
- affected scope and why nearby hypotheses were rejected;
- recommended fix boundary and regression test.

Do not patch around the symptom, rewrite unrelated code, or claim a root cause without evidence. If a fix is requested, preserve the diagnosis and use `test-generation` for a focused regression test.
