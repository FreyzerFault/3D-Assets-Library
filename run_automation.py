#!/usr/bin/env python3
"""Single-entry automation for the 3D asset library workflow.

This script runs the full local maintenance flow in one click:
1. regenerate the catalog from the model files
2. run the automated tests
3. record the latest project metrics
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent


def build_steps(repo_root=None):
    if repo_root is None:
        repo_root = REPO_ROOT

    return [
        (
            "Generación del catálogo",
            [sys.executable, str(repo_root / "generate_assets_data.py"), "--report"],
        ),
        (
            "Validación con tests",
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-v",
            ],
        ),
        (
            "Registro de métricas",
            [sys.executable, str(repo_root / "scripts" / "record_metrics.py")],
        ),
    ]


def run_step(name, command, repo_root=None):
    if repo_root is None:
        repo_root = REPO_ROOT

    print(f"\n=== {name} ===")
    result = subprocess.run(command, cwd=str(repo_root), check=False)
    if result.returncode != 0:
        print(f"[ERROR] '{name}' falló con código {result.returncode}.")
        raise SystemExit(result.returncode)
    print(f"[OK] '{name}' completado.")


def run_sequence(steps=None, repo_root=None):
    if repo_root is None:
        repo_root = REPO_ROOT
    if steps is None:
        steps = build_steps(repo_root=repo_root)

    for name, command in steps:
        run_step(name, command, repo_root=repo_root)

    return 0


def main():
    print("Inicio del flujo de automatización del proyecto.")
    print(f"Directorio del repositorio: {REPO_ROOT}")
    print("Se ejecutarán la generación del catálogo, tests y registro de métricas.")
    try:
        run_sequence(repo_root=REPO_ROOT)
    except SystemExit as exc:
        raise exc

    print("\n[OK] Todas las tareas de automatización han terminado correctamente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
