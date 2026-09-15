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
                                "percent_covered": 88.5,
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
                json.dumps([
                    {"timestamp": "2026-09-16T00:00:00Z", "coverage_total": 82.0},
                    {"timestamp": "2026-09-15T00:00:00Z", "coverage_total": 81.8},
                ])
            )
            original = metrics_trend.LOG_PATH
            metrics_trend.LOG_PATH = metrics_path
            try:
                entries = metrics_trend.load_entries()
                self.assertEqual(len(entries), 2)
                self.assertEqual(entries[0]["coverage_total"], 82.0)
            finally:
                metrics_trend.LOG_PATH = original


if __name__ == "__main__":
    unittest.main()
