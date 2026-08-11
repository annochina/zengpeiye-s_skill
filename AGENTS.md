# my-codex-skills Repository Rules

## Source of truth

- This repository is the source of truth for shared Skill source files.
- Keep the global discovery path `~/.agents/skills` linked to this repository's `skills/` directory.
- Edit the repository files, not the installed global link directly.
- Keep project-only knowledge in the consuming project's `.agents/skills/` directory.
- Every repository modification must add or update the matching local-date entry in `CHANGELOG.md` in the same commit.
- Record durable project debugging, architecture, and decision knowledge in the consuming project's root `CHANGELOG.md` through the global `changelog` Skill.

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
4. Update `CHANGELOG.md` with the challenge, changes, validation, and next step.
5. Review `git diff --check` and the complete staged diff before committing.
6. Do not commit secrets, tokens, generated caches, or machine-specific paths.

## Runtime configuration

Keep repository-specific Codex configuration in `.codex/config.toml`. Do not add MCP servers, hooks, credentials, or destructive automation without an explicit requirement.

## Skill generator defaults

- Run `create-skill-tree` from a project root to create `./.agents/skills/<normalized-project-name>/SKILL.md`.
- The generator removes release suffixes such as `-master_delivery` from the project directory name.
- Run `create-skill-tree --shared` to create the shared Skill tree under the current project's `.agents/skills/`.
- Pass `~/.agents/skills` explicitly when the machine-level global library must be updated.

## Fresh-machine bootstrap

- Run `./scripts/bootstrap.sh` after cloning this repository.
- The script links `~/.agents/skills` to this repository's `skills/`, installs the maintenance commands, and adds `~/.local/bin` to shell startup files.
- Use `--no-shell-config` when shell startup files must remain untouched.
- The script is idempotent and preserves conflicting existing paths as numbered backups.
