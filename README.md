自己搭workflow，自己管理，toy project

📘 Code Generator System Spec v0.1（冻结版）
0. 系统目标（Goal）

构建一个程序生成系统：

将高层任务 → 递归拆分 → 图结构 → 可执行代码项目

核心要求：

7B模型可稳定运行
强约束结构生成
可递归拆分（bounded recursion）
数据流严格
模块依赖严格
状态显式
可日志追踪
1. 总体结构（Pipeline）
TASK
  ↓
NODE GENERATION (LLM)
  ↓
STRUCTURE ASSIGNMENT (SYSTEM)
  ↓
RECURSIVE EXPANSION
  ↓
PRIMITIVE MATCHING
  ↓
CODE EMISSION
  ↓
RUNTIME EXECUTION
  ↓
LOGGING (ASYNC)
2. 核心抽象（唯一数据结构）
✔ Node（唯一基本单位）
Node = {
  id,
  children,
  input,
  output,
  state,
  role
}
3. LLM权限范围（严格限制）

LLM只能做：

✔ 允许
提出最多4个子节点名称
提供语义标签（非逻辑）
描述模块功能（input/output语义）
❌ 禁止
不允许决定结构（SEQ / BRANCH / etc）
不允许写 condition
不允许定义 case
不允许决定 import
不允许定义 recursion规则
4. SYSTEM权限范围

System负责：

✔ Structure Assignment

固定 topology：

SEQ
PAR
BRANCH
ROUTER
✔ Primitive Matching

将 node group 映射为结构类型：

NODE SET → TOPOLOGY
✔ Case Collapse（重要）

LLM输出语义：

attack
heal
fallback

System转换：

CASE_0
CASE_1
CASE_2
5. Topology规则（固定）
✔ SEQ
A → B → C
✔ PAR
A ↘
B → M
C ↗
✔ BRANCH
A → {B, C, D}
✔ ROUTER
A → CASE_ID → branch
6. 递归规则（核心）
✔ Expansion规则
expand(node):
    LLM proposes ≤4 children
    system validates
    system assigns topology
    repeat
✔ 强约束
max_children = 4
max_depth = N
no free-form branching
must terminate in primitive match
7. Primitive Matching（结构收敛）

所有节点必须最终映射：

SEQ
PAR
BRANCH
ROUTER

没有新增 primitive 权限。

8. Case系统（折叠机制，不是逻辑）
✔ LLM输出（语义）
error_detected
success_state
fallback
✔ SYSTEM转换
CASE_0
CASE_1
CASE_2
✔ ROUTER绑定
CASE_ID → branch
❌ 禁止
if
score > threshold
boolean expression
LLM condition reasoning
9. 数据流模型（Function Core）

所有节点统一：

dict → dict
数据结构（必须统一）
{
  meta,
  state,
  data,
  error
}
10. State系统（显式）
✔ 类型
Local state
Flow state
Persistent state (only explicit node)
✔ 规则
state必须声明
state不能隐式存在
state不能跨节点随意共享
11. Import / Inheritance（严格依赖）
✔ DAG规则
A → B → C
✔ 禁止
cycle
backward import
dynamic structural import
12. Logging系统（异步线程）
✔ 架构
execution
  ↓
event emit
  ↓
async queue
  ↓
logger thread
  ↓
storage
✔ event结构
{
  node,
  input_keys,
  output_keys,
  state_read,
  state_write,
  duration
}
✔ 禁止
logging影响执行
logging参与决策
13. 关键设计哲学（核心约束）
✔ 1. LLM = proposal engine

只提出：

“节点集合”

✔ 2. SYSTEM = compiler

负责：

结构 + 规则 + 验证

✔ 3. Runtime = deterministic executor

负责：

dataflow + state + logs

14. 最终系统形态（收敛）
LLM:
    nodes (≤4)

SYSTEM:
    topology assignment
    case collapse
    recursion control

RUNTIME:
    execution + state + logging
15. 一句话总定义（冻结核心）

This system is a constrained recursive graph compiler where LLM proposes nodes, system enforces structure and case collapse, and runtime executes deterministic dataflow with explicit state and logging.