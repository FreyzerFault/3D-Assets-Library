import sys
import unittest
from pathlib import Path

import run_autopilot_loop


class RunAutopilotLoopTests(unittest.TestCase):
    def test_build_iteration_command_uses_runner(self):
        command = run_autopilot_loop.build_iteration_command(repo_root=Path("/tmp/project"))
        self.assertEqual(command[0], sys.executable)
        self.assertTrue(any("run_automation.py" in part for part in command))

    def test_post_message_to_webhook_uses_json_payload(self):
        class FakeResponse:
            status_code = 200
            text = "ok"

        fake_requests = type(
            "FakeRequests",
            (),
            {"post": staticmethod(lambda url, data, headers, timeout: FakeResponse())},
        )

        original_requests = run_autopilot_loop.requests
        run_autopilot_loop.requests = fake_requests
        try:
            ok, info = run_autopilot_loop.post_message_to_webhook(
                message="hola",
                webhook_url="https://example.com/hook",
                token="secret",
            )
            self.assertTrue(ok)
            self.assertIn("HTTP 200", info)
        finally:
            run_autopilot_loop.requests = original_requests

    def test_wait_for_stop_or_continue_returns_false_when_no_keypress(self):
        self.assertFalse(run_autopilot_loop.wait_for_stop_or_continue(0.05))


if __name__ == "__main__":
    unittest.main()
