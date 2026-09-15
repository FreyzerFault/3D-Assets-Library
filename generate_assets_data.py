import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_FILE = BASE_DIR / "assets.json"
MODELS_DIR = BASE_DIR / "models"


def format_name(filename):
    name = Path(filename).stem
    name = name.replace("_", " ").replace("-", " ")
    name = " ".join(name.split())
    return name.title()


def normalize_file_path(file_path):
    return str(file_path).replace("\\", "/").strip()


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


def normalize_asset(asset, default_category="Props"):
    if not isinstance(asset, dict):
        return None

    name = str(asset.get("name", "") or "").strip()
    if not name:
        file_path = asset.get("file")
        name = format_name(file_path) if file_path else "Asset"

    category = str(asset.get("category") or default_category).strip() or default_category
    description = str(asset.get("description") or "").strip()

    file_path = normalize_file_path(asset.get("file", ""))
    if not file_path:
        return None

    return {
        "name": name,
        "file": file_path,
        "category": category,
        "description": description,
    }


def validate_assets(assets, models_dir=None):
    if models_dir is None:
        models_dir = MODELS_DIR

    issues = []
    seen_files = set()
    normalized_assets = []

    for index, asset in enumerate(assets):
        normalized = normalize_asset(asset)
        if normalized is None:
            issues.append(f"Entrada #{index + 1} no tiene un archivo valido.")
            continue

        if normalized["file"] in seen_files:
            issues.append(f"Archivo duplicado: {normalized['file']}")
            continue

        seen_files.add(normalized["file"])

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

        asset = {
            "name": format_name(model.name),
            "file": normalized_path,
            "category": "Props",
            "description": "",
        }

        assets.append(asset)
        new_assets.append(model.name)

    return assets, new_assets


def main():
    assets = load_assets()
    assets, issues = validate_assets(assets)

    if issues:
        print("[WARN] Se detectaron problemas en assets.json:")
        for issue in issues:
            print(f"  - {issue}")

    assets, new_assets = collect_new_assets(assets)

    with ASSETS_FILE.open("w", encoding="utf-8") as f:
        json.dump(assets, f, ensure_ascii=False, indent=2)

    if new_assets:
        print(f"[OK] Agregados {len(new_assets)} modelos:")
        for model in new_assets:
            print(f"  - {model}")
    else:
        print("[OK] No hay modelos nuevos.")

    print(f"\nTotal de assets: {len(assets)}")


if __name__ == "__main__":
    main()