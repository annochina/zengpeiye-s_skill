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
- Next: 每次后续 Skill、配置或脚本修改都在当天条目下追加挑战结果。
