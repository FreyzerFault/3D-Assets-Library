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
import re
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


def parse_test_summary(stdout):
    test_count = 0
    failed_count = 0
    match = re.search(r"Ran\s+(\d+)\s+tests?", stdout or "", re.IGNORECASE)
    if match:
        test_count = int(match.group(1))

    fail_match = re.search(r"failures?=\s*(\d+)", stdout or "", re.IGNORECASE)
    if fail_match:
        failed_count = int(fail_match.group(1))

    return test_count, failed_count


def load_coverage_summary(path):
    if not path.exists():
        return None, []

    with path.open("r", encoding="utf-8") as f:
        cov = json.load(f)

        totals = cov.get("totals") or {}
    total_cov = totals.get("percent_covered") or totals.get("percent")
    files = []
    for fname, info in (cov.get("files") or {}).items():
        summary = info.get("summary") or {}
        files.append(
            {
                "file": fname,
                "percent_covered": summary.get("percent_covered")
                or summary.get("percent"),
                "missing_lines": info.get("missing_lines", []),
            }
        )
    return total_cov, files


def read_assets_summary(path):
    if not path.exists():
        return {}

    try:
        with path.open("r", encoding="utf-8") as f:
            rep = json.load(f)
    except Exception:
        return {"error": "could not read assets-report.json"}

    return {
        "total_assets": rep.get("summary", {}).get("total_assets"),
        "issues": rep.get("summary", {}).get("issues"),
        "warnings": rep.get("summary", {}).get("warnings"),
    }


def main():
    start = time.time()

    # 1) Run tests under coverage
    print("Running tests with coverage...")
    test_run = run_cmd(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-v",
        ],
        capture_output=True,
    )
    duration = time.time() - start

    stdout = (test_run.stdout or "") + "\n" + (test_run.stderr or "")
    test_count, failed_count = parse_test_summary(stdout)

    if test_run.returncode != 0 and failed_count == 0:
        failed_count = max(1, test_count)

    # 2) Generate coverage json
    print("Generating coverage json...")
    run_cmd([sys.executable, "-m", "coverage", "json", "-o", str(COV_JSON)])

    # 3) Load coverage.json
    total_cov, files = load_coverage_summary(COV_JSON)

    # 4) Gather assets-report data if present
    assets_summary = read_assets_summary(ASSETS_REPORT)

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

    # human-readable markdown entry
    entry_lines = [
        "---",
        f"## {now} UTC  — automated metrics",
        f"- Commit: {commit}",
        f"- Tests: {test_count} total, {failed_count} failed",
        f"- Test duration (s): {duration:.2f}",
    ]

    if total_cov is not None:
        entry_lines.append(f"- Coverage total: {total_cov}%")
    else:
        entry_lines.append("- Coverage total: (not available)")

    if files:
        entry_lines.append("- Coverage highlights:")
        for info in sorted(files, key=lambda i: (i.get("percent_covered") or 0))[:8]:
            entry_lines.append(f"  - {info['file']}: {info.get('percent_covered')}%")

    if assets_summary:
        entry_lines.append("- Catalog metrics:")
        for k, v in assets_summary.items():
            entry_lines.append(f"  - {k}: {v}")

    entry_lines.append("\n")

    # structured JSON entry
    json_entry = {
        "timestamp": now,
        "commit": commit,
        "test_count": test_count,
        "failed_tests": failed_count,
        "test_duration_seconds": round(duration, 2),
        "coverage_total": total_cov,
        "coverage_files": files[:50],
        "assets_summary": assets_summary,
    }

    # 7) Append to human-readable log and JSON log
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write("\n".join(entry_lines))
        f.write("\n")

    json_log_path = LOG_PATH.parent / "metrics_log.json"
    if json_log_path.exists():
        try:
            with json_log_path.open("r", encoding="utf-8") as jf:
                arr = json.load(jf)
                if not isinstance(arr, list):
                    arr = []
        except Exception:
            arr = []
    else:
        arr = []

    arr.append(json_entry)
    with json_log_path.open("w", encoding="utf-8") as jf:
        json.dump(arr, jf, ensure_ascii=False, indent=2)

    print(f"Metrics appended to {LOG_PATH} and {json_log_path}")


if __name__ == "__main__":
    main()
