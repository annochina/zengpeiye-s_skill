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
- Challenge: 让 `--shared` 生成的 Skill 树也位于当前项目目录内。
- Changes: `create-skill-tree --shared` 默认改为当前项目的 `.agents/skills/`；需要更新机器级全局库时可显式传入 `~/.agents/skills`。
- Validation: 当前项目路径、显式全局路径、项目 Skill 发现路径、两套生成脚本语法、23 个 Skill 元数据校验和 `git diff --check` 均通过。
- Challenge: 让 Skill 说明更符合中文使用习惯。
- Changes: 将仓库内 Skill 的 description、正文、模板、CHANGELOG 参考格式和界面提示统一改为中文优先；保留命令、代码标识、协议名和必要技术术语为英文。
- Validation: 23 个仓库 Skill、Observationguilite 项目 Skill 和 skill-tree-scaffold Skill 均通过 quick_validate；openai.yaml YAML 解析通过；残留英文模板扫描和 git diff --check 通过。
- Challenge: 修复项目本地旧版 streak Skill 仍显示英文的问题。
- Changes: 将生成器 starter 模板改为中文，并在 Observationguilite 项目中重新生成 .agents/skills 下的共享 Skill 副本。
- Validation: 当前项目共享 Skill 重新生成成功；streak 内容和全部项目副本的英文 starter 残留扫描通过。
- Challenge: 让所有项目的共享 Skill 与全局源码保持同一份内容。
- Changes: 将 `create-skill-tree` 的项目 `common/` 和 `domain/` 改为指向 `~/.agents/skills/` 的软链接；已有普通目录会备份到 `.agents/skills.backup/`，项目专属 Skill 继续保留为普通目录。
- Validation: Observationguilite 项目软链接转换、重复执行保持链接、生成器语法、Skill 元数据校验和 `git diff --check` 通过。
- Challenge: 扩充全局 common Skill，加入成熟的生产级工程工作流。
- Changes: 引入 `addyosmani/agent-skills` 的 24 个 Skill 到 `skills/common/`，同步其 7 个共享检查表到 `skills/references/`，补充 MIT 许可声明，并将 Skill 入口说明翻译为中文。生成器现在识别这些 Skill；`--force` 只覆盖本生成器产生的 starter 文件，不覆盖已引入的自定义内容。
- Validation: 24 个上游 Skill 文件、7 个共享参考文件和 MIT 声明已落盘；路径引用已适配当前目录结构；全部 Skill 通过 `quick_validate.py`，生成器语法、项目发现、`--force --dry-run` 保护和 `git diff --check` 均通过。
- Next: 后续上游工作流更新时，先审查差异，再同步到 `skills/common/` 并重新运行完整校验。
- Challenge: 将常用的 Git 推送脚本改造成可跨项目复用的安全工具。
- Changes: 新增 `scripts/git_push.sh`，保留提交、tag、分支查看和远程分支删除功能；改为使用当前仓库的 remote/branch，加入 `--staged-only`、`--force-with-lease` 和删除确认，并由 bootstrap 安装到 `~/.local/bin/`；同步在 `git-workflow` Skill 中记录使用约定。
- Validation: `bash -n scripts/git_push.sh`、帮助信息、临时 Git 仓库的安全失败路径和 `git diff --check` 通过。
- Next: 在实际项目中先使用 `--staged-only` 验证提交流程，再按需使用自动 tag。

## 2026-08-19

- Challenge: 让项目 Skill 的改动按独立变更立即交付，避免未上传改动累积。
- Changes: 在 `naviai-manip-lerobot-cleaner-convert-gui` 项目 Skill 中加入每个独立逻辑改动都要先写 `CHANGELOG.md`、单独 commit 并立即 push 的约定；明确隔离已有脏改动，push 失败时停止继续修改。
- Validation: `skill-creator` 的 `quick_validate.py` 通过；Skill 内容检查通过。

- Challenge: 让 `create-skill-tree` 初始化项目时自动建立 Skill 检查入口。
- Changes: 项目模式现在会在项目根目录幂等创建或更新带标记的 `AGENTS.md` Skill-discovery 提示；保留已有项目规则，拒绝修改软链接指向的共享 `AGENTS.md`；显式更新全局 Skill 库时不触碰项目指令文件。
- Validation: Python 编译、帮助命令、`git diff --check` 和临时项目首次创建/已有文件保护/重复执行/`--directories-only`/全局 `--shared` 隔离测试通过。

## 2026-08-25

- Challenge: 将程序说明整理需求沉淀为专门的飞书文档输出 Skill，避免与通用 Markdown 排版或代码分析混用。
- Changes: 新增 `skills/common/feishu-software-docs/`，支持程序使用文档、功能表、模块说明、ROS/CLI 接口与部署说明；约束事实保真、命令和代码原样、未知状态标记为“待确认”、按内容选择章节并输出标准飞书友好 Markdown；新增 `agents/openai.yaml` 界面元数据。
- Validation: `quick_validate.py` 通过；当前项目 `.agents/skills/common` 发现路径可见；Skill 252 行，未包含 TODO 占位；13 项触发、边界和七类输入场景标记覆盖检查通过；`openai.yaml` 元数据检查和目标文件 `git diff --check` 通过。
- Next: 使用真实 README、ROS、CLI、信息不完整和已有 Markdown 样本进行一次端到端人工复核，再按反馈收敛触发边界。

## 2026-09-04

- Challenge: 为跨项目 Git 推送建立按目录后缀选择远程仓库的规则。
- Changes: 更新主项目 Skill：`_delivery` 目录默认推送到 `naviai_delivery_push`，无 `_delivery` 后缀的目录默认推送到 `naviai_data_collection`；完整历史迁移需先核对目标 tip，授权强制更新使用 `--force-with-lease`。该规则覆盖三个关联项目的推送场景。
- Validation: 主项目 Skill 通过 `quick_validate.py`；`git diff --check` 通过。
- Next: 后续跨项目推送先核对目录后缀、远程地址和目标分支，再执行 dry-run。

- Challenge: 把项目开工前的需求确认、接口检查和防返工流程沉淀为可复用的知识库入口。
- Changes: 新增 `skills/common/project-start-checklist/`，包含开工门禁、项目要求记录模板、阶段检查规则和用户提供的 10 条标准提问模板，并加入硬件、软件和复盘专用检查。
- Validation: `quick_validate.py`、`git diff --check`、引用路径检查通过；Skill 正文 58 行，配套模板和提问库共 139 行。
- Next: 在各项目的 `.agents/skills/<项目名>/references/project-requirements.md` 中逐项补齐真实项目要求，缺失项确认前不开始实现。
- Challenge: 让项目 CHANGELOG 的每条新增记录都能对应明确的软件版本。
- Changes: 更新通用 `changelog` Skill、Naviai Manip 项目 Skill 和项目仓库规则，要求新增记录使用 `vMAJOR.MINOR.PATCH` 版本标题；版本必须来自 tag、包发布配置或用户确认，历史无版本号记录不回写。
- Validation: 目标 Skill 元数据和正文检查、`git diff --check` 通过。
- Next: 后续项目变更先确认版本号，再写入带版本标题的 CHANGELOG 记录。
