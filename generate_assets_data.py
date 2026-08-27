import json
from pathlib import Path

ASSETS_FILE = Path("assets.json")
MODELS_DIR = Path("models")


def format_name(filename):
    name = Path(filename).stem
    name = name.replace("_", " ").replace("-", " ")
    return name.title()


# Cargar assets existentes
with open(ASSETS_FILE, "r", encoding="utf-8") as f:
    assets = json.load(f)


# Modelos ya registrados
registered_files = {asset["file"] for asset in assets}


# Buscar modelos nuevos
new_assets = []

for model in sorted(MODELS_DIR.glob("*.glb")):
    relative_path = f"models/{model.name}"

    if relative_path in registered_files:
        continue

    asset = {
        "name": format_name(model.name),
        "file": relative_path,
        "category": "Props",
        "description": ""
    }

    assets.append(asset)
    new_assets.append(model.name)


# Guardar JSON actualizado
with open(ASSETS_FILE, "w", encoding="utf-8") as f:
    json.dump(assets, f, ensure_ascii=False, indent=2)


# Resultado
if new_assets:
    print(f"✓ Añadidos {len(new_assets)} modelos:")
    for model in new_assets:
        print(f"  - {model}")
else:
    print("✓ No hay modelos nuevos.")

print(f"\nTotal de assets: {len(assets)}")