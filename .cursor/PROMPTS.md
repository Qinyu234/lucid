# Code Generator 指令模板

在 Cursor Chat 输入 **`/`** 可选择下方命令（文件在 `.cursor/commands/`）。  
也可复制本节「速查表」到对话框，替换 `{{...}}`。

---

## Rules 在哪里、怎么查

| 文件 | 何时生效 |
|------|----------|
| **`codegen-user-contract.mdc`** | **始终** — §1–§4 生成；§5 优化（只锁文件夹架构 + 性能） |
| `codegen-algorithms.mdc` | **留白** — 未来优化算法规则，充实前勿臆造 |
| `codegen-system.mdc` | 始终 — 阶段与规则索引 |
| `codegen-src.mdc` | 打开 `src/**` 时 — 仅本仓库编译器 |
| `codegen-output.mdc` | 打开 `io/output/**` 时 — 产出路径 |

Cursor UI：**Settings → Rules, Commands → Project Rules**，或 Chat 输入 `@` 引用规则名。

机械检查（生成 job）：`python tools/assess_workplace.py <job_id>`  
机械检查（编译器）：`python tools/verify_src_contract.py`

---

## 怎么用

| 方式 | 操作 |
|------|------|
| **Slash 命令** | Chat 输入 `/` → 选 `design-summary`、`run-fix-loop` 等 |
| **复制模板** | 从下表复制，替换 `{{占位符}}` |
| **全局命令** | 把常用 `.md` 复制到 `~/.cursor/commands/` 可在所有项目用 `/` |

---

## 速查表

### A. 设计与对齐（先聊后写）

**`/design-summary`** — 读代码总结，不改代码  
```
模块：{{growth_loop / code_tree / 全 pipeline}}
```

**`/design-choice`** — 架构抉择  
```
主题：{{topology 种类、节点深度、是否嵌套}}
倾向：{{你的初步想法}}
```

---

### B. 规范与实现

**`/spec-enforce`** — 规范 → rules + 生成 + src 三层  
```
{{粘贴编号规范}}
```

**`/feature-list`** — 多条需求逐条做  
```
1. ...
2. ...
```

**`/continue-next`** — 「上一项完成，做下一项」  
```
已完成：{{...}}
下一项：{{...}}
```

**`/contract-audit`** — 审计生成物是否符合 contract §1–§4  
**`/optimize-performance`** — 优化阶段：只守骨架，改实现求性能  

**`/fix-business-logic`** — 用正确语义覆盖错误实现（similarity、结束条件等）  

**`/memory-recall-spec`** — keyword→embedding→reranker→静态 io  

**`/path-layout-fix`** — config / io/output 目录纠偏  

---

### C. 运行与排错

**`/single-job-run`** — 单 job，结束后才看 log  
```
job_id: ocr_game_logger
```

**`/run-fix-loop`** — 一轮：跑完 → grep error → 看产出 → 修  

**`/run-fix-until-ready`** — 多轮直到骨架合格（配合 `/stop-report` 停止）  

**`/bug-with-log`** — 贴 log/类型错误/代码块排错  

**`/stop-report`** — 停止循环并汇报进度  

---

## 组合示例（你的典型节奏）

```
1. /design-summary        → 对齐
2. /design-choice         → 定 topology
3. /spec-enforce          → 写 rules + 管线
4. /feature-list          → 拆 3～5 条实现
5. /single-job-run        → 验收
6. /bug-with-log          → 若偏了用 /fix-business-logic
7. /run-fix-until-ready   → 夜间打磨
8. /stop-report           → 收工
```

---

## 占位符约定

| 占位符 | 含义 |
|--------|------|
| `{{job_id}}` | 如 `ocr_game_logger` |
| `{{模块/路径}}` | `src/pipeline/growth_loop` 等 |
| `{{粘贴...}}` | 你的编号规范或 log |

---

## 新增自定义命令

```bash
# 项目内
.cursor/commands/my-cmd.md   # Chat 里 /my-cmd
```

文件内容为 Markdown 说明即可；文件名即命令名。
