# 单 job 试运行

对 job **`{{job_id}}`** 做一次完整试运行：

```bash
python tools/run_one_job.py {{job_id}}
```

- 等待进程**完全结束**后再分析  
- 结束后检查：`io/output/logs/run_{{job_id}}_*.log`、`io/output/workplace/{{job_id}}/tree/latest.json`  
- 汇报：成功/失败、树节点数、未生成枝、top 3 errors  

**不要**中途轮询；**不要** commit。
