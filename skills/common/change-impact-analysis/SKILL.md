---
name: change-impact-analysis
description: 分析拟议代码或接口变更影响到的 callers、依赖方、contract、数据流、协议、测试、配置和文档。修改函数、API、消息、schema、service、共享状态或公开行为前使用。
---

# 变更影响分析

在修改函数、接口、协议或共享行为前，先梳理影响范围。

## 工作流

1. 定义拟议变更、兼容性要求，以及必须保持不变的行为。
2. 使用 rg 定位定义和全部引用。包括直接 callers、间接 wrappers、callbacks、subclasses、registrations、dependency injection、reflection、配置、生成代码和脚本。
3. 沿受影响的调用链追踪输入和输出。识别状态、线程、生命周期、serialization、消息 schema、错误行为和资源所有权。
4. 检查下游消费者：测试、CLI、service、launch/config 文件、部署文件、文档、外部 client，以及可访问的其他 package 或仓库。
5. 将影响分类为直接、传递、仅运行时/配置，或不确定。明确标记 API、ABI、wire format、时序和向后兼容风险。
6. 定义最小安全变更计划，以及每个边界所需的验证。

## 输出

提供一份影响地图，包含：

- 修改的 symbol 或 contract；
- callers 和依赖方；
- 数据、状态、协议和生命周期影响；
- 受影响的测试/配置/文档；
- 兼容性和发布风险；
- 要修改的文件，以及明确保持不动的文件；
- 验证命令和仍未解决的问题。

除非用户明确要求同时实现，否则分析期间不要编辑代码。设计发生实质变化后重新运行分析。
