import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

import run_automation


class RunAutomationTests(unittest.TestCase):
    def test_build_steps_contains_expected_workflow(self):
        steps = run_automation.build_steps(repo_root=Path("/tmp/project"))
        self.assertEqual(len(steps), 3)
        self.assertEqual(steps[0][0], "Generación del catálogo")
        self.assertTrue(any("generate_assets_data.py" in part for part in steps[0][1]))
        self.assertEqual(steps[1][0], "Validación con tests")
        self.assertEqual(steps[2][0], "Registro de métricas")

    def test_run_sequence_stops_on_failure(self):
        failing_step = ("Paso de prueba", [sys.executable, "-c", "import sys; sys.exit(1)"])

        with patch("run_automation.subprocess.run", return_value=types.SimpleNamespace(returncode=1)) as mock_run:
            with self.assertRaises(SystemExit):
                run_automation.run_sequence([failing_step], repo_root=Path("/tmp/project"))
        mock_run.assert_called_once_with(
            failing_step[1],
            cwd=str(Path("/tmp/project")),
            check=False,
        )


    def test_build_steps_defaults_to_repository_root(self):
        steps = run_automation.build_steps()
        self.assertIn(str(run_automation.REPO_ROOT / "generate_assets_data.py"), steps[0][1])
        self.assertIn(str(run_automation.REPO_ROOT / "scripts" / "record_metrics.py"), steps[2][1])

    def test_run_step_completes_on_success(self):
        step = ("Paso correcto", [sys.executable, "-c", "print('ok')"])

        with patch("run_automation.subprocess.run", return_value=types.SimpleNamespace(returncode=0)) as mock_run:
            run_automation.run_step(*step, repo_root=Path("/tmp/project"))

        mock_run.assert_called_once_with(step[1], cwd=str(Path("/tmp/project")), check=False)

    def test_run_step_defaults_repo_root_to_repository_root(self):
        captured = {}

        def fake_subprocess_run(command, cwd=None, check=False):
            captured["cwd"] = cwd
            return types.SimpleNamespace(returncode=0)

        with patch("run_automation.subprocess.run", side_effect=fake_subprocess_run):
            run_automation.run_step("Paso", ["echo"])

        self.assertEqual(captured["cwd"], str(run_automation.REPO_ROOT))

    def test_run_sequence_runs_every_step(self):
        steps = [
            ("Primero", [sys.executable, "-c", "print(1)"]),
            ("Segundo", [sys.executable, "-c", "print(2)"]),
        ]

        with patch("run_automation.subprocess.run", return_value=types.SimpleNamespace(returncode=0)) as mock_run:
            result = run_automation.run_sequence(steps, repo_root=Path("/tmp/project"))

        self.assertEqual(result, 0)
        self.assertEqual(mock_run.call_count, 2)

    def test_run_sequence_defaults_repo_root_to_repository_root(self):
        captured = []

        def fake_run_step(name, command, repo_root=None):
            captured.append(repo_root)

        original = run_automation.run_step
        try:
            run_automation.run_step = fake_run_step
            run_automation.run_sequence([("Paso", ["echo"])])
        finally:
            run_automation.run_step = original

        self.assertEqual(captured, [run_automation.REPO_ROOT])

    def test_main_runs_sequence_and_returns_zero(self):
        calls = []

        def fake_run_sequence(steps=None, repo_root=None):
            calls.append(repo_root)
            return 0

        original = run_automation.run_sequence
        try:
            run_automation.run_sequence = fake_run_sequence
            result = run_automation.main()
        finally:
            run_automation.run_sequence = original

        self.assertEqual(result, 0)
        self.assertEqual(calls, [run_automation.REPO_ROOT])

    def test_main_propagates_sequence_failure(self):
        def fake_run_sequence(steps=None, repo_root=None):
            raise SystemExit(2)

        original = run_automation.run_sequence
        try:
            run_automation.run_sequence = fake_run_sequence
            with self.assertRaises(SystemExit):
                run_automation.main()
        finally:
            run_automation.run_sequence = original


if __name__ == "__main__":
    unittest.main()
