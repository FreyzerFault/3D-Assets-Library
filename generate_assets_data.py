import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_FILE = BASE_DIR / "assets.json"
MODELS_DIR = BASE_DIR / "models"
REPORT_FILE = BASE_DIR / "assets-report.json"
LARGE_FILE_WARNINGS = (10 * 1024 * 1024, 100 * 1024 * 1024)
LARGE_FILE_LIMIT = LARGE_FILE_WARNINGS[1]
TWO_GB_LIMIT = 2 * 1024 * 1024 * 1024

# region File and metadata utilities


def normalize_name(value):
    name = str(value or "").strip()
    name = name.replace("_", " ").replace("-", " ")
    name = re.sub(r"\s+", " ", name)
    return name.title() if name else ""


def format_name(filename):
    name = Path(filename).stem
    return normalize_name(name)


def normalize_file_path(file_path):
    return str(file_path).replace("\\", "/").strip()


def get_file_metadata(file_path):
    resolved_path = (BASE_DIR / file_path).resolve()
    if not resolved_path.exists():
        return {"size_bytes": None, "modified_at": None}

    stat = resolved_path.stat()
    return {
        "size_bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(
            stat.st_mtime, tz=timezone.utc
        ).isoformat(),
    }


def load_assets(path=None):
    if path is None:
        path = ASSETS_FILE

    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(f"{path.name} debe contener una lista JSON de assets.")

    return data


# endregion

# region Asset normalization and validation


def normalize_tags(value):
    if isinstance(value, str):
        value = [value]

    if not isinstance(value, list):
        return []

    tags = []
    for tag in value:
        if not isinstance(tag, str):
            continue

        normalized = re.sub(r"\s+", " ", tag.strip().lower())
        if normalized and normalized not in tags:
            tags.append(normalized)

    return tags


def normalize_asset(asset, default_category="Props"):
    if not isinstance(asset, dict):
        return None

    file_path = normalize_file_path(asset.get("file", ""))
    if not file_path:
        return None

    name = normalize_name(asset.get("name"))
    if not name:
        name = format_name(file_path)

    category = normalize_name(asset.get("category") or default_category)
    if not category:
        category = default_category

    description = str(asset.get("description") or "").strip()

    normalized = {
        "name": name,
        "file": file_path,
        "category": category,
        "description": description,
    }

    tags = normalize_tags(asset.get("tags"))
    if tags:
        normalized["tags"] = tags

    metadata = get_file_metadata(file_path)
    if metadata["size_bytes"] is not None:
        normalized["size_bytes"] = metadata["size_bytes"]
    if metadata["modified_at"] is not None:
        normalized["modified_at"] = metadata["modified_at"]

    return normalized


def validate_assets(assets, models_dir=None):
    if models_dir is None:
        models_dir = MODELS_DIR

    issues = []
    seen_files = set()
    seen_names = set()
    normalized_assets = []

    for index, asset in enumerate(assets):
        normalized = normalize_asset(asset)
        if normalized is None:
            issues.append(f"Entrada #{index + 1} no tiene un archivo valido.")
            continue

        if normalized["file"] in seen_files:
            issues.append(f"Archivo duplicado: {normalized['file']}")
            continue

        if normalized["name"] in seen_names:
            issues.append(f"Nombre duplicado: {normalized['name']}")
            continue

        seen_files.add(normalized["file"])
        seen_names.add(normalized["name"])

        if Path(normalized["file"]).is_absolute() or normalized["file"].startswith("/"):
            issues.append(f"Ruta absoluta no permitida: {normalized['file']}")
            continue

        absolute_path = (BASE_DIR / normalized["file"]).resolve()
        if normalized["file"].startswith("models/") and not absolute_path.exists():
            issues.append(f"Archivo no encontrado: {normalized['file']}")
            continue

        normalized_assets.append(normalized)

    return normalized_assets, issues


def collect_new_assets(assets, models_dir=None):
    if models_dir is None:
        models_dir = MODELS_DIR

    registered_files = {normalize_file_path(asset["file"]) for asset in assets}
    new_assets = []

    for model in sorted(models_dir.glob("*.glb")):
        relative_path = f"models/{model.name}"
        normalized_path = normalize_file_path(relative_path)

        if normalized_path in registered_files:
            continue

        metadata = get_file_metadata(normalized_path)
        asset = {
            "name": format_name(model.name),
            "file": normalized_path,
            "category": "Props",
            "description": "",
        }

        for key, value in metadata.items():
            if value is not None:
                asset[key] = value

        assets.append(asset)
        new_assets.append(model.name)

    return assets, new_assets


# endregion

# region Reporting and CLI


def warn_large_files(assets):
    warnings = []

    for asset in assets:
        size_bytes = asset.get("size_bytes")
        if not isinstance(size_bytes, int):
            continue

        if size_bytes > LARGE_FILE_WARNINGS[1]:
            warnings.append(
                f"[ALERTA] {asset['file']} supera 100 MB ({size_bytes / (1024 * 1024):.1f} MB)."
            )
        elif size_bytes > LARGE_FILE_WARNINGS[0]:
            warnings.append(
                f"[AVISO] {asset['file']} supera 10 MB ({size_bytes / (1024 * 1024):.1f} MB)."
            )

    return warnings


def check_size_policy(assets):
    """Comprueba que cada activo vive en la carpeta que indica su tamaño."""
    policy_issues = []

    for asset in assets:
        file_path = asset.get("file", "")
        size_bytes = asset.get("size_bytes")
        if not file_path or not isinstance(size_bytes, int):
            continue

        size_mb = size_bytes / (1024 * 1024)
        size_gb = size_bytes / (1024 * 1024 * 1024)
        in_large = file_path.startswith("models/large/")
        in_two_gb = file_path.startswith("models/2gb-plus/")

        if size_bytes > TWO_GB_LIMIT and not in_two_gb:
            policy_issues.append(
                f"[POLITICA] {file_path} supera 2 GB ({size_gb:.1f} GB); debe vivir en "
                "models/2gb-plus/ fuera del repositorio (LFS o almacenamiento externo)."
            )
        elif size_bytes > LARGE_FILE_LIMIT and not in_large and not in_two_gb:
            policy_issues.append(
                f"[POLITICA] {file_path} supera 100 MB ({size_mb:.1f} MB); muévelo a models/large/."
            )
        elif in_large and size_bytes <= LARGE_FILE_LIMIT:
            policy_issues.append(
                f"[POLITICA] {file_path} está en models/large/ con {size_mb:.1f} MB; "
                "puede volver a models/."
            )
        elif in_two_gb and size_bytes <= TWO_GB_LIMIT:
            policy_issues.append(
                f"[POLITICA] {file_path} está en models/2gb-plus/ con {size_gb:.1f} GB; "
                "debe estar en models/large/ (o en models/ si no supera 100 MB)."
            )

    return policy_issues


def generate_report(assets, issues, warnings, output_path=None):
    if output_path is None:
        output_path = REPORT_FILE

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_assets": len(assets),
            "issues": len(issues),
            "warnings": len(warnings),
        },
        "errors": issues,
        "warnings": warnings,
    }

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return output_path


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Genera y valida el catálogo de assets 3D."
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Genera un assets-report.json con errores y warnings.",
    )
    return parser.parse_args(argv)


def persist_assets(assets):
    with ASSETS_FILE.open("w", encoding="utf-8") as f:
        json.dump(assets, f, ensure_ascii=False, indent=2)


def main(argv=None):
    args = parse_args([] if argv is None else argv)
    assets = load_assets()
    assets, issues = validate_assets(assets)

    if issues:
        print("[WARN] Se detectaron problemas en assets.json:")
        for issue in issues:
            print(f"  - {issue}")

    assets, new_assets = collect_new_assets(assets)
    warnings = warn_large_files(assets)
    policy_issues = check_size_policy(assets)

    if warnings:
        print("\n[WARN] Archivos grandes detectados:")
        for warning in warnings:
            print(f"  - {warning}")

    if policy_issues:
        print("\n[WARN] Activos que no cumplen la política de archivos grandes:")
        for issue in policy_issues:
            print(f"  - {issue}")

    persist_assets(assets)

    if args.report:
        report_path = generate_report(assets, issues, warnings + policy_issues)
        print(f"\n[OK] Reporte generado: {report_path.name}")

    if new_assets:
        print(f"\n[OK] Agregados {len(new_assets)} modelos:")
        for model in new_assets:
            print(f"  - {model}")
    else:
        print("\n[OK] No hay modelos nuevos.")

    print(f"\nTotal de assets: {len(assets)}")


# endregion


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
