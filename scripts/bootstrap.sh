#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Bootstrap the repository-managed Codex Skill library.

Usage:
  ./scripts/bootstrap.sh [--home-dir PATH] [--no-shell-config]

Options:
  --home-dir PATH       install links under PATH instead of the current user's home
  --no-shell-config     do not add ~/.local/bin to shell startup files
  -h, --help            show this help
EOF
}

if ! command -v python3 >/dev/null 2>&1; then
    echo "error: python3 is required" >&2
    exit 2
fi

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
home_dir=""
update_shell_config=true

while (($# > 0)); do
    case "$1" in
        --home-dir)
            if (($# < 2)); then
                echo "error: --home-dir requires a path" >&2
                exit 2
            fi
            home_dir="$(cd -- "$2" 2>/dev/null && pwd -P || true)"
            if [[ -z "$home_dir" ]]; then
                home_dir="$2"
                mkdir -p -- "$home_dir"
                home_dir="$(cd -- "$home_dir" && pwd -P)"
            fi
            shift 2
            ;;
        --no-shell-config)
            update_shell_config=false
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "error: unknown argument: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

if [[ -z "$home_dir" ]]; then
    home_dir="$(python3 -c 'from pathlib import Path; print(Path.home())')"
fi

shared_source="$repo_root/skills"
if [[ ! -d "$shared_source" ]]; then
    echo "error: repository skill directory does not exist: $shared_source" >&2
    exit 2
fi

next_backup_path() {
    local target="$1"
    local candidate="${target}.backup"
    local index=1
    while [[ -e "$candidate" || -L "$candidate" ]]; do
        candidate="${target}.backup.${index}"
        index=$((index + 1))
    done
    printf '%s\n' "$candidate"
}

ensure_link() {
    local target="$1"
    local source="$2"
    local target_parent
    local source_resolved
    local current_resolved
    local backup

    target_parent="$(dirname -- "$target")"
    mkdir -p -- "$target_parent"
    source_resolved="$(readlink -f -- "$source")"

    if [[ -L "$target" ]]; then
        current_resolved="$(readlink -f -- "$target" 2>/dev/null || true)"
        if [[ "$current_resolved" == "$source_resolved" ]]; then
            echo "keep      $target -> $source_resolved"
            return
        fi
        backup="$(next_backup_path "$target")"
        mv -- "$target" "$backup"
        echo "backup    $target -> $backup"
    elif [[ -e "$target" ]]; then
        backup="$(next_backup_path "$target")"
        mv -- "$target" "$backup"
        echo "backup    $target -> $backup"
    fi

    ln -s -- "$source" "$target"
    echo "link      $target -> $source_resolved"
}

agents_skills="$home_dir/.agents/skills"
codex_skills="$home_dir/.codex/skills"
codex_library="$codex_skills/skill-library"
bin_dir="$home_dir/.local/bin"

ensure_link "$agents_skills" "$shared_source"
ensure_link "$codex_library" "$agents_skills"
ensure_link "$bin_dir/create-skill-tree" "$repo_root/scripts/create_skill_tree.py"
ensure_link "$bin_dir/init-changelog" "$repo_root/scripts/init_changelog.py"
ensure_link "$bin_dir/git_push.sh" "$repo_root/scripts/git_push.sh"

add_path_to_file() {
    local shell_file="$1"
    local path_line='export PATH="$HOME/.local/bin:$PATH"'

    if [[ ! -f "$shell_file" ]]; then
        return 1
    fi
    if grep -Fqx -- "$path_line" "$shell_file"; then
        return 0
    fi
    {
        echo
        echo "# Codex Skill tools"
        echo "$path_line"
    } >> "$shell_file"
    echo "path      $shell_file"
    return 0
}

if [[ "$update_shell_config" == true ]]; then
    shell_files=()
    for shell_file in "$home_dir/.bashrc" "$home_dir/.zshrc" "$home_dir/.profile"; do
        if [[ -f "$shell_file" ]]; then
            shell_files+=("$shell_file")
        fi
    done
    if ((${#shell_files[@]} == 0)); then
        shell_files+=("$home_dir/.profile")
        touch "${shell_files[0]}"
    fi
    for shell_file in "${shell_files[@]}"; do
        add_path_to_file "$shell_file" || true
    done
fi

echo "Bootstrap complete"
echo "Repository: $repo_root"
echo "Shared skills: $agents_skills"
echo "Commands: $bin_dir/create-skill-tree, $bin_dir/init-changelog, $bin_dir/git_push.sh"
echo "Restart the shell or export PATH=\"$bin_dir:\$PATH\" to use the commands now."
