import json
import tempfile
import unittest
from pathlib import Path

import generate_assets_data as generator


class GenerateAssetsDataTests(unittest.TestCase):
    def test_main_adds_new_model_and_uses_relative_paths(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            models_dir = tmp_path / "models"
            models_dir.mkdir()

            original_asset = {
                "name": "Existing Asset",
                "file": "models/existing.glb",
                "category": "Props",
                "description": "",
            }
            (tmp_path / "assets.json").write_text(
                json.dumps([original_asset], ensure_ascii=False),
                encoding="utf-8",
            )
            (models_dir / "existing.glb").write_text("existing", encoding="utf-8")
            (models_dir / "new_model.glb").write_text("new", encoding="utf-8")

            generator.BASE_DIR = tmp_path
            generator.ASSETS_FILE = tmp_path / "assets.json"
            generator.MODELS_DIR = models_dir

            generator.main()

            with generator.ASSETS_FILE.open("r", encoding="utf-8") as f:
                assets = json.load(f)

            self.assertEqual(len(assets), 2)
            self.assertIn("models/new_model.glb", {asset["file"] for asset in assets})
            self.assertEqual(assets[1]["name"], "New Model")
            self.assertIn("size_bytes", assets[1])
            self.assertIn("modified_at", assets[1])

    def test_warn_large_files(self):
        assets = [
            {"file": "models/small.glb", "size_bytes": 5 * 1024 * 1024},
            {"file": "models/big.glb", "size_bytes": 15 * 1024 * 1024},
            {"file": "models/huge.glb", "size_bytes": 150 * 1024 * 1024},
        ]

        warnings = generator.warn_large_files(assets)

        self.assertEqual(len(warnings), 2)
        self.assertTrue(any("10 MB" in warning for warning in warnings))
        self.assertTrue(any("100 MB" in warning for warning in warnings))

    def test_normalize_name_and_detect_name_duplicates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            models_dir = tmp_path / "models"
            models_dir.mkdir()
            (models_dir / "a.glb").write_text("a", encoding="utf-8")
            (models_dir / "b.glb").write_text("b", encoding="utf-8")

            assets = [
                {"name": "  my_asset__model  ", "file": "models/a.glb", "category": "Props", "description": ""},
                {"name": "My Asset Model", "file": "models/b.glb", "category": "Props", "description": ""},
            ]

            generator.BASE_DIR = tmp_path
            generator.MODELS_DIR = models_dir

            normalized_assets, issues = generator.validate_assets(assets)

            self.assertEqual(len(normalized_assets), 1)
            self.assertEqual(normalized_assets[0]["name"], "My Asset Model")
            self.assertTrue(any("Nombre duplicado" in issue for issue in issues))

    def test_generate_report_writes_json_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            report_path = tmp_path / "assets-report.json"

            generated_path = generator.generate_report(
                assets=[{"file": "models/example.glb", "size_bytes": 1000}],
                issues=["Archivo no encontrado: models/example.glb"],
                warnings=["[AVISO] models/example.glb supera 10 MB."],
                output_path=report_path,
            )

            self.assertEqual(generated_path, report_path)
            self.assertTrue(report_path.exists())
            payload = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["summary"]["issues"], 1)
            self.assertEqual(payload["summary"]["warnings"], 1)

    def test_validate_assets_flags_duplicates_and_missing_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            models_dir = tmp_path / "models"
            models_dir.mkdir()

            (models_dir / "asset1.glb").write_text("asset1", encoding="utf-8")

            assets = [
                {"name": "Asset 1", "file": "models/asset1.glb", "category": "Props", "description": ""},
                {"name": "Asset 1 Duplicate", "file": "models/asset1.glb", "category": "Props", "description": ""},
                {"name": "Missing", "file": "models/missing.glb", "category": "Props", "description": ""},
            ]

            generator.BASE_DIR = tmp_path
            generator.MODELS_DIR = models_dir

            normalized_assets, issues = generator.validate_assets(assets)

            self.assertEqual(len(normalized_assets), 1)
            self.assertTrue(any("duplicado" in issue.lower() for issue in issues))
            self.assertTrue(any("no encontrado" in issue.lower() for issue in issues))


if __name__ == "__main__":
    unittest.main()
