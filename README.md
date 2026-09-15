# 3D Assets Library

Biblioteca estática de assets 3D para visualizar, revisar y descargar modelos `.glb` desde una web ligera sin backend.

## Qué hace el proyecto

- muestra un catálogo de modelos 3D en navegador
- renderiza cada asset con un visor 3D usando `model-viewer`
- permite descargar cada archivo GLB directamente
- mantiene un catálogo centralizado en `assets.json`
- automatiza la detección de nuevos modelos con `generate_assets_data.py`

## Estructura del repositorio

```text
.
├── README.md
├── index.html
├── style.css
├── assets.json
├── generate_assets_data.py
├── models/
├── tests/
├── docs/
│   ├── SPECIFICATIONS.md
│   ├── ARCHITECTURE.md
│   └── task.md
├── .github/
├── AGENTS.md
└── .gitignore
```

## Cómo usarlo

1. Añade un archivo `.glb` en `models/`.
2. Ejecuta:
   ```bash
   python generate_assets_data.py
   ```
3. Abre `index.html` en un navegador o sirve el proyecto con un servidor estático.

## Requisitos

- Python 3
- navegador moderno con soporte WebGL
- acceso a archivos locales o hosting estático

## Notas importantes

- El proyecto está pensado para despliegue estático.
- La ruta del catálogo y los modelos se resuelven respecto al propio script, no al directorio de trabajo.
- La documentación técnica está en `docs/`.

## Estado actual

El proyecto está en una fase funcional y simple, orientada a catálogo y visualización. La siguiente evolución natural es añadir validación, metadata más rica y mejor UX de navegación.
