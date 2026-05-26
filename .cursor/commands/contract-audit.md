# 规范符合性审计

请审计 **{{生成项目路径 或 io/output/workplace/JOB_ID}}** 是否符合 **codegen-user-contract**：

1. 骨架：根目录有 `src/`、`io/`、`requirement/`、`run.py`；每业务包有 `__init__.py` 接口  
2. 每文件一个顶层函数；leaf 函数名 = 文件名；`__init__` 函数名 = 文件夹名  
3. import：leaf **仅** `src.shared`；shared **仅** 标准库（库/类型/日志）；`__init__` 仅 shared + 同目录一层 `.child`  
4. 禁止 leaf 直 import 标准库、禁止跨目录 import 非接口  
5. （若为本仓库 pipeline）node 元数据与 SEQ/ROUTER 模板  

编译器本体 `src/` 用 `python tools/verify_src_contract.py`，不用上表第 3 条的 `src.shared` 规则。

## 输出
- 违规清单（路径 + 规则编号 + 修复建议）  
- 若仅生成物违规：是否应加强 `src/` 校验/生成逻辑  
- 运行 `python tools/verify_src_contract.py`（若审计 src）并贴结果  

先报告，**我确认后再批量改**（除非我写了「直接修」）。
