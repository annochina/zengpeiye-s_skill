---
name: change-impact-analysis
description: Analyze the callers, dependents, contracts, data flow, protocol effects, tests, configuration, and documentation affected by a proposed code or interface change. Use before modifying functions, APIs, messages, schemas, services, shared state, or public behavior.
---

# Change Impact Analysis

Map the blast radius before changing a function, interface, protocol, or shared behavior.

## Workflow

1. Define the proposed change, the compatibility requirement, and the behavior that must remain unchanged.
2. Locate the definition and all references with `rg`. Include direct callers, indirect wrappers, callbacks, subclasses, registrations, dependency injection, reflection, configuration, generated code, and scripts.
3. Trace inputs and outputs through the affected call chain. Identify state, threading, lifecycle, serialization, message schemas, error behavior, and resource ownership.
4. Inspect downstream consumers: tests, CLIs, services, launch/config files, deployment files, documentation, external clients, and other packages or repositories when available.
5. Classify impact as direct, transitive, runtime/configuration-only, or uncertain. Mark API, ABI, wire-format, timing, and backward-compatibility risks explicitly.
6. Define the smallest safe change plan and the validation required at each boundary.

## Output

Provide an impact map with:

- changed symbol or contract;
- callers and dependents;
- data, state, protocol, and lifecycle effects;
- affected tests/configuration/docs;
- compatibility and rollout risks;
- files to change and files deliberately left untouched;
- validation commands and any unresolved questions.

Do not edit code during analysis unless the user explicitly combines analysis with implementation. Re-run the analysis after the design changes materially.
