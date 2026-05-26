# 业务语义纠错（重述 spec）

当前实现与预期不符。请以以下语义为**唯一正确 spec** 修改管线（不要只 patch 表象）：

## 正确业务逻辑
{{例如：先 LLM 拆分 → embedding 过相似则无效拆分、不新增节点 → 通过后再 assign seq/para/router 模板}}

## 关联约束
- 静态分析：父子 node 的 `io.in`/`io.out` 类型对齐  
- 类型写入 `io/schema` 或 shared  
- context 需含：数据格式、语义、import/used-by（模板可自动生成部分）  

## 交付
- 改哪些函数、旧逻辑错在哪  
- 建议加的 log event 名便于以后用 log 验证  
