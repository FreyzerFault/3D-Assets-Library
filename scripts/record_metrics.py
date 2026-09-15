#!/usr/bin/env python3
"""
Record metrics script
- Runs tests under coverage
- Produces coverage.json (temporary) and reads assets-report.json
- Appends a readable entry to docs/metrics_log.md

Usage: python scripts/record_metrics.py

The script expects 'coverage' to be available in the environment (python -m coverage).
"""
import json
import shlex
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = REPO_ROOT / "docs" / "metrics_log.md"
COV_JSON = REPO_ROOT / "coverage.json"
ASSETS_REPORT = REPO_ROOT / "assets-report.json"


def run_cmd(cmd, capture_output=True, check=False):
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    return subprocess.run(cmd, capture_output=capture_output, text=True)


def main():
    start = time.time()

    # 1) Run tests under coverage
    print("Running tests with coverage...")
    r = run_cmd([sys.executable, "-m", "coverage", "run", "-m", "unittest", "discover", "-v"], capture_output=False)
    duration = time.time() - start

    # 2) Generate coverage json
    print("Generating coverage json...")
    run_cmd([sys.executable, "-m", "coverage", "json", "-o", str(COV_JSON)])

    # 3) Load coverage.json
    total_cov = None
    files = []
    if COV_JSON.exists():
        with COV_JSON.open("r", encoding="utf-8") as f:
            cov = json.load(f)
        totals = cov.get("totals") or {}
        percent = totals.get("percent_covered") or totals.get("percent") or None
        total_cov = percent
        files_data = cov.get("files") or {}
        for fname, info in files_data.items():
            files.append({
                "file": fname,
                "percent_covered": info.get("percent_covered") or info.get("percent"),
                "missing_lines": info.get("missing_lines", []),
            })

    # 4) Gather assets-report data if present
    assets_summary = {}
    if ASSETS_REPORT.exists():
        try:
            with ASSETS_REPORT.open("r", encoding="utf-8") as f:
                rep = json.load(f)
            assets_summary = {
                "total_assets": rep.get("summary", {}).get("total_assets"),
                "issues": rep.get("summary", {}).get("issues"),
                "warnings": rep.get("summary", {}).get("warnings"),
            }
        except Exception:
            assets_summary = {"error": "could not read assets-report.json"}

    # 5) Get git commit short
    commit = "<unknown>"
    try:
        gr = run_cmd(["git", "rev-parse", "--short", "HEAD"])
        if gr.returncode == 0:
            commit = gr.stdout.strip()
    except Exception:
        pass

    # 6) Compose entry
    now = datetime.now(timezone.utc).isoformat()
    entry_lines = ["---", f"## {now} UTC  — automated metrics", f"- Commit: {commit}", f"- Tests: ran under coverage", f"- Test duration (s): {duration:.2f}"]

    if total_cov is not None:
        entry_lines.append(f"- Coverage total: {total_cov}%")
    else:
        entry_lines.append("- Coverage total: (not available)")

    if files:
        # include top 8 files sorted by percent covered ascending (low coverage first)
        entry_lines.append("- Coverage highlights:")
        for info in sorted(files, key=lambda i: (i.get("percent_covered") or 0))[:8]:
            entry_lines.append(f"  - {info['file']}: {info.get('percent_covered')}%")

    if assets_summary:
        entry_lines.append("- Catalog metrics:")
        for k, v in assets_summary.items():
            entry_lines.append(f"  - {k}: {v}")

    entry_lines.append("\n")

    # 7) Append to log
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write("\n".join(entry_lines))
        f.write("\n")

    print(f"Metrics appended to {LOG_PATH}")


if __name__ == "__main__":
    main()
