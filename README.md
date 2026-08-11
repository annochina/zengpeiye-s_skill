# my-codex-skills

个人 Codex Skill 源码仓库。

## 目录结构

```text
my-codex-skills/
├── skills/
│   ├── common/       # 跨项目通用 Skill
│   ├── domain/       # ROS、LeRobot 等技术领域 Skill
│   └── project/      # 可复用的项目类 Skill 模板
├── scripts/          # Skill 库维护脚本
├── AGENTS.md         # 本仓库协作规则
└── .codex/config.toml
```

全局发现路径应指向仓库中的 `skills/`：

```bash
ln -sfn /path/to/my-codex-skills/skills /home/$USER/.agents/skills
```

当前机器的全局路径为：

```text
/home/zhenpeiye/.agents/skills -> /home/zhenpeiye/source/src/my-codex-skills/skills
```

## Skill 分类

- `common/`：架构探索、Bug 定位、影响分析、代码审查、重构、测试生成、Git 工作流等。
- `common/streak/`：维护按本地日期记录的每日 challenge 和连续 streak。
- `domain/`：ROS1、ROS2、导航、录制、LeRobot 数据集、训练、策略和部署。
- `project/`：机器人车、BLDC 控制器、Tracker 等项目类模板。

项目专属 Skill 放在对应项目的 `.agents/skills/`，不要复制全局 Skill。

## 校验

```bash
find skills -type f -name SKILL.md -exec dirname {} \; \
  | sort -u \
  | xargs -n1 python /home/zhenpeiye/.codex/skills/.system/skill-creator/scripts/quick_validate.py
```

修改后提交前，先检查完整 diff 和校验结果，再进行 Git 提交与推送。

## Daily Challenge Log

每次修改仓库内容都必须同步更新根目录的 [`CHANGELOG.md`](CHANGELOG.md)。同一天使用同一个日期标题追加记录，不要创建重复日期标题。
