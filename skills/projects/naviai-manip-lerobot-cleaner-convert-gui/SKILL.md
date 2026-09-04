---
name: naviai-manip-lerobot-cleaner-convert-gui
description: 项目专属 Skill：维护 Naviai Manip Lerobot Cleaner Convert GUI 及其关联的 Observation GUI、ROS1 recorder 工作流；需要跨仓库联调、远程 orin/pico/BDC_TEST 操作、任务队列排障或数据转换链路维护时使用。
---

# Naviai Manip Lerobot Cleaner Convert Gui

## 项目范围

这三个目录属于同一个联动项目，涉及接口、录制状态、数据上传和转换流程的修改时必须一起考虑：

- 当前仓库：`naviai-manip-lerobot-cleaner-convert-gui`
- 关联 GUI 仓库：`../observationguilite-master`
- 关联 ROS1 recorder 仓库：`../nav_ros1rec-5fcc4e9`

两个关联目录位于当前仓库的同级目录。开始修改前确认目录实际存在；`observationguilite-master/AGENTS.md` 是该仓库的额外约定，进入该仓库工作时先阅读它。

## Skill 发现

进入本项目时优先加载本目录的项目专属 Skill；当前项目中的 `common/`、`domain/` 和本项目 Skill 目录均为软链接，分别指向统一共享库和 `~/.agents/skills/projects/naviai-manip-lerobot-cleaner-convert-gui`。需要修改关联项目时，切换到对应项目根目录，并加载该项目自己的 `.agents/skills/<project-skill>/SKILL.md`，不要把本项目专属约定当作其他项目的默认约定。

## 远程主机约定

用户口中的主机名映射如下：

- `orin`：`naviai@192.168.217.100`
- `pico`：`nav01@192.168.217.66`
- `BDC_TEST`：SSH 配置中的远端别名；项目目录通常为 `/root/workspace/naviai-manip-lerobot-cleaner-convert-gui`

凭据不得写入仓库、日志、提交信息或命令输出。推荐在本机 `~/.ssh/config` 中配置上述 Host 别名并使用 SSH key；需要口令时通过本机私有凭据管理器或交互式输入提供。Skill、README 和脚本中只能保留主机别名、用户名和地址，不能保存口令。

## GitLab 远程选择

推送前根据当前仓库目录名选择地址，并先核对 `git remote -v`：

- 目录名以 `_delivery` 结尾：推送到交付仓库 `naviai_delivery_push`，通常使用 `origin`。
- 目录名不以 `_delivery` 结尾：推送到内部仓库 `naviai_data_collection`，通常使用 `production`。

默认只推送到与目录后缀匹配的一个地址，不因 `origin` 是默认远程就推错仓库。只有用户明确要求迁移或双向同步时，才切换目标；迁移完整历史前先读取目标分支 tip，显式授权的强制更新使用 `--force-with-lease`，不使用盲目的 `--force`。

常用连接形式：

```bash
ssh orin
ssh pico
ssh BDC_TEST
scp <local-file> orin:<remote-path>
rsync -av --dry-run <local-path>/ orin:<remote-path>/
```

涉及同步、删除或覆盖远程文件时，先执行只读检查和 `--dry-run`，明确目标后再进行实际操作；除非用户明确授权，不执行删除性远程操作。

## 触发条件

- 修改当前转换 GUI，并可能影响 Observation GUI 或 ROS1 recorder。
- 调试录制、状态、上传、就绪检查、远程启动/停止或数据转换链路。
- 用户提到 `orin`、`pico`，或要求在机器人主机上检查/部署。
- 修改跨仓库共享的 topic、service、参数、文件路径或数据格式。

## 标准工作流

1. 先检查三个仓库的 Git 状态、项目说明和适用的 `AGENTS.md`/Skill，保留用户已有改动。
2. 使用 code-review-graph 梳理当前仓库的入口、调用关系、受影响流程和测试覆盖；图谱不足时再补充文本搜索。
3. 明确跨仓库的数据流：Observation GUI → ROS1 recorder → 本项目清理/转换 GUI，并记录边界契约。
4. 先做最小范围修改，跨仓库变更时分别检查每个仓库的兼容性和配置来源。
5. 远程操作先连接检查、再 dry-run、最后执行；不把口令、token 或包含凭据的环境变量打印到日志。
6. 运行受影响仓库的聚焦测试、语法检查和脚本帮助命令，并记录验证结果。

## Git 上传与 CHANGELOG

- 每完成一个独立的逻辑改动，立即在对应仓库根目录的 `CHANGELOG.md` 写入该改动的简要说明，并记录必要的验证结果；不得把多个独立改动攒到最后再统一记录。
- 完成该改动的最小验证后，只暂存属于本次改动的文件，执行一次独立 commit，并立即 push 到当前分支的已配置上游；后续改动必须重新走一轮，不能合并成一个批量提交。
- 工作区已有的未提交文件、其他仓库的改动和用户未要求的文件不得混入本次 commit。跨仓库改动要在各仓库分别写 CHANGELOG、commit 和 push。
- push 无上游、无权限、网络失败或发生冲突时，立即停止继续修改并报告原因；不得为了继续工作而攒着未上传的后续改动，也不得 force-push、reset 或覆盖用户改动。

## BDC_TEST 清洗任务队列排障

BDC_TEST 是 SSH 远端，不等同于当前本地 checkout。先在远端只读确认进程、任务缓存和任务日志：

```bash
ssh BDC_TEST 'cd /root/workspace/naviai-manip-lerobot-cleaner-convert-gui && ./scripts/manage_services_nosystemd.sh status'
ssh BDC_TEST 'curl -fsS http://127.0.0.1:8000/api/tasks'
ssh BDC_TEST 'tail -n 100 /tmp/lerobot-server.log'
```

清洗任务的旧版实现把队列保存在服务进程内存中：`TaskManager._run_queue` 保存等待顺序，`_active_run_task_id` 保存当前槽位，HTTP 创建/启动接口通过 FastAPI `BackgroundTasks` 调用 `run_cleaning_task`。`dataset/cache/tasks.json` 只保存持久化状态，不能据此推断内存队列为空。

已确认的 BDC_TEST 故障模式：旧版 `TaskManager.delete_task()` 删除任务记录和日志，却没有从 `_run_queue` 移除任务 ID，也没有通知等待者。删除一个已排队任务后，它可能成为队列头的“幽灵 ID”；后续任务会一直显示 `queued`，没有 `RUNNING` 状态、开始日志或处理进度。排查时重点比对：

- `/api/tasks` 中是否只有 `queued` 任务，且没有 `RUNNING` 状态或运行开始日志；
- `log/cleaner_tasks/<id>.log` 是否只到“排队等待清洗”；
- `/tmp/lerobot-server.log` 中异常任务创建前是否有删除排队任务的请求；
- 部署中的 `server.py` 是否仍有 `delete_task()` 只删除 `self.tasks`、未清理 `_run_queue` 的实现。

恢复前保护 `dataset/cache/tasks.json`、`log/cleaner_tasks/` 和 `log/converter_jobs/`。不要直接手改 79 MB 级别的 `tasks.json`，也不要无授权删除任务或重启服务。经用户授权后，可重启无 systemd 服务以清空进程内的幽灵队列；旧版启动加载会把持久化的 `queued`/`running` 任务改为 `paused`，随后应通过 API 明确启动需要继续的任务。代码修复边界是：删除排队任务时在同一条件锁下移除其队列项并 `notify_all()`；同时让取队列头的逻辑跳过已不存在的任务，覆盖服务已被污染的存量状态。

## BDC_TEST 修复部署与在线验证

当前本地 checkout 可能包含其他未提交改动，不能为部署队列 Bug 而执行整仓 `rsync --delete`。先比较目标源码和服务进程加载时间，再只同步队列实现文件：

```bash
LOCAL_FILE=src/naviai_manip_lerobot_cleaner_gui/cleaner/task_manager.py
REMOTE_FILE=/root/workspace/naviai-manip-lerobot-cleaner-convert-gui/$LOCAL_FILE
rsync -avzn --checksum -e 'ssh -o ConnectTimeout=8' "$LOCAL_FILE" "BDC_TEST:$REMOTE_FILE"
rsync -avz  --checksum -e 'ssh -o ConnectTimeout=8' "$LOCAL_FILE" "BDC_TEST:$REMOTE_FILE"
```

同步后用远端实际运行环境执行最小回归，必须设置 `PYTHONPATH`，且不要触碰远端任务缓存：

```bash
ssh BDC_TEST 'cd /root/workspace/naviai-manip-lerobot-cleaner-convert-gui && PYTHONPATH="$PWD/src" /root/miniforge/envs/lerobot_cleaner_convert/bin/python -m pytest -q test/test_task_manager_queue.py'
```

如果测试文件未部署，则使用等价的内存队列回归：验证删除队头后下一个任务能获得槽位，并验证不存在的队头会被跳过。服务重启只在“远端源码时间晚于进程启动时间”或源码哈希不一致时进行；重启前再次确认任务没有实际运行，并经用户授权执行：

```bash
ssh BDC_TEST 'bash -s' <<'REMOTE'
cd /root/workspace/naviai-manip-lerobot-cleaner-convert-gui
PYTHONPATH="$PWD/src" /root/miniforge/envs/lerobot_cleaner_convert/bin/python - <<'PY'
import threading
from types import SimpleNamespace
from naviai_manip_lerobot_cleaner_gui.cleaner.task_manager import TaskManager

def make_manager(*ids):
    manager = object.__new__(TaskManager)
    manager.tasks = {task_id: SimpleNamespace(temp_dir=None, working_dir=None) for task_id in ids}
    manager._stop_flags = {task_id: False for task_id in ids}
    manager._logs = {task_id: [] for task_id in ids}
    manager._run_condition = threading.Condition()
    manager._run_queue = []
    manager._active_run_task_id = None
    manager._save_tasks = lambda: None
    manager._delete_task_log_file = lambda _task_id: None
    return manager

def assert_acquires(manager, task_id):
    finished = threading.Event()
    result = []
    def wait_for_slot():
        result.append(manager.wait_for_run_slot(task_id))
        finished.set()
    thread = threading.Thread(target=wait_for_slot, daemon=True)
    thread.start()
    assert finished.wait(timeout=1), "queue waiter remained blocked"
    assert result == [True], result
    manager.release_run_slot(task_id)

manager = make_manager("deleted-task", "next-task")
manager.enqueue_run_task("deleted-task")
manager.enqueue_run_task("next-task")
manager.delete_task("deleted-task")
assert_acquires(manager, "next-task")

manager = make_manager("next-task")
manager._run_queue = ["deleted-task", "next-task"]
assert_acquires(manager, "next-task")
print("REMOTE_QUEUE_REGRESSION=PASS")
PY
REMOTE
```

确认需要重启后再执行：

```bash
ssh BDC_TEST 'ps -o pid,lstart,args -p "$(pgrep -f "[/]src/server.py" | head -1)"'
ssh BDC_TEST 'stat -c "%y %n" /root/workspace/naviai-manip-lerobot-cleaner-convert-gui/src/naviai_manip_lerobot_cleaner_gui/cleaner/task_manager.py'
ssh BDC_TEST 'cd /root/workspace/naviai-manip-lerobot-cleaner-convert-gui && bash scripts/manage_services_nosystemd.sh restart'
```

认证开启时 `/api/tasks` 返回 401 属于预期，使用已有登录会话或只读检查 `dataset/cache/tasks.json` 的状态计数，不在命令行、Skill 或日志中保存 Cookie、密码或 token。确认服务已加载修复后，`tasks.json` 不应出现 `queued`/`running` 孤儿状态；任务日志应能继续出现“任务开始”而不再只停留在“排队等待清洗”。

## Converter 嵌套包的 IDE 导入解析

`navi_mcap2lerobot` 不是仓库根目录下的一级 `src` 包，而是在 `src/nav_lerobot_converter/nav_lerobot_converter/src` 下的独立 setuptools 子项目。运行时由 `src/naviai_manip_lerobot_cleaner_gui/converter/configuration.py` 注入该路径；Pylance/pyright 不会执行运行时代码，因此仓库根目录必须保留 `pyrightconfig.json` 的 `executionEnvironments.extraPaths` 配置。看到 `无法解析导入 "navi_mcap2lerobot"` 时，先确认编辑器打开的是仓库根目录，再重载 Python language server；命令行运行服务或测试仍使用：

```bash
PYTHONPATH="src:src/nav_lerobot_converter/nav_lerobot_converter/src" python -c 'import navi_mcap2lerobot'
```

## 安全与验证

- 所有日志都视为可能被保存或上传的公开工程产物，不得写入密码或 token。
- 不使用宽范围删除命令；清理文件前先列出精确目标并保留日志文件。
- 修改同步逻辑时，任务日志、转换日志及其他运行日志默认必须保留。
- 修改日志显示时，时间戳应位于左侧时间列，不以短横线替代时间。
- 提交前检查 `git diff --check`，并确认敏感信息未出现在 diff、脚本参数或生成文件中。
