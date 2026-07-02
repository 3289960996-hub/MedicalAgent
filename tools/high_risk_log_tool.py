import json
from datetime import datetime
from pathlib import Path


LOG_PATH = Path(__file__).resolve().parents[1] / "logs" / "high_risk_logs.json"


def high_risk_log_tool(question: str, risk_level: str, reason: str, action: str) -> dict:
    """
    高风险问题写入本地 JSON 日志，不使用数据库。
    """
    if risk_level != "emergency":
        return {
            "logged": False,
            "path": str(LOG_PATH),
            "reason": "非高风险问题，无需写入高风险日志。"
        }

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    if LOG_PATH.exists():
        try:
            records = json.loads(LOG_PATH.read_text(encoding="utf-8"))
        except Exception:
            records = []
    else:
        records = []

    record = {
        "question": question,
        "risk_level": risk_level,
        "reason": reason,
        "action": action,
        "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    records.append(record)
    LOG_PATH.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "logged": True,
        "path": str(LOG_PATH),
        "record": record
    }
