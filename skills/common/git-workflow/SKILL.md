---
name: git-workflow
description: 应用从 diff 检查、验证到有意提交、push 和 pull request 准备的规范 Git 工作流。准备评审变更、提交、推送分支或创建 PR 时使用；未经用户明确授权，绝不执行发布操作。
---

# Git 工作流

让每次变更都有明确目的、可评审、经过测试且可恢复。

## 工作流

1. 检查仓库、分支、remotes、工作区状态和用户已有修改。绝不丢弃无关编辑。
2. 检查完整 diff 和未跟踪文件。运行 git diff --check；判断变更是否应包含被忽略或生成的文件前，先检查它们。
3. 按变更风险运行聚焦测试、lint、类型检查、构建检查或项目专属验证。记录失败和环境限制。
4. 只 stage 预期文件。再次检查 staged diff 和 staged 文件列表，确认没有 secret、credential、生成噪声或无关修改。
5. 创建简洁的祈使句 commit message，描述实际变更。除非明确要求，不要 amend 或重写已有提交。
6. 仅在用户要求时 push。push 前确认分支和 remote。仅在用户要求时创建或更新 PR，并提供摘要、测试证据、风险和后续事项。

## 安全

- 执行破坏性命令、重写历史、force push、删除分支或修改 remote 前先询问。
- 不要使用 git reset --hard、git checkout -- 或宽泛的 clean 命令解决不明确的工作区问题。
- 如果检查失败，要如实报告，不要声称提交已经准备好。
- 让 commit 和 PR 范围与用户请求保持一致。

结束时报告分支、commit、检查结果和发布状态。如果用户没有要求 commit 或 push，在报告已验证的 diff 后停止。
