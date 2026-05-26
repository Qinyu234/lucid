# 循环：直到 job 达到骨架合格

目标：每个 job 达到「**程序框架基本要求**」（树完整、init 有数据流、leaf 可编译、无明显逻辑空洞），可供后续优化。

## 参数
- Job 列表：`{{job_id 或 all}}`  
- 单 job 命令：`python tools/run_one_job.py {{job_id}}`  
- Memory：**保留必要 leaf memory**，其余按配置  

## 每轮流程
1. 运行并**等待结束**（不中途看 log）  
2. 结束后：`grep` logs 中的 error；检查 workplace 产出  
3. 修复 → 简短说明 → 再跑  
4. 重复直到该 job 达标或你汇报阻塞原因  

## 停止条件
- 我发送 `/stop-report` 或说「停止汇报」时立即停并汇总进度  
