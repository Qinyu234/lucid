# 规范三层落地

请将以下规范写入项目并贯通三层（`src/` 编译器 → 生成校验 → `io/output` 产出）：

## 规范正文
{{粘贴你的编号规范，例如：一文件一函数、import 边界、node.io、similarity 停止条件等}}

## 执行顺序
1. **Rules**：更新 `.cursor/rules/` 中相关条目（与 `codegen-system` 一致、不重复矛盾）  
2. **生成管线**：调整 growth / code_tree / render_init / verify，使产出可校验  
3. **本体 src/**：通过 `tools/verify_src_contract.py`；必要时 nest 或 split 模块  

## 验收
- 说明改了哪些文件、每条规范如何被 enforce  
- 不扩大范围；未写明的文件不动  
