#!/usr/bin/env python3
"""Create shared skills and project-local agent skills."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SHARED_SKILL_TREE = {
    "common": (
        "architecture-exploration",
        "bug-investigation",
        "change-impact-analysis",
        "changelog",
        "code-review",
        "documentation",
        "embedded-debug",
        "git-workflow",
        "refactor",
        "streak",
        "test-generation",
    ),
    "domain": (
        "ros1",
        "ros2",
        "ros-navigation",
        "ros-recording",
        "lerobot-dataset",
        "lerobot-training",
        "lerobot-policy",
        "lerobot-deployment",
    ),
}

DEFAULT_TARGET = Path.home() / ".agents" / "skills"
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PROJECT_RELEASE_SUFFIX_PATTERN = re.compile(
    r"[-_]master[-_]delivery$", re.IGNORECASE
)


def skill_title(skill_name: str) -> str:
    return " ".join(part.capitalize() for part in skill_name.split("-"))


def starter_skill_md(category: str, skill_name: str) -> str:
    title = skill_title(skill_name)
    category_label = {
        "common": "cross-project",
        "domain": "technical-domain",
        "project": "project-specific",
    }[category]
    return f"""---
name: {skill_name}
description: Starter {category_label} skill for {title}. Use when Codex needs the workflows, conventions, or references maintained for {skill_name}.
---

# {title}

Replace this starter content with the reusable instructions for the `{skill_name}` skill.

## Scope

- Category: `{category}`
- Purpose: Describe what this skill knows or automates.
- Triggers: List the user requests that should activate this skill.

## Workflow

1. Add the normal workflow for this skill.
2. Add validation or safety checks.
3. Link directly to any files in `references/`, `scripts/`, or `assets/` when they are needed.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a project-local Skill in the current directory."
    )
    parser.add_argument(
        "target",
        nargs="?",
        type=Path,
        default=None,
        help=f"shared skill destination when --shared is used (default: {DEFAULT_TARGET})",
    )
    parser.add_argument(
        "--shared",
        action="store_true",
        help="create or update the shared Skill library instead of a project Skill",
    )
    parser.add_argument(
        "--project",
        type=Path,
        help="create project-specific skills under PROJECT/.agents/skills (default: current directory)",
    )
    parser.add_argument(
        "--project-skill",
        action="append",
        default=[],
        nargs="?",
        const="",
        metavar="NAME",
        help="project skill name; omit NAME to use the project directory name",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite generated leaf SKILL.md files without deleting other files",
    )
    parser.add_argument(
        "--directories-only",
        action="store_true",
        help="create directories without starter SKILL.md files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show planned changes without writing anything",
    )
    return parser.parse_args()


def validate_directory(target: Path) -> None:
    if target.exists() and not target.is_dir():
        raise ValueError(f"target exists and is not a directory: {target}")


def validate_skill_name(skill_name: str) -> None:
    if not SKILL_NAME_PATTERN.fullmatch(skill_name):
        raise ValueError(
            f"invalid skill name {skill_name!r}; use lowercase letters, digits, and hyphens"
        )


def project_skill_name(project: Path) -> str:
    """Derive a valid Skill name from a project directory name."""
    name = PROJECT_RELEASE_SUFFIX_PATTERN.sub("", project.name)
    name = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()
    if not name:
        raise ValueError(
            f"cannot derive a skill name from project directory: {project}"
        )
    validate_skill_name(name)
    return name


def create_shared_tree(
    target: Path, force: bool, directories_only: bool, dry_run: bool
) -> int:
    validate_directory(target)

    if dry_run:
        for category, skills in SHARED_SKILL_TREE.items():
            category_path = target / category
            print(f"{'keep' if category_path.exists() else 'create':9} directory {category_path}")
            for skill_name in skills:
                skill_path = category_path / skill_name
                print(f"{'keep' if skill_path.exists() else 'create':9} directory {skill_path}")
                if not directories_only:
                    skill_file = skill_path / "SKILL.md"
                    action = "overwrite" if skill_file.exists() and force else (
                        "keep" if skill_file.exists() else "create"
                    )
                    print(f"{action:9} file      {skill_file}")
        return 0

    target.mkdir(parents=True, exist_ok=True)
    for category, skills in SHARED_SKILL_TREE.items():
        category_path = target / category
        category_path.mkdir(parents=True, exist_ok=True)
        for skill_name in skills:
            skill_path = category_path / skill_name
            skill_path.mkdir(parents=True, exist_ok=True)
            if directories_only:
                continue
            skill_file = skill_path / "SKILL.md"
            if skill_file.exists() and not force:
                continue
            skill_file.write_text(
                starter_skill_md(category, skill_name), encoding="utf-8"
            )

    print(f"Shared skill library ready: {target}")
    return 0


def create_project_skills(
    project: Path,
    skill_names: list[str],
    force: bool,
    directories_only: bool,
    dry_run: bool,
) -> int:
    if not project.exists():
        raise ValueError(f"project directory does not exist: {project}")
    if not project.is_dir():
        raise ValueError(f"project path is not a directory: {project}")
    for skill_name in skill_names:
        validate_skill_name(skill_name)

    target = project / ".agents" / "skills"
    validate_directory(target)
    if dry_run:
        print(f"{'keep' if target.exists() else 'create':9} directory {target}")
        for skill_name in skill_names:
            skill_path = target / skill_name
            print(f"{'keep' if skill_path.exists() else 'create':9} directory {skill_path}")
            if not directories_only:
                skill_file = skill_path / "SKILL.md"
                action = "overwrite" if skill_file.exists() and force else (
                    "keep" if skill_file.exists() else "create"
                )
                print(f"{action:9} file      {skill_file}")
        return 0

    target.mkdir(parents=True, exist_ok=True)
    for skill_name in skill_names:
        skill_path = target / skill_name
        skill_path.mkdir(parents=True, exist_ok=True)
        if directories_only:
            continue
        skill_file = skill_path / "SKILL.md"
        if skill_file.exists() and not force:
            continue
        skill_file.write_text(
            starter_skill_md("project", skill_name), encoding="utf-8"
        )

    print(f"Project skill directory ready: {target}")
    return 0


def main() -> int:
    args = parse_args()
    try:
        if args.shared:
            if args.project is not None or args.project_skill:
                raise ValueError("do not combine --shared with project Skill options")
            target = (args.target or DEFAULT_TARGET).expanduser().resolve()
            return create_shared_tree(
                target,
                args.force,
                args.directories_only,
                args.dry_run,
            )

        if args.target is not None:
            raise ValueError("a shared target requires --shared")

        project = (args.project or Path.cwd()).expanduser().resolve()
        if args.project_skill:
            skill_names = [
                skill_name or project_skill_name(project)
                for skill_name in args.project_skill
            ]
        else:
            skill_names = [project_skill_name(project)]

        return create_project_skills(
            project,
            skill_names,
            args.force,
            args.directories_only,
            args.dry_run,
        )
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
