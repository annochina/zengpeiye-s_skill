#!/usr/bin/env python3
"""Initialize a project's root CHANGELOG.md without overwriting history."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


STARTER = """# Changelog

Record release changes and durable engineering knowledge by local date.

## - YYYY-MM-DD

### Added

- **Initial entry**: replace this placeholder with the first meaningful change.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize a project's root CHANGELOG.md."
    )
    parser.add_argument(
        "--project",
        type=Path,
        default=Path.cwd(),
        help="project root (default: current directory)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite an existing CHANGELOG.md (dangerous; use only intentionally)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show the planned file without writing",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project = args.project.expanduser().resolve()
    if not project.is_dir():
        print(f"error: project directory does not exist: {project}", file=sys.stderr)
        return 2

    target = project / "CHANGELOG.md"
    if target.exists() and not args.force:
        print(f"keep      {target}")
        return 0
    print(f"{'overwrite' if target.exists() else 'create':9} {target}")
    if not args.dry_run:
        target.write_text(STARTER, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
