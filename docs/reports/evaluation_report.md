# Evaluation Report

## 评测目标

本评测用于验证 `main.py` 轻量导诊 demo 在典型症状场景下的稳定性，重点覆盖：

- 风险等级判断：`low` / `medium` / `high`
- 科室推荐：呼吸内科、消化内科、急诊科、口腔科、神经内科等
- 是否需要动态追问
- 高风险否定词边界，例如“没有胸痛，但是呼吸困难”

评测不替代医学验证，仅用于开源展示和工程回归测试。

## 评测数据

评测集位于：

```text
eval/triage_eval_cases.json
```

当前包含 12 条典型问诊样例，覆盖低风险、中风险、高风险、否定高危词和常见科室路由。

## 运行方式

```bash
python scripts/evaluate_demo_cases.py --fail-under 1.0
```

也可以输出完整 JSON 报告：

```bash
python scripts/evaluate_demo_cases.py --output eval/last_report.json
```

## 当前结果

```json
{
  "total": 12,
  "exact_match": 12,
  "exact_match_rate": 1.0,
  "risk_level_accuracy": 1.0,
  "department_accuracy": 1.0,
  "followup_accuracy": 1.0
}
```

## 说明

该评测针对无需 API Key 的轻量 demo 入口，确保面试官或 reviewer 在没有大模型配置时也能快速验证项目核心导诊行为。完整 LangGraph Agent 流程受 LLM、RAG 向量库和本地配置影响，后续可以扩展独立评测集。
