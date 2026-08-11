# Challenge Log

按本地日历日期记录 Skill 仓库的每日 challenge。每次仓库修改都在当天标题下追加记录，并与修改放在同一个提交中。

## 2026-08-11

- Challenge: 将 Skill 源码仓库接入全局发现路径，并加入可持续维护的 Streak Skill。
- Changes: 新增 `skills/common/streak/SKILL.md`，加入按日 `CHANGELOG.md` 规则，并让生成器包含 `streak`。
- Validation: 21 个 Skill 目录通过 `quick_validate.py`；`git diff --check` 通过；`create-skill-tree --dry-run` 正常。
- Follow-up: 按用户要求将日志文件名统一为 `CHANGELOG.md`，移除临时命名。
- Follow-up: 修正 Streak Skill 中残留的日志文件名引用，统一使用 `CHANGELOG.md`。
- Challenge: 将开发经验沉淀从仓库修改日志中分离出来，建立项目级 Challenge Log。
- Changes: 新增全局 `changelog` Skill、`references/log-format.md` 和 `init_changelog.py`，统一使用项目根目录 `CHANGELOG.md` 记录开发经验。
- Follow-up: 根据用户要求移除临时侧目录方案，所有项目经验统一写入根目录 `CHANGELOG.md`。
- Validation: 22 个 Skill 目录通过 `quick_validate.py`；`git diff --check` 通过；`init_changelog.py --dry-run` 保留已有项目 `CHANGELOG.md`；`create-skill-tree --dry-run` 包含 `changelog` 和 `streak`。
- Challenge: 让全新机器从 Git 拉取后可以一键恢复全局 Skill 环境。
- Changes: 新增 `scripts/bootstrap.sh`，负责全局软链接、Codex 兼容路径、维护命令和 shell PATH 初始化。
- Validation: `bash -n scripts/bootstrap.sh` 通过；临时 home 首次/重复部署通过；当前机器 `--no-shell-config` 部署通过；23 个 Skill 目录和 `git diff --check` 通过。
- Next: 每次后续 Skill、配置或脚本修改都在当天条目下追加挑战结果。
- Challenge: 让项目创建 Skill 时不必重复输入项目路径。
- Changes: `create-skill-tree --project-skill NAME` 现在默认使用当前目录，并在当前目录下自动创建 `.agents/skills/NAME/`；保留 `--project` 作为指定其他项目的选项。
- Validation: 当前目录创建、指定 `--project` 创建、命令帮助、23 个 Skill 元数据校验和 `git diff --check` 均通过。
- Challenge: 让项目 Skill 名称直接复用项目文件夹名称。
- Changes: `--project-skill` 现在允许省略名称，自动使用当前项目目录名；显式名称和 `--project` 仍然兼容。
- Validation: 省略名称自动命名、显式名称、指定项目目录、命令帮助、23 个 Skill 元数据校验和 `git diff --check` 均通过。
- Challenge: 让项目根目录直接执行 `create-skill-tree` 就能创建项目 Skill。
- Changes: 默认模式改为使用当前目录创建项目 Skill；新增 `--shared` 用于创建或更新全局共享 Skill 库；自动去除 `-master_delivery` 等发布后缀并规范化名称。
- Validation: 默认项目模式、`--shared` 模式、`observationguilite-master_delivery` 后缀清理、23 个 Skill 元数据校验和 `git diff --check` 均通过。
