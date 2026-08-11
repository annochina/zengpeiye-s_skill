# my-codex-skills Repository Rules

## Source of truth

- This repository is the source of truth for shared Skill source files.
- Keep the global discovery path `~/.agents/skills` linked to this repository's `skills/` directory.
- Edit the repository files, not the installed global link directly.
- Keep project-only knowledge in the consuming project's `.agents/skills/` directory.

## Skill layout

- `skills/common/`: workflows that apply across projects.
- `skills/domain/`: reusable technical-domain knowledge such as ROS and LeRobot.
- `skills/project/`: reusable project-category templates.
- Every Skill directory must contain a valid `SKILL.md` with lowercase hyphenated `name` and a specific trigger-oriented `description`.
- Keep Skill instructions concise. Add `references/`, `scripts/`, or `assets/` only when they materially support the Skill.

## Change workflow

1. Read the target Skill and inspect its existing metadata before editing.
2. Keep unrelated Skills and project files out of the change.
3. Validate every changed Skill with `quick_validate.py`.
4. Review `git diff --check` and the complete staged diff before committing.
5. Do not commit secrets, tokens, generated caches, or machine-specific paths.

## Runtime configuration

Keep repository-specific Codex configuration in `.codex/config.toml`. Do not add MCP servers, hooks, credentials, or destructive automation without an explicit requirement.
