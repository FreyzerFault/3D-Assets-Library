import json
import tempfile
import unittest
from pathlib import Path

import generate_assets_data as generator


class GenerateAssetsDataMoreTests(unittest.TestCase):
    def setUp(self):
        # ensure tests are isolated by default
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmpdir.name)
        self.models_dir = self.tmp_path / "models"
        self.models_dir.mkdir()

        # point generator to temp directory
        generator.BASE_DIR = self.tmp_path
        generator.ASSETS_FILE = self.tmp_path / "assets.json"
        generator.MODELS_DIR = self.models_dir

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_load_assets_missing_returns_empty_list(self):
        # no assets.json created
        assets = generator.load_assets()
        self.assertEqual(assets, [])

    def test_load_assets_invalid_json_raises(self):
        (self.tmp_path / "assets.json").write_text(
            "{ not: valid json }", encoding="utf-8"
        )
        with self.assertRaises(json.JSONDecodeError):
            # load_assets will attempt to json.load and raise
            generator.load_assets()

    def test_normalize_file_path_handles_windows_backslashes(self):
        inp = "models\\subdir\\file.glb"
        out = generator.normalize_file_path(inp)
        self.assertEqual(out, "models/subdir/file.glb")

    def test_get_file_metadata_missing_returns_none_fields(self):
        meta = generator.get_file_metadata("models/missing.glb")
        self.assertIsNone(meta.get("size_bytes"))
        self.assertIsNone(meta.get("modified_at"))

    def test_collect_new_assets_ignores_non_glb_files(self):
        (self.models_dir / "readme.txt").write_text("txt", encoding="utf-8")
        (self.models_dir / "model.glb").write_text("glb", encoding="utf-8")

        assets, new = generator.collect_new_assets([])
        # should only add the .glb file
        self.assertIn("model.glb", new)
        self.assertTrue(any(a["file"].endswith("model.glb") for a in assets))

    def test_validate_assets_rejects_absolute_paths(self):
        # create a real file
        (self.models_dir / "a.glb").write_text("a", encoding="utf-8")
        abs_path = str((self.models_dir / "a.glb").resolve())

        assets = [
            {"name": "Abs", "file": abs_path, "category": "Props", "description": ""}
        ]
        normalized, issues = generator.validate_assets(assets)
        self.assertEqual(len(normalized), 0)
        self.assertTrue(
            any("Ruta absoluta" in i or "Ruta absoluta" in i for i in issues)
        )

    def test_warn_large_files_thresholds(self):
        one_exact = 10 * 1024 * 1024
        one_over = one_exact + 1
        hundred_exact = 100 * 1024 * 1024
        hundred_over = hundred_exact + 1

        assets = [
            {"file": "models/a.glb", "size_bytes": one_exact},
            {"file": "models/b.glb", "size_bytes": one_over},
            {"file": "models/c.glb", "size_bytes": hundred_over},
            {"file": "models/d.glb", "size_bytes": hundred_exact},
        ]

        warnings = generator.warn_large_files(assets)
        # one_exact and hundred_exact use > comparison so should NOT trigger
        self.assertTrue(any("b.glb" in w for w in warnings))
        self.assertTrue(any("c.glb" in w for w in warnings))
        self.assertFalse(any("a.glb" in w for w in warnings))

    def test_persist_and_load_roundtrip(self):
        data = [
            {
                "name": "X",
                "file": "models/x.glb",
                "category": "Props",
                "description": "",
            }
        ]
        generator.persist_assets(data)
        loaded = generator.load_assets()
        self.assertEqual(loaded, data)

    def test_generate_report_content_counts(self):
        report_path = self.tmp_path / "assets-report.json"
        assets = [{"file": "models/example.glb", "size_bytes": 1000}]
        issues = ["Missing: models/example.glb"]
        warnings = ["[AVISO] models/example.glb supera 10 MB."]

        out = generator.generate_report(
            assets, issues, warnings, output_path=report_path
        )
        self.assertEqual(out, report_path)
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["summary"]["total_assets"], 1)
        self.assertEqual(payload["summary"]["issues"], 1)
        self.assertEqual(payload["summary"]["warnings"], 1)


    def test_check_size_policy_flags_oversized_file_outside_large(self):
        assets = [{"file": "models/big.glb", "size_bytes": generator.LARGE_FILE_LIMIT + 1}]
        issues = generator.check_size_policy(assets)
        self.assertEqual(len(issues), 1)
        self.assertIn("models/large/", issues[0])

    def test_check_size_policy_flags_file_over_two_gb(self):
        assets = [
            {"file": "models/large/huge.glb", "size_bytes": generator.TWO_GB_LIMIT + 1}
        ]
        issues = generator.check_size_policy(assets)
        self.assertEqual(len(issues), 1)
        self.assertIn("models/2gb-plus/", issues[0])

    def test_check_size_policy_accepts_correctly_placed_files(self):
        assets = [
            {"file": "models/normal.glb", "size_bytes": generator.LARGE_FILE_LIMIT},
            {
                "file": "models/large/heavy.glb",
                "size_bytes": generator.LARGE_FILE_LIMIT + 1,
            },
            {
                "file": "models/2gb-plus/massive.glb",
                "size_bytes": generator.TWO_GB_LIMIT + 1,
            },
        ]
        self.assertEqual(generator.check_size_policy(assets), [])

    def test_check_size_policy_flags_undersized_file_in_large(self):
        assets = [{"file": "models/large/small.glb", "size_bytes": 10 * 1024 * 1024}]
        issues = generator.check_size_policy(assets)
        self.assertEqual(len(issues), 1)
        self.assertIn("puede volver a models/", issues[0])

    def test_check_size_policy_flags_undersized_file_in_two_gb(self):
        assets = [
            {"file": "models/2gb-plus/medium.glb", "size_bytes": 500 * 1024 * 1024}
        ]
        issues = generator.check_size_policy(assets)
        self.assertEqual(len(issues), 1)
        self.assertIn("models/2gb-plus/", issues[0])

    def test_check_size_policy_ignores_entries_without_size(self):
        assets = [{"file": "models/unknown.glb"}, {"file": "", "size_bytes": 5}]
        self.assertEqual(generator.check_size_policy(assets), [])

    def test_normalize_asset_keeps_normalized_tags(self):
        asset = {
            "name": "Espada",
            "file": "models/espada.glb",
            "category": "Armas",
            "description": "Prueba",
            "tags": ["  Low-Poly ", "ARMAS", "low-poly", "", 42, None],
        }
        normalized = generator.normalize_asset(asset)
        self.assertEqual(normalized["tags"], ["low-poly", "armas"])

    def test_normalize_asset_omits_empty_tags(self):
        asset = {
            "name": "X",
            "file": "models/x.glb",
            "category": "Props",
            "description": "",
        }
        normalized = generator.normalize_asset(asset)
        self.assertNotIn("tags", normalized)

    def test_normalize_asset_ignores_non_list_tags(self):
        asset = {
            "name": "X",
            "file": "models/x.glb",
            "category": "Props",
            "description": "",
            "tags": {"bad": True},
        }
        normalized = generator.normalize_asset(asset)
        self.assertNotIn("tags", normalized)

    def test_main_includes_policy_issues_in_report(self):
        big_size = generator.LARGE_FILE_LIMIT + 1
        (self.models_dir / "big.glb").write_text("big", encoding="utf-8")
        (self.tmp_path / "assets.json").write_text(
            json.dumps(
                [
                    {
                        "name": "Big",
                        "file": "models/big.glb",
                        "category": "Props",
                        "description": "",
                    }
                ],
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        original_metadata = generator.get_file_metadata
        original_report_file = generator.REPORT_FILE
        try:
            generator.REPORT_FILE = self.tmp_path / "assets-report.json"
            generator.get_file_metadata = lambda file_path: {
                "size_bytes": big_size,
                "modified_at": "2026-09-16T00:00:00+00:00",
            }
            generator.main(["--report"])
        finally:
            generator.get_file_metadata = original_metadata
            generator.REPORT_FILE = original_report_file

        report = json.loads(
            (self.tmp_path / "assets-report.json").read_text(encoding="utf-8")
        )
        policy_warnings = [w for w in report["warnings"] if "[POLITICA]" in w]
        self.assertEqual(len(policy_warnings), 1)
        self.assertIn("models/large/", policy_warnings[0])


if __name__ == "__main__":
    unittest.main()
