# 3D Assets Library

![Coverage](https://img.shields.io/badge/coverage-reference-82%25-brightgreen)

Biblioteca estática de assets 3D para visualizar, revisar y descargar modelos `.glb` desde una web ligera sin backend.

Métricas del proyecto: [docs/METRICS.md](docs/METRICS.md)

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
│   ├── README.md
│   ├── large/
│   ├── projects/
│   └── 2gb-plus/   # ignorada por git; manejar con LFS o almacenamiento externo
├── tests/
├── docs/
│   ├── SPECIFICATIONS.md
│   ├── ARCHITECTURE.md
│   ├── METRICS.md
│   └── task.md
├── .github/
├── AGENTS.md
├── .gitignore
└── .vscode/
```

## Cómo usarlo

### Flujo manual

1. Añade un archivo `.glb` en `models/`.
2. Ejecuta:
   ```bash
   python generate_assets_data.py
   ```
3. Abre `index.html` en un navegador o sirve el proyecto con un servidor estático.

### Flujo único de automatización

Para lanzar la validación completa del proyecto con un solo clic en Windows:

- Haz doble clic en `run_automation.bat`
- O ejecuta desde consola:
  ```bash
  python run_automation.py
  ```

Este punto de entrada ejecuta, en orden, la regeneración del catálogo, la suite de tests y el registro de métricas del proyecto.


## Requisitos

- Python 3
- navegador moderno con soporte WebGL
- acceso a archivos locales o hosting estático

## Notas importantes

- El proyecto está pensado para despliegue estático.
- La ruta del catálogo y los modelos se resuelven respecto al propio script, no al directorio de trabajo.
- La organización de modelos sigue una política simple: `models/` para producción, `models/large/` para archivos >100 MB, `models/projects/` para fuentes de autoría y `models/2gb-plus/` para blobs mayores de 2 GB que deben gestionarse fuera del repositorio.
- La documentación técnica está en `docs/`.

## Estado actual

El proyecto está en una fase funcional y simple, orientada a catálogo y visualización, con una capa de calidad y métricas añadida para seguir evolucionando sin perder control. La siguiente evolución natural es consolidar la validación, seguir registrando la cobertura y preparar mejoras de UX o herramientas operativas según el crecimiento del catálogo.

## Mediciones del proyecto

- Registro de métricas: `docs/METRICS.md`
- Historial legible: `docs/metrics_log.md`
- Historial estructurado: `docs/metrics_log.json`
- Tendencia de cobertura: `docs/metrics_trend.txt`

> La badge de cobertura es un indicador de referencia del núcleo del generador. La medición oficial del proyecto se regenera con `scripts/record_metrics.py` y puede variar según qué archivos se incluyan en la medición.
