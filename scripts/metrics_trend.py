#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = ROOT / "docs" / "metrics_log.json"
OUTPUT_PATH = ROOT / "docs" / "metrics_trend.txt"


def load_entries():
    if not LOG_PATH.exists():
        raise FileNotFoundError(f"No se encontró {LOG_PATH}")

    with LOG_PATH.open("r", encoding="utf-8") as handle:
        entries = json.load(handle)

    if not isinstance(entries, list):
        raise ValueError("metrics_log.json debe contener una lista de entradas")

    return [e for e in entries if isinstance(e, dict)]


def make_bar(value, min_value, max_value, width=30):
    if max_value <= min_value:
        return "#" * width
    ratio = (value - min_value) / (max_value - min_value)
    return "#" * int(round(ratio * width))


def main():
    entries = load_entries()
    if not entries:
        raise ValueError("No hay entradas en el historial para generar la tendencia")

    points = []
    for entry in entries:
        value = entry.get("coverage_total")
        if isinstance(value, (int, float)):
            points.append((entry.get("timestamp", "unknown"), float(value)))

    if not points:
        raise ValueError("No hay cobertura registrada para dibujar la tendencia")

    min_value = min(v for _, v in points)
    max_value = max(v for _, v in points)

    lines = ["Tendencia de cobertura (ultimas mediciones)", "=" * 48]
    for timestamp, value in points:
        date_label = timestamp[:10] if len(timestamp) >= 10 else timestamp
        bar = make_bar(value, min_value, max_value)
        lines.append(f"{date_label:<12} {value:>5.1f}% | {bar}")

    content = "\n".join(lines) + "\n"
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(content)
    print(f"\nResumen guardado en {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
