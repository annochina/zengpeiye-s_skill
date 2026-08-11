#!/usr/bin/env python3
"""Create shared skills and project-local agent skills."""

from __future__ import annotations

import argparse
import re
import shutil
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
        "api-and-interface-design",
        "browser-testing-with-devtools",
        "ci-cd-and-automation",
        "code-review-and-quality",
        "code-simplification",
        "context-engineering",
        "debugging-and-error-recovery",
        "deprecation-and-migration",
        "documentation-and-adrs",
        "doubt-driven-development",
        "frontend-ui-engineering",
        "git-workflow-and-versioning",
        "idea-refine",
        "incremental-implementation",
        "interview-me",
        "observability-and-instrumentation",
        "performance-optimization",
        "planning-and-task-breakdown",
        "security-and-hardening",
        "shipping-and-launch",
        "source-driven-development",
        "spec-driven-development",
        "test-driven-development",
        "using-agent-skills",
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

GLOBAL_SHARED_ROOT = Path.home() / ".agents" / "skills"
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PROJECT_RELEASE_SUFFIX_PATTERN = re.compile(
    r"[-_]master[-_]delivery$", re.IGNORECASE
)

SKILL_TITLES = {
    "architecture-exploration": "架构探索",
    "bug-investigation": "Bug 定位",
    "change-impact-analysis": "变更影响分析",
    "changelog": "CHANGELOG 维护",
    "code-review": "代码审查",
    "documentation": "文档维护",
    "embedded-debug": "嵌入式调试",
    "git-workflow": "Git 工作流",
    "refactor": "重构",
    "streak": "Streak",
    "test-generation": "测试生成",
    "ros1": "ROS1",
    "ros2": "ROS2",
    "ros-navigation": "ROS 导航",
    "ros-recording": "ROS 录制",
    "lerobot-dataset": "LeRobot 数据集",
    "lerobot-training": "LeRobot 训练",
    "lerobot-policy": "LeRobot 策略",
    "lerobot-deployment": "LeRobot 部署",
    "api-and-interface-design": "API 与接口设计",
    "browser-testing-with-devtools": "浏览器 DevTools 测试",
    "ci-cd-and-automation": "CI/CD 与自动化",
    "code-review-and-quality": "代码审查与质量",
    "code-simplification": "代码简化",
    "context-engineering": "上下文工程",
    "debugging-and-error-recovery": "调试与错误恢复",
    "deprecation-and-migration": "弃用与迁移",
    "documentation-and-adrs": "文档与 ADR",
    "doubt-driven-development": "质疑驱动开发",
    "frontend-ui-engineering": "前端 UI 工程",
    "git-workflow-and-versioning": "Git 工作流与版本管理",
    "idea-refine": "想法提炼",
    "incremental-implementation": "增量实现",
    "interview-me": "需求访谈",
    "observability-and-instrumentation": "可观测性与埋点",
    "performance-optimization": "性能优化",
    "planning-and-task-breakdown": "规划与任务拆解",
    "security-and-hardening": "安全与加固",
    "shipping-and-launch": "发布与上线",
    "source-driven-development": "来源驱动开发",
    "spec-driven-development": "规格驱动开发",
    "test-driven-development": "测试驱动开发",
    "using-agent-skills": "Agent Skill 使用指南",
}


def skill_title(skill_name: str) -> str:
    return SKILL_TITLES.get(
        skill_name,
        " ".join(part.capitalize() for part in skill_name.split("-")),
    )


def starter_skill_md(category: str, skill_name: str) -> str:
    title = skill_title(skill_name)
    category_label = {
        "common": "跨项目",
        "domain": "技术领域",
        "project": "项目专属",
    }[category]
    return f"""---
name: {skill_name}
description: {category_label} Skill：{title}。需要维护 {skill_name} 相关工作流、约定或参考资料时使用。
---

# {title}

将此模板替换为 {skill_name} Skill 的项目或团队专属说明。

## 范围

- 分类：{category}
- 用途：描述此 Skill 掌握或自动化的内容。
- 触发条件：列出应激活此 Skill 的用户请求。

## 工作流

1. 补充此 Skill 的标准工作流。
2. 添加验证或安全检查。
3. 需要时链接 references、scripts 或 assets 中的资源。
"""


def generated_skill_action(
    skill_file: Path, category: str, skill_name: str, force: bool
) -> str:
    if not skill_file.exists():
        return "create"
    if not force:
        return "keep"
    if skill_file.read_text(encoding="utf-8") == starter_skill_md(category, skill_name):
        return "overwrite"
    return "keep-custom"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a project-local Skill in the current directory."
    )
    parser.add_argument(
        "target",
        nargs="?",
        type=Path,
        default=None,
        help="shared skill destination when --shared is used (default: current project/.agents/skills)",
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


def next_backup_path(path: Path) -> Path:
    candidate = path
    suffix = 0
    while candidate.exists() or candidate.is_symlink():
        suffix += 1
        suffix_text = "" if suffix == 1 else f".{suffix - 1}"
        candidate = Path(f"{path}.backup{suffix_text}")
    return candidate


def ensure_symlink(link_path: Path, target: Path, dry_run: bool) -> None:
    if not target.is_dir():
        raise ValueError(
            f"global shared Skill category does not exist: {target}; "
            "run bootstrap first or specify an explicit shared target"
        )

    expected = target.resolve()
    if link_path.is_symlink() and link_path.resolve() == expected:
        print(f"keep      link      {link_path} -> {target}")
        return

    if dry_run:
        action = "backup+link" if link_path.exists() or link_path.is_symlink() else "link"
        print(f"{action:9} link      {link_path} -> {target}")
        return

    if link_path.exists() or link_path.is_symlink():
        backup_root = link_path.parent.with_name(f"{link_path.parent.name}.backup")
        backup_path = next_backup_path(backup_root / link_path.name)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(link_path), str(backup_path))
        print(f"backup    path      {link_path} -> {backup_path}")

    link_path.parent.mkdir(parents=True, exist_ok=True)
    link_path.symlink_to(target, target_is_directory=True)
    print(f"link      directory {link_path} -> {target}")


def ensure_project_shared_links(project: Path, dry_run: bool) -> int:
    target = project / ".agents" / "skills"
    validate_directory(target)
    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)

    for category in SHARED_SKILL_TREE:
        ensure_symlink(
            target / category,
            GLOBAL_SHARED_ROOT / category,
            dry_run,
        )

    print(f"Project shared Skill links ready: {target}")
    return 0


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
                    action = generated_skill_action(
                        skill_file, category, skill_name, force
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
            if generated_skill_action(skill_file, category, skill_name, force) != "overwrite" and skill_file.exists():
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
        if skill_name in SHARED_SKILL_TREE:
            raise ValueError(
                f"project skill name {skill_name!r} is reserved for shared Skill categories"
            )

    target = project / ".agents" / "skills"
    validate_directory(target)
    ensure_project_shared_links(project, dry_run)
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
            if args.target is None:
                return ensure_project_shared_links(Path.cwd().resolve(), args.dry_run)
            target = args.target.expanduser().resolve()
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
