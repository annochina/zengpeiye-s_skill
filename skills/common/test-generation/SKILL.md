---
name: test-generation
description: Add focused tests for changed behavior, bug regressions, edge cases, and interface contracts using the repository's existing test conventions. Use after an implementation change, bug fix, refactor, or when targeted coverage is missing.
---

# Test Generation

Turn the changed behavior and its failure modes into the smallest useful regression coverage.

## Workflow

1. Read the change, diagnosis, and existing nearby tests. Identify the contract, inputs, outputs, side effects, error behavior, and concurrency or timing assumptions.
2. Detect the project test framework, fixture style, naming convention, setup/teardown, mocks, factories, and standard test commands. Follow existing patterns.
3. Choose the narrowest useful layer: unit test for local logic, integration test for boundaries, or end-to-end test only when lower layers cannot prove the behavior.
4. Add a focused happy-path test, the relevant boundary or negative case, and a regression case for the reported failure when applicable. Avoid duplicating broad coverage.
5. Prefer real small values and stable fakes over excessive mocking. Assert observable behavior and important side effects, not private implementation details.
6. Run the new test first, then the relevant suite and project-standard checks. If feasible, verify that the regression test would fail without the fix or explain why that check is impractical.

## Quality Checks

- Keep tests deterministic, isolated, readable, and fast.
- Avoid weakening assertions merely to make a test pass.
- Do not alter production behavior just to accommodate a test.
- Include cleanup and resource handling for files, processes, network clients, ROS nodes, or hardware fakes.

Report the scenarios covered, commands run, and any remaining untested risk.
