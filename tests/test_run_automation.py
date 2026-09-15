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


if __name__ == "__main__":
    unittest.main()
