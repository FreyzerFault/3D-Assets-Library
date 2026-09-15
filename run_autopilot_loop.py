#!/usr/bin/env python3
"""Local autopilot loop for the 3D asset library.

Each iteration runs the project automation entry point and then restarts the loop
until the user interrupts it by pressing a key or closing the process.

Optional integrations:
- copy the prompt to the clipboard
- send the prompt to a webhook endpoint via HTTP POST
- open the chat URL configured in CHAT_URL
- show a desktop notification on Windows
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

DEFAULT_MESSAGE = (
    "Dios 3mendo, eres un genio. Sigue asi.\n"
    "Ponte modo autopilot infinito hasta que te pare.\n"
    "Revisa las tareas, actualizalas, genera mas tareas alineadas con las specs en orden de prioridad y diseccionalas en tareas pequeñas.\n"
    "Ponte a hacerlas todas, una tras otra sin parar siguiendo siempre las directrices de AGENTS.md logicamente.\n"
    "Y repite, vuelve a revisar y generar tareas, completalas, testea y repite..."
)

REPO_ROOT = Path(__file__).resolve().parent
AUTOMATION_CMD = [sys.executable, str(REPO_ROOT / "run_automation.py")]
CHAT_URL = os.environ.get("AUTOPILOT_CHAT_URL")
WEBHOOK_URL = os.environ.get("AUTOPILOT_WEBHOOK_URL")
WEBHOOK_TOKEN = os.environ.get("AUTOPILOT_WEBHOOK_TOKEN")
POLL_SECONDS = float(os.environ.get("AUTOPILOT_POLL_SECONDS", "2"))

try:
    import pyperclip
except Exception:  # pragma: no cover - optional dependency
    pyperclip = None

try:
    from win10toast import ToastNotifier
except Exception:  # pragma: no cover - optional dependency
    ToastNotifier = None

try:
    import requests
except Exception:  # pragma: no cover - optional dependency
    requests = None

try:
    import msvcrt
except Exception:  # pragma: no cover - Windows-only helper
    msvcrt = None


def build_iteration_command(repo_root=None):
    if repo_root is None:
        repo_root = REPO_ROOT
    return [sys.executable, str(Path(repo_root) / "run_automation.py")]


def copy_prompt_to_clipboard(message=DEFAULT_MESSAGE):
    if pyperclip is None:
        return False
    try:
        pyperclip.copy(message)
        return True
    except Exception:
        return False


def notify_windows(title, message, duration=6):
    if ToastNotifier is None:
        print(f"[NOTIFY] {title}: {message}")
        return False

    try:
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=duration, threaded=True)
        return True
    except Exception:
        return False


def post_message_to_webhook(message=DEFAULT_MESSAGE, webhook_url=None, token=None):
    if webhook_url is None:
        webhook_url = WEBHOOK_URL
    if not webhook_url:
        return False, "Webhook no configurado"
    if requests is None:
        return False, "requests no instalado"

    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.post(
            webhook_url,
            data=json.dumps({"message": message}),
            headers=headers,
            timeout=20,
        )
        if 200 <= response.status_code < 300:
            return True, f"HTTP {response.status_code}"
        return False, f"HTTP {response.status_code}: {response.text[:200]}"
    except Exception as exc:
        return False, f"request failed: {exc}"


def wait_for_stop_or_continue(delay_seconds):
    deadline = time.monotonic() + max(delay_seconds, 0.1)

    while time.monotonic() < deadline:
        if os.name == "nt" and msvcrt is not None and msvcrt.kbhit():
            try:
                msvcrt.getwch()
            except Exception:
                pass
            return True
        time.sleep(0.1)

    return False


def run_iteration(command=None):
    if command is None:
        command = build_iteration_command()

    print(f"\n=== Iteración del autopilot ===")
    result = subprocess.run(command, cwd=str(REPO_ROOT), check=False)
    return result.returncode


def main():
    iteration = 0
    print("Autopilot loop iniciado. Pulsa cualquier tecla para detenerlo o cierra la ventana.")
    while True:
        iteration += 1
        exit_code = run_iteration()
        status = "OK" if exit_code == 0 else f"ERROR ({exit_code})"
        print(f"[ITERACIÓN {iteration}] Estado: {status}")

        copied = copy_prompt_to_clipboard(DEFAULT_MESSAGE)
        if copied:
            print("[INFO] Mensaje copiado al portapapeles.")
        else:
            print("[INFO] Mensaje listo para pegar; portapapeles no disponible.")

        if CHAT_URL:
            try:
                import webbrowser

                webbrowser.open(CHAT_URL)
                print(f"[INFO] URL del chat abierta: {CHAT_URL}")
            except Exception as exc:  # pragma: no cover
                print(f"[WARN] No se pudo abrir la URL del chat: {exc}")

        success, info = post_message_to_webhook(DEFAULT_MESSAGE)
        if success:
            print(f"[WEBHOOK] {info}")
        else:
            print(f"[WEBHOOK] {info}")

        notify_windows(
            "Autopilot iteración completada",
            f"Iteración {iteration} terminada: {status}",
            duration=6,
        )

        if wait_for_stop_or_continue(POLL_SECONDS):
            print("\nParada solicitada por el usuario. Finalizando bucle.")
            break

    print("Autopilot loop finalizado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
