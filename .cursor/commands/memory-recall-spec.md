# Memory 召回管线实现

请实现或调整 leaf memory 召回，顺序为：

1. **关键词 + embedding** 粗检索  
2. **Reranker** 精排  
3. **静态规则**：io.in / io.out 类型与名称兼容检测  

## 场景
- 生成新 leaf 前询问是否可复用已有 shared/leaf  
- Job：`{{可选 job_id}}`  

## 约束
- 配置从 `config/` 读取模型与 API，按 scenario 区分  
- 失败时降级策略写清，不阻塞主 pipeline  

交付：涉及模块、配置项、一次手动验证步骤。
