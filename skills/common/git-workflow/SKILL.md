---
name: git-workflow
description: Apply a disciplined Git workflow from diff inspection through checks, intentional commit, push, and pull request preparation. Use when preparing changes for review, committing work, pushing a branch, or opening a PR; never perform publication actions without explicit user authorization.
---

# Git Workflow

Keep the change intentional, reviewable, tested, and recoverable.

## Workflow

1. Inspect repository, branch, remotes, worktree status, and user-owned changes. Never discard unrelated edits.
2. Review the complete diff and untracked files. Run `git diff --check`; inspect ignored/generated files before deciding whether they belong in the change.
3. Run focused tests, lint, type checks, build checks, or project-specific validation proportional to the change. Record failures and environment limitations.
4. Stage only the intended files. Review the staged diff and staged file list again; verify no secrets, credentials, generated noise, or unrelated changes are included.
5. Create a concise imperative commit message describing the actual change. Do not amend or rewrite existing commits unless explicitly requested.
6. Push only when requested. Before pushing, confirm the branch and remote. Open or update a PR only when requested, with a summary, test evidence, risks, and follow-up notes.

## Safety

- Ask before destructive commands, history rewriting, force pushes, deleting branches, or changing remotes.
- Do not use `git reset --hard`, `git checkout --`, or broad clean commands to solve an unclear worktree.
- If checks fail, report the failure instead of claiming the commit is ready.
- Keep commit and PR scope aligned with the user request.

End with the branch, commit, checks, and publication status. If no commit or push was requested, stop after reporting the verified diff.
