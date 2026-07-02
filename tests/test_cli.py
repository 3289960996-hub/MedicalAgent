import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_cli_runs_all_demo_cases():
    completed = subprocess.run(
        [sys.executable, "main.py", "--case", "all"],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    payload = json.loads(completed.stdout)

    assert len(payload) == 3
    assert {item["actual"]["risk_level"] for item in payload} == {
        "low",
        "medium",
        "high",
    }
    assert all(item["actual"]["disclaimer"] for item in payload)
