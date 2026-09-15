#!/usr/bin/env python3
"""Example webhook receiver that can receive the autopilot loop message.

Usage:
  python scripts/autopilot_webhook_server.py

Then POST to http://localhost:8765/autopilot with JSON payload:
  { "message": "..." }

Optional env vars:
  AUTOPILOT_WEBHOOK_HOST=0.0.0.0
  AUTOPILOT_WEBHOOK_PORT=8765
  AUTOPILOT_WEBHOOK_TOKEN=secret-token
"""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

try:
    from win10toast import ToastNotifier
except Exception:  # pragma: no cover - optional dependency
    ToastNotifier = None

HOST = os.environ.get("AUTOPILOT_WEBHOOK_HOST", "0.0.0.0")
PORT = int(os.environ.get("AUTOPILOT_WEBHOOK_PORT", "8765"))
EXPECTED_TOKEN = os.environ.get("AUTOPILOT_WEBHOOK_TOKEN")


def notify_windows(title, message):
    if ToastNotifier is None:
        print(f"[NOTIFY] {title}: {message}")
        return
    try:
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=6, threaded=True)
    except Exception:
        print(f"[NOTIFY] {title}: {message}")


class AutopilotWebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            payload = {
                "status": "ok",
                "endpoints": ["/autopilot"],
                "usage": "Use POST /autopilot with a JSON body: {\"message\": \"...\"}",
            }
            self._send_json(200, payload)
            return
        self._send_json(404, {"status": "not_found"})

    def do_POST(self):
        if self.path != "/autopilot":
            self._send_json(404, {"status": "not_found"})
            return

        auth = self.headers.get("Authorization", "")
        if EXPECTED_TOKEN and auth != f"Bearer {EXPECTED_TOKEN}":
            self._send_json(401, {"status": "unauthorized"})
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length)

        try:
            payload = json.loads(raw.decode("utf-8"))
        except Exception:
            self._send_json(400, {"status": "invalid_json"})
            return

        message = payload.get("message") or ""
        if not isinstance(message, str) or not message.strip():
            self._send_json(400, {"status": "missing_message"})
            return

        print(f"[WEBHOOK] {message}")
        notify_windows("Autopilot webhook", message)
        self._send_json(200, {"status": "received", "message": message})

    def log_message(self, format, *args):
        return

    def _send_json(self, status_code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    server = ThreadingHTTPServer((HOST, PORT), AutopilotWebhookHandler)
    print(f"Autopilot webhook server listening on http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nWebhook server stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
