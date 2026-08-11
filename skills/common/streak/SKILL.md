---
name: streak
description: 通过在 CHANGELOG.md 中记录仓库每次修改，维护 Skill 仓库按日历日期计算的每日 challenge streak。新增、更新、删除、验证或发布 Skill，查看当日 challenge，或继续每日工程习惯时使用。
---

# Streak

为 Skill 仓库维护一份真实、按日期记录的 challenge 日志。

## 必需日志

只使用仓库根目录的 CHANGELOG.md 作为每日记录。日期使用本地日历的 YYYY-MM-DD 格式。不要创建第二份日志，也不要静默改写历史记录。

## 工作流

1. 修改仓库文件前先阅读 CHANGELOG.md，检查最新记录并确定今天的 challenge。
2. 为当前工作日选择一个具体、较小且可验证的 challenge。可以是新增 Skill、改进说明、验证元数据、修复生成器或发布经过测试的变更。
3. 完成用户要求的仓库修改，不要把无关文件带入范围。
4. 使用相关 Skill validator、测试、git diff --check 或安全命令验证变更。
5. 最终回复前，将结果追加到 CHANGELOG.md。如果今天的标题已存在，就在该标题下追加；否则只创建一个今天的日期标题。
6. 将日志修改和仓库变更放入同一个 commit。

## 记录格式

每次记录包含：

- Challenge：当天的具体挑战。
- Changes：新增、更新或修复的内容。
- Validation：通过、失败或不可用的命令和检查。
- Next：仍需继续的下一项小挑战。

同一天有多次修改时，保留一个日期标题，在其下继续追加内容。不要删除历史记录。

## Streak 规则

- 只有存在真实完成记录的日期才计入 streak。
- 某天没有记录时，不要声称连续天数。
- 除非用户明确要求记录历史工作，不要补写错过的日期；如需补写，明确标记为 backfilled。
- 有具体变更或验证结果才算有效记录，只有计划不算。
- 如果验证失败，要如实记录，并将 challenge 标记为未完成或继续中。

交接工作时，只有在可以直接从 CHANGELOG.md 推导时，才报告日期记录和当前 streak。

## 项目 Skill 位置

在项目根目录运行 create-skill-tree。命令使用当前项目目录名创建项目 Skill，位置为当前项目的 .agents/skills/<项目名>/。会去掉 -master_delivery 等发布后缀，并将名称规范化为小写连字符格式。

需要显式名称时可以使用 create-skill-tree --project-skill NAME。需要在当前项目创建共享树时使用 create-skill-tree --shared；需要更新机器级全局库时显式传入 ~/.agents/skills。
