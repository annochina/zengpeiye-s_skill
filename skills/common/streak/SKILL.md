---
name: streak
description: Maintain a daily calendar-based challenge streak for the Skill repository by recording every repository modification in CHANGELOG.md. Use when adding, updating, removing, validating, or publishing Skills, reviewing the current daily challenge, or continuing the repository's daily engineering habit.
---

# Streak

Maintain one honest, date-based challenge log for this Skill repository.

## Required Log

Use the repository-root file `CHANGELOG.md` as the only daily record. Use the local calendar date in `YYYY-MM-DD` format. Do not create a second log or silently rewrite previous entries.

## Workflow

1. Read `CHANGELOG.md` before changing repository files. Inspect the latest entry and determine today's challenge.
2. Choose one small, concrete, verifiable challenge for the current workday. A challenge may be adding a Skill, improving instructions, validating metadata, fixing the generator, or publishing a tested change.
3. Make the requested repository change while keeping unrelated files out of scope.
4. Validate the change with the relevant Skill validator, tests, `git diff --check`, or a safe command run.
5. Before the final response, append the result to `CHANGELOG.md`. If today's heading exists, add another bullet to that heading; otherwise create exactly one new heading for today.
6. Include the log update in the same commit as the repository change.

## Entry Format

Use this format:

```markdown
## YYYY-MM-DD

- Challenge: one concrete challenge for the day.
- Changes: what was added, updated, or fixed.
- Validation: commands or checks that passed, failed, or were unavailable.
- Next: the next small challenge or follow-up.
```

For multiple modifications on the same date, keep one date heading and append additional bullets under it. Preserve earlier entries as history.

## Streak Rules

- Count a streak only from dates that have an actual completed entry.
- Do not claim a consecutive day when the log has no entry for that date.
- Do not backfill a missed day unless the user explicitly asks to record historical work, and label it as backfilled.
- A valid entry requires a concrete change or verified challenge result, not just an intention.
- If validation fails, record the failure honestly and mark the challenge incomplete or continuing.

When handing off work, report the date entry and the current streak only when it can be derived directly from `CHANGELOG.md`.

## Project Skill placement

When creating a project-specific Skill, run the generator from the project root:

```bash
create-skill-tree
```

The command uses the current project directory name as the Skill name and creates it one level below the project at `./.agents/skills/<project-directory-name>/`. Release suffixes such as `-master_delivery` are removed and the result is normalized to a valid lowercase hyphenated name. Pass a name after `--project-skill` to override it, or use `--project /path/to/project` for a different project. Use `--shared` to create the shared tree under the current project's `.agents/skills/`; pass `~/.agents/skills` explicitly when updating the machine-level global library.
