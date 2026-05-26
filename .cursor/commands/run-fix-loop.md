# 运行结束 → 分析 → 修复（单轮）

## 运行
- Job：`{{job_id，如 ocr_game_logger}}`  
- 命令：`{{如 python tools/run_one_job.py ocr_game_logger}}`  
- **在进程结束前不要读 log**；只等待运行结束  

## 结束后按顺序
1. **Errors**：在 `io/output/logs/` grep `ERROR` / `Traceback`，定位并修复  
2. **产出物**：检查 `io/output/workplace/{{job_id}}/` 树与代码——分叉是否齐全、init 是否有 `ctx` 流动、leaf 是否符合 contract  
3. **归类**：每条问题标为 `算法` / `模型(LLM)` / `管线逻辑` / `配置` / `规范校验`  

## 修复原则
- 最小 diff；保留必要 leaf memory  
- 修完说明如何再跑一轮验证  

**不要**在运行过程中轮询 log；**不要**未结束就改代码。
