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

## 新机器一键部署

```bash
git clone https://github.com/annochina/zengpeiye-s_skill.git my-codex-skills
cd my-codex-skills
./scripts/bootstrap.sh
source ~/.bashrc
```

`bootstrap.sh` 会把仓库的 `skills/` 链接到 `~/.agents/skills`，创建 `~/.codex/skills/skill-library` 兼容链接，并安装 `create-skill-tree` 与 `init-changelog` 命令。脚本可以重复执行；已有冲突路径会先保留为备份。

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
- `common/changelog/`：将项目 Bug、架构事实和设计决策沉淀到项目根目录 `CHANGELOG.md`。
- `domain/`：ROS1、ROS2、导航、录制、LeRobot 数据集、训练、策略和部署。
- `project/`：机器人车、BLDC 控制器、Tracker 等项目类模板。

项目专属 Skill 放在对应项目的 `.agents/skills/`，不要复制全局 Skill。

在项目根目录直接创建项目 Skill：

```bash
cd /path/to/project
create-skill-tree
```

命令会使用当前项目文件夹名称作为 Skill 名称，并自动在当前目录的下一级创建 `.agents/skills/<项目文件夹名>/`。末尾的 `-master_delivery` 等发布后缀会被去掉，并统一转换为合法的 Skill 名称。

如果需要显式指定名称，或为指定项目创建 Skill：

```bash
create-skill-tree --project-skill custom-name
create-skill-tree --project /path/to/project
```

维护全局共享 Skill 库时使用：

```bash
create-skill-tree --shared
```

## 校验

```bash
find skills -type f -name SKILL.md -exec dirname {} \; \
  | sort -u \
  | xargs -n1 python /home/zhenpeiye/.codex/skills/.system/skill-creator/scripts/quick_validate.py
```

修改后提交前，先检查完整 diff 和校验结果，再进行 Git 提交与推送。

## Daily Challenge Log

每次修改仓库内容都必须同步更新根目录的 [`CHANGELOG.md`](CHANGELOG.md)。同一天使用同一个日期标题追加记录，不要创建重复日期标题。

项目开发经验统一写入项目根目录的 `CHANGELOG.md`：

```bash
python scripts/init_changelog.py --project /path/to/project
```

如果项目没有 `CHANGELOG.md`，该命令会创建一个安全的初始模板；已有日志默认保留不覆盖。`CHANGELOG.md` 同时记录仓库修改和可复用的开发经验。
