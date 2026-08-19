#!/usr/bin/env bash
set -euo pipefail

# 通用 Git 提交、标签和推送脚本。
# 默认使用当前仓库的 origin 和当前分支，不写死远程地址，也不会自动 force push。

SCRIPT_NAME="$(basename "$0")"
REMOTE_NAME="${GIT_PUSH_REMOTE:-origin}"
REMOTE_URL="${GIT_PUSH_REMOTE_URL:-}"
BRANCH_NAME="${GIT_PUSH_BRANCH:-}"
SET_REMOTE=false
USE_TAG=false
TAG=""
FORCE_WITH_LEASE=false
ASSUME_YES=false
STAGE_ALL=true
ACTION="push"
POSITIONAL=()

usage() {
    cat <<EOF
用法:
  $SCRIPT_NAME [push] [提交消息] [选项]
  $SCRIPT_NAME major [提交消息] [选项]
  $SCRIPT_NAME branches
  $SCRIPT_NAME delete <远程分支> [--yes]

常用示例:
  $SCRIPT_NAME
  $SCRIPT_NAME push "修复录制状态"
  $SCRIPT_NAME push "发布功能" --tag
  $SCRIPT_NAME push "发布功能" --tag v1.02
  $SCRIPT_NAME major "大版本更新"
  $SCRIPT_NAME branches
  $SCRIPT_NAME delete old-branch

选项:
  --remote NAME          远程名称，默认读取 GIT_PUSH_REMOTE 或 origin
  --remote-url URL       远程不存在时使用该地址；已有远程不匹配时需同时使用 --set-remote
  --set-remote           明确允许更新已有远程地址
  --branch NAME          指定推送分支，默认使用当前分支
  --tag [TAG]            推送标签；不指定标签时自动递增 vX.YY
  --force-with-lease     使用 force-with-lease 推送，禁止隐式强推
  --staged-only          只提交已暂存文件，不自动执行 git add -A
  --yes                  跳过删除远程分支时的确认
  -h, --help             显示帮助

环境变量:
  GIT_PUSH_REMOTE        默认远程名称
  GIT_PUSH_REMOTE_URL    默认远程地址
  GIT_PUSH_BRANCH        默认推送分支
EOF
}

die() {
    echo "错误: $*" >&2
    exit 2
}

ensure_repo() {
    local repo_root
    repo_root="$(git rev-parse --show-toplevel 2>/dev/null)" || die "当前目录不在 Git 仓库中"
    cd -- "$repo_root"
}

current_branch() {
    local branch
    branch="${BRANCH_NAME:-$(git symbolic-ref --quiet --short HEAD || true)}"
    [[ -n "$branch" ]] || die "当前处于 detached HEAD，请使用 --branch 指定分支"
    printf '%s\n' "$branch"
}

setup_remote() {
    local current_url

    if git remote get-url "$REMOTE_NAME" >/dev/null 2>&1; then
        current_url="$(git remote get-url "$REMOTE_NAME")"
        if [[ -n "$REMOTE_URL" && "$current_url" != "$REMOTE_URL" ]]; then
            if [[ "$SET_REMOTE" != true ]]; then
                die "远程 $REMOTE_NAME 已存在但地址不同；确认后使用 --set-remote"
            fi
            git remote set-url "$REMOTE_NAME" "$REMOTE_URL"
            echo "远程地址已更新: $REMOTE_NAME -> $REMOTE_URL"
        fi
        return
    fi

    [[ -n "$REMOTE_URL" ]] || die "远程 $REMOTE_NAME 不存在，请先配置 remote 或使用 --remote-url URL"
    git remote add "$REMOTE_NAME" "$REMOTE_URL"
    echo "已添加远程: $REMOTE_NAME -> $REMOTE_URL"
}

latest_version_tag() {
    git tag -l 'v*' \
        | awk '/^v[0-9]+\.[0-9]+$/ { print }' \
        | sort -V \
        | tail -n 1
}

fetch_tags() {
    if command -v timeout >/dev/null 2>&1; then
        timeout 10 git fetch "$REMOTE_NAME" --tags --quiet || \
            echo "警告: 获取远程标签失败，将使用本地标签计算版本" >&2
    else
        git fetch "$REMOTE_NAME" --tags --quiet || \
            echo "警告: 获取远程标签失败，将使用本地标签计算版本" >&2
    fi
}

auto_tag() {
    local latest major minor

    fetch_tags
    latest="$(latest_version_tag)"
    if [[ -z "$latest" ]]; then
        printf 'v1.00\n'
        return
    fi

    major="${latest#v}"
    major="${major%%.*}"
    minor="${latest#*.}"
    minor=$((10#$minor + 1))
    printf 'v%d.%02d\n' "$major" "$minor"
}

major_tag() {
    local latest major

    fetch_tags
    latest="$(latest_version_tag)"
    if [[ -z "$latest" ]]; then
        printf 'v2.00\n'
        return
    fi

    major="${latest#v}"
    major="${major%%.*}"
    printf 'v%d.00\n' "$((major + 1))"
}

validate_tag() {
    [[ -n "$1" ]] || die "标签名不能为空"
    git check-ref-format --allow-onelevel "refs/tags/$1" >/dev/null \
        || die "非法标签名: $1"
    if git rev-parse --verify --quiet "refs/tags/$1" >/dev/null; then
        die "本地标签已存在: $1"
    fi
}

prepare_commit() {
    local commit_msg="$1"

    git diff --check
    if [[ "$STAGE_ALL" == true ]]; then
        git add -A
    else
        echo "只使用已暂存文件"
    fi
    git diff --cached --check

    if git diff --cached --quiet; then
        echo "没有变更需要提交，继续推送当前 HEAD"
        return
    fi

    git commit -m "$commit_msg"
}

push_current_branch() {
    local branch="$1"

    if [[ "$FORCE_WITH_LEASE" == true ]]; then
        git push --force-with-lease -u "$REMOTE_NAME" "$branch"
    else
        git push -u "$REMOTE_NAME" "$branch"
    fi
}

cmd_push() {
    local commit_msg tag

    [[ ${#POSITIONAL[@]} -le 1 ]] || die "push 最多接受一个提交消息"
    commit_msg="${POSITIONAL[0]:-auto push: $(date '+%Y-%m-%d %H:%M:%S')}"
    setup_remote

    if [[ "$USE_TAG" == true ]]; then
        tag="${TAG:-$(auto_tag)}"
        validate_tag "$tag"
    fi

    echo "远程: $REMOTE_NAME"
    echo "分支: $(current_branch)"
    echo "消息: $commit_msg"
    [[ "$USE_TAG" == true ]] && echo "标签: $tag"

    prepare_commit "$commit_msg"
    if [[ "$USE_TAG" == true ]]; then
        git tag "$tag"
        echo "已创建标签: $tag"
    fi

    push_current_branch "$(current_branch)"
    if [[ "$USE_TAG" == true ]]; then
        git push "$REMOTE_NAME" "$tag"
    fi
    echo "推送完成: $REMOTE_NAME/$(current_branch)"
}

cmd_major() {
    local commit_msg tag

    [[ ${#POSITIONAL[@]} -le 1 ]] || die "major 最多接受一个提交消息"
    commit_msg="${POSITIONAL[0]:-major bump: $(date '+%Y-%m-%d %H:%M:%S')}"
    USE_TAG=true
    setup_remote
    tag="${TAG:-$(major_tag)}"
    validate_tag "$tag"

    echo "远程: $REMOTE_NAME"
    echo "分支: $(current_branch)"
    echo "消息: $commit_msg"
    echo "标签: $tag"

    prepare_commit "$commit_msg"
    git tag "$tag"
    push_current_branch "$(current_branch)"
    git push "$REMOTE_NAME" "$tag"
    echo "大版本推送完成: $REMOTE_NAME/$(current_branch), $tag"
}

cmd_branches() {
    local output

    [[ ${#POSITIONAL[@]} -eq 0 ]] || die "branches 不接受额外参数"
    setup_remote
    output="$(git ls-remote --heads "$REMOTE_NAME")"
    if [[ -z "$output" ]]; then
        echo "远程没有可见分支"
        return
    fi

    echo "远程分支 ($REMOTE_NAME):"
    echo "$output" | sed 's|.*refs/heads/||' | sort | nl -w2 -s'. '
}

cmd_delete() {
    local target confirm

    [[ ${#POSITIONAL[@]} -eq 1 ]] || die "用法: $SCRIPT_NAME delete <远程分支> [--yes]"
    target="${POSITIONAL[0]}"
    git check-ref-format --branch "$target" >/dev/null \
        || die "非法分支名: $target"
    setup_remote

    if [[ "$ASSUME_YES" != true ]]; then
        [[ -t 0 ]] || die "非交互环境删除分支必须显式使用 --yes"
        read -r -p "确认删除 $REMOTE_NAME/$target ? [y/N] " confirm
        [[ "$confirm" == y || "$confirm" == Y ]] || {
            echo "已取消"
            return
        }
    fi

    git push "$REMOTE_NAME" --delete "$target"
    echo "已删除远程分支: $REMOTE_NAME/$target"
}

if (($# > 0)); then
    case "$1" in
        push|major|branches|list|ls|delete|rm|del)
            ACTION="$1"
            shift
            ;;
        help|-h|--help)
            ACTION="help"
            shift
            ;;
        *)
            ACTION="push"
            ;;
    esac
fi

while (($# > 0)); do
    case "$1" in
        --remote)
            (($# >= 2)) || die "--remote 需要参数"
            REMOTE_NAME="$2"
            shift 2
            ;;
        --remote-url)
            (($# >= 2)) || die "--remote-url 需要参数"
            REMOTE_URL="$2"
            shift 2
            ;;
        --set-remote)
            SET_REMOTE=true
            shift
            ;;
        --branch)
            (($# >= 2)) || die "--branch 需要参数"
            BRANCH_NAME="$2"
            shift 2
            ;;
        --tag)
            USE_TAG=true
            shift
            if (($# > 0)) && [[ "$1" != --* ]]; then
                TAG="$1"
                shift
            fi
            ;;
        --force-with-lease|--force)
            FORCE_WITH_LEASE=true
            shift
            ;;
        --staged-only)
            STAGE_ALL=false
            shift
            ;;
        --yes)
            ASSUME_YES=true
            shift
            ;;
        -h|--help|help)
            ACTION="help"
            shift
            ;;
        --)
            shift
            POSITIONAL+=("$@")
            break
            ;;
        --*)
            die "未知选项: $1"
            ;;
        *)
            POSITIONAL+=("$1")
            shift
            ;;
    esac
done

case "$ACTION" in
    help)
        usage
        ;;
    push)
        ensure_repo
        cmd_push
        ;;
    major)
        ensure_repo
        cmd_major
        ;;
    branches|list|ls)
        ensure_repo
        cmd_branches
        ;;
    delete|rm|del)
        ensure_repo
        cmd_delete
        ;;
    *)
        die "未知命令: $ACTION；使用 --help 查看用法"
        ;;
esac
