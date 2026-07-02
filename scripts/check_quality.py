import py_compile
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


PY_COMPILE_TARGETS = [
    "app.py",
    "chat_schema.py",
    "graph.py",
    "tools/risk_triage_tool.py",
    "tools/department_router_tool.py",
    "scripts/check_triage_regression.py",
]


def main() -> None:
    for relative_path in PY_COMPILE_TARGETS:
        py_compile.compile(str(ROOT / relative_path), doraise=True)

    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_triage_regression.py")],
        cwd=ROOT,
        check=True,
    )

    print("quality checks ok")


if __name__ == "__main__":
    main()
