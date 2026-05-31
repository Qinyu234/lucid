# Schema 设计原则和扩展指南

## 文件结构

```
graph/schemas/
  primitives.schema.json   ← 原子定义（shape, identifier, semver...）
  io.schema.json           ← port 定义 + coerce 表
  node.schema.json         ← node 和 edge 定义
  graph.schema.json        ← graph L1 顶层结构
  template.schema.json     ← template + test suite
  operation.schema.json    ← graph protocol operations

compiler/accessor/
  schema_accessor.py       ← 唯一允许直接读 schema 字段的文件
```

## 核心原则

### 1. 引用不复制
schema 之间通过 `$ref` 引用，不复制字段定义。
改一个地方，所有引用自动更新。

### 2. Accessor 隔离
所有业务代码只调用 `schema_accessor.py` 里的函数。
禁止在 accessor 之外直接写 `obj["field_name"]`。
schema 字段改名时，只改 accessor，其他代码不动。

### 3. 版本号
每个 schema 文件有 `version` 字段。
每个 graph/template 文件记录它写入时的 `schema_version`。
版本不匹配时，loader 走迁移路径，不是直接报错。

### 4. additionalProperties: false
所有 schema 对象都设置 `additionalProperties: false`。
新字段必须先加到 schema，不能悄悄塞进 json 里。

---

## 如何扩展 shape 类型

1. 在 `primitives.schema.json` 的 `shape.enum` 里加新值
2. 在 `io.schema.json` 的 `coerce_table` 里补新行和新列
3. 在 `registry/type_registry.json` 里注册 coerce 函数
4. 在 `schema_accessor.py` 里加对应的 getter（如果新 shape 有新字段）
5. 在 `compiler/passes/003_validate_types.py` 里处理新 shape

**不需要改其他任何文件。**

---

## 如何扩展 operation 类型

1. 在 `operation.schema.json` 的 `definitions` 里加新 op 定义
2. 在 `operation` 的 `oneOf` 里加引用
3. 在 `schema_accessor.py` 里加 getter（如果新 op 有新字段）
4. 在 `web/websocket/operation_handler.py` 里加 dispatch case
5. 在 `permissions/roles.json` 里加对应的 permission（如果需要）

**不需要改 graph 结构或 node 定义。**

---

## 如何扩展 node 类型

control_kind 扩展（加新拓扑原语）：
1. 在 `node.schema.json` 的 `control_kind.enum` 里加新值
2. 在 `control_node.properties` 里加新字段
3. 在 `schema_accessor.py` 里加 getter
4. 在 `templates/control/` 里加对应 template
5. 在 `compiler/runtime/` 里加 `execute_<kind>.py`
6. 在 `compiler/passes/010+` 里加对应 lowering pass

---

## Coerce 表扩展

默认 coerce 表在 `io.schema.json` 里是静态的。
自定义 coerce 注册在 `registry/type_registry.json`：

```json
{
  "custom_coerce": [
    {
      "from_shape": "dict",
      "to_shape": "list",
      "fn": "coerce_dict_to_list",
      "safety": "safe",
      "module": "src.shared.coerce_fns"
    }
  ]
}
```

注册后，表里 dict→list 从 forbidden 变成 safe。
连线时 validator 会自动识别并标记 edge 的 coerce 字段。

---

## Schema 变更影响范围速查

| 变更内容 | 需要改的文件 |
|---------|------------|
| 加新 shape | primitives + io(coerce表) + type_registry + accessor + 003_validate_types |
| 加新 operation | operation + accessor + operation_handler + roles |
| 加新 control node | node(control_kind) + accessor + template + execute_* + lowering pass |
| 改 port schema 字段 | io + accessor |
| 改 node 基础字段 | node(node_base) + accessor |
| 改 graph 顶层字段 | graph + accessor |
| 改 template 字段 | template + accessor |
