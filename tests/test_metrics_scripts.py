import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


record_metrics = load_module("record_metrics", "scripts/record_metrics.py")
metrics_trend = load_module("metrics_trend", "scripts/metrics_trend.py")


class _FakeCompletedProcess:
    def __init__(self, stdout="", stderr="", returncode=0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


class MetricsScriptTests(unittest.TestCase):
    def test_parse_test_summary_reads_counts(self):
        stdout = "Ran 3 tests in 0.05s\nFAILED (failures=1)"
        test_count, failed_count = record_metrics.parse_test_summary(stdout)
        self.assertEqual(test_count, 3)
        self.assertEqual(failed_count, 1)

    def test_load_coverage_summary_reads_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            coverage_path = Path(tmpdir) / "coverage.json"
            coverage_path.write_text(
                json.dumps(
                    {
                        "totals": {"percent_covered": 88.5},
                        "files": {
                            "generate_assets_data.py": {
                                "summary": {
                                    "percent_covered": 88.5,
                                },
                                "missing_lines": [12, 15],
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )

            total_cov, files = record_metrics.load_coverage_summary(coverage_path)
            self.assertEqual(total_cov, 88.5)
            self.assertEqual(len(files), 1)
            self.assertEqual(files[0]["file"], "generate_assets_data.py")
            self.assertEqual(files[0]["percent_covered"], 88.5)
            self.assertEqual(files[0]["missing_lines"], [12, 15])

    def test_read_assets_summary_reads_report(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "assets-report.json"
            report_path.write_text(
                json.dumps(
                    {
                        "summary": {"total_assets": 9, "issues": 1, "warnings": 3},
                    }
                ),
                encoding="utf-8",
            )

            summary = record_metrics.read_assets_summary(report_path)
            self.assertEqual(summary["total_assets"], 9)
            self.assertEqual(summary["issues"], 1)
            self.assertEqual(summary["warnings"], 3)

    def test_make_bar_uses_range_and_width(self):
        self.assertEqual(metrics_trend.make_bar(10, 0, 20, width=4), "##")
        self.assertEqual(metrics_trend.make_bar(0, 0, 20, width=4), "")

    def test_load_entries_accepts_metrics_history(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_path = Path(tmpdir) / "metrics_log.json"
            metrics_path.write_text(
                json.dumps(
                    [
                        {"timestamp": "2026-09-16T00:00:00Z", "coverage_total": 82.0},
                        {"timestamp": "2026-09-15T00:00:00Z", "coverage_total": 81.8},
                    ]
                )
            )
            original = metrics_trend.LOG_PATH
            metrics_trend.LOG_PATH = metrics_path
            try:
                entries = metrics_trend.load_entries()
                self.assertEqual(len(entries), 2)
                self.assertEqual(entries[0]["coverage_total"], 82.0)
            finally:
                metrics_trend.LOG_PATH = original

    def test_record_metrics_main_appends_entry(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            log_path = repo_root / "docs" / "metrics_log.md"
            json_log_path = repo_root / "docs" / "metrics_log.json"
            cov_path = repo_root / "coverage.json"
            report_path = repo_root / "assets-report.json"
            log_path.parent.mkdir(parents=True, exist_ok=True)

            report_path.write_text(
                json.dumps(
                    {"summary": {"total_assets": 12, "issues": 0, "warnings": 2}}
                ),
                encoding="utf-8",
            )

            original_root = record_metrics.REPO_ROOT
            original_log = record_metrics.LOG_PATH
            original_cov = record_metrics.COV_JSON
            original_report = record_metrics.ASSETS_REPORT
            original_time = record_metrics.time.time
            original_run_cmd = record_metrics.run_cmd
            try:
                record_metrics.REPO_ROOT = repo_root
                record_metrics.LOG_PATH = log_path
                record_metrics.COV_JSON = cov_path
                record_metrics.ASSETS_REPORT = report_path
                record_metrics.time.time = lambda: 1.0

                def fake_run_cmd(cmd, capture_output=True, check=False):
                    if (
                        isinstance(cmd, list)
                        and len(cmd) >= 4
                        and cmd[1:4] == ["-m", "coverage", "run"]
                    ):
                        return _FakeCompletedProcess(
                            stdout="Ran 2 tests in 0.01s\nOK\n", stderr="", returncode=0
                        )
                    if (
                        isinstance(cmd, list)
                        and len(cmd) >= 4
                        and cmd[1:4] == ["-m", "coverage", "json"]
                    ):
                        cov_path.write_text(
                            json.dumps(
                                {
                                    "totals": {"percent_covered": 82},
                                    "files": {
                                        "generate_assets_data.py": {
                                            "percent_covered": 82,
                                            "missing_lines": [],
                                        }
                                    },
                                }
                            ),
                            encoding="utf-8",
                        )
                        return _FakeCompletedProcess(stdout="", stderr="", returncode=0)
                    if isinstance(cmd, list) and cmd[:3] == [
                        "git",
                        "rev-parse",
                        "--short",
                    ]:
                        return _FakeCompletedProcess(
                            stdout="abc1234\n", stderr="", returncode=0
                        )
                    raise AssertionError(f"Unexpected command: {cmd}")

                record_metrics.run_cmd = fake_run_cmd
                record_metrics.main()

                self.assertTrue(log_path.exists())
                self.assertTrue(json_log_path.exists())
                text = log_path.read_text(encoding="utf-8")
                self.assertIn("Coverage total: 82%", text)
                payload = json.loads(json_log_path.read_text(encoding="utf-8"))
                self.assertEqual(payload[-1]["coverage_total"], 82)
                self.assertEqual(payload[-1]["assets_summary"]["total_assets"], 12)
            finally:
                record_metrics.REPO_ROOT = original_root
                record_metrics.LOG_PATH = original_log
                record_metrics.COV_JSON = original_cov
                record_metrics.ASSETS_REPORT = original_report
                record_metrics.time.time = original_time
                record_metrics.run_cmd = original_run_cmd

    def test_metrics_trend_main_writes_summary(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            metrics_path = repo_root / "docs" / "metrics_log.json"
            output_path = repo_root / "docs" / "metrics_trend.txt"
            metrics_path.parent.mkdir(parents=True, exist_ok=True)
            metrics_path.write_text(
                json.dumps(
                    [
                        {"timestamp": "2026-09-16T00:00:00Z", "coverage_total": 82.0},
                        {"timestamp": "2026-09-15T00:00:00Z", "coverage_total": 80.0},
                    ]
                ),
                encoding="utf-8",
            )

            original_log = metrics_trend.LOG_PATH
            original_output = metrics_trend.OUTPUT_PATH
            try:
                metrics_trend.LOG_PATH = metrics_path
                metrics_trend.OUTPUT_PATH = output_path
                metrics_trend.main()
                self.assertTrue(output_path.exists())
                content = output_path.read_text(encoding="utf-8")
                self.assertIn("Tendencia de cobertura", content)
                self.assertIn("82.0%", content)
            finally:
                metrics_trend.LOG_PATH = original_log
                metrics_trend.OUTPUT_PATH = original_output


    def test_make_bar_returns_full_bar_when_range_is_flat(self):
        self.assertEqual(metrics_trend.make_bar(5, 5, 5, width=3), "###")

    def test_load_entries_missing_file_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            missing = Path(tmpdir) / "metrics_log.json"
            original = metrics_trend.LOG_PATH
            metrics_trend.LOG_PATH = missing
            try:
                with self.assertRaises(FileNotFoundError):
                    metrics_trend.load_entries()
            finally:
                metrics_trend.LOG_PATH = original

    def test_load_entries_rejects_non_list_payload(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "metrics_log.json"
            path.write_text(json.dumps({"coverage_total": 80}), encoding="utf-8")
            original = metrics_trend.LOG_PATH
            metrics_trend.LOG_PATH = path
            try:
                with self.assertRaises(ValueError):
                    metrics_trend.load_entries()
            finally:
                metrics_trend.LOG_PATH = original

    def test_load_entries_skips_non_dict_items(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "metrics_log.json"
            path.write_text(
                json.dumps([{"coverage_total": 80}, "ruido", 42]), encoding="utf-8"
            )
            original = metrics_trend.LOG_PATH
            metrics_trend.LOG_PATH = path
            try:
                entries = metrics_trend.load_entries()
                self.assertEqual(entries, [{"coverage_total": 80}])
            finally:
                metrics_trend.LOG_PATH = original

    def test_main_rejects_empty_history(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "metrics_log.json"
            path.write_text(json.dumps([]), encoding="utf-8")
            original_log = metrics_trend.LOG_PATH
            original_output = metrics_trend.OUTPUT_PATH
            try:
                metrics_trend.LOG_PATH = path
                metrics_trend.OUTPUT_PATH = Path(tmpdir) / "metrics_trend.txt"
                with self.assertRaises(ValueError):
                    metrics_trend.main()
            finally:
                metrics_trend.LOG_PATH = original_log
                metrics_trend.OUTPUT_PATH = original_output

    def test_main_rejects_entries_without_coverage(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "metrics_log.json"
            path.write_text(
                json.dumps([{"timestamp": "2026-09-16T00:00:00Z", "commit": "abc"}]),
                encoding="utf-8",
            )
            original_log = metrics_trend.LOG_PATH
            original_output = metrics_trend.OUTPUT_PATH
            try:
                metrics_trend.LOG_PATH = path
                metrics_trend.OUTPUT_PATH = Path(tmpdir) / "metrics_trend.txt"
                with self.assertRaises(ValueError):
                    metrics_trend.main()
            finally:
                metrics_trend.LOG_PATH = original_log
                metrics_trend.OUTPUT_PATH = original_output


if __name__ == "__main__":
    unittest.main()
