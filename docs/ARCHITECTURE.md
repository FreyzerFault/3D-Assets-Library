# Arquitectura actual

## Stack

- HTML5 + CSS + JavaScript vanilla
- `model-viewer` de Google cargado desde CDN
- Python 3 para la generación del catálogo
- `assets.json` como fuente de datos del frontend
- archivos `.glb` en `models/`
- despliegue estático (GitHub Pages o hosting equivalente)

## Estructura del proyecto

```text
.
├── README.md
├── CONTRIBUTING.md
├── index.html
├── style.css
├── assets.json
├── assets-report.json
├── generate_assets_data.py
├── run_automation.py
├── run_automation.bat
├── .pre-commit-config.yaml
├── .flake8
├── .coveragerc
├── .gitignore
├── .agents/
│   └── skills/            # flujos de trabajo para agentes
├── models/
│   ├── README.md
│   ├── large/
│   ├── projects/
│   └── 2gb-plus/          # fuera de git; gestionar con LFS o almacenamiento externo
├── scripts/
│   ├── record_metrics.py
│   └── metrics_trend.py
├── docs/
│   ├── SPECIFICATIONS.md
│   ├── ARCHITECTURE.md
│   ├── TESTING.md
│   ├── METRICS.md
│   ├── task.md
│   ├── task_archive.md
│   ├── metrics_log.md
│   ├── metrics_log.json
│   └── metrics_trend.txt
├── tests/
├── .github/
│   └── workflows/
├── .vscode/
└── AGENTS.md
```

## Componentes principales

### `index.html`

Es la capa de presentación. Carga `assets.json`, crea las tarjetas de los assets y renderiza cada visor 3D con `model-viewer`.

### `assets.json`

Es la fuente de verdad del catálogo visible. Contiene los assets que se muestran en la web y su metadata mínima.

### `generate_assets_data.py`

Script de mantenimiento que:

- detecta modelos nuevos en `models/`
- normaliza nombres y rutas
- valida entradas duplicadas o rotas
- detecta activos mal ubicados según la política de tamaño (`check_size_policy`)
- puede reubicarlos en disco con `--fix-large` (`fix_large_files`)
- actualiza `assets.json`

### `run_automation.py` y `run_automation.bat`

Punto único de acceso para la operación del repositorio. El flujo automatizado:

- genera el catálogo y el reporte de validación
- ejecuta la suite de tests
- escribe las métricas del proyecto

Esto reduce la fricción operativa para colaboradores y evita depender de varios comandos separados o de una consola de Python cada vez.

### `models/`

Directorio de archivos 3D. La política actual separa el contenido por uso y tamaño:

- `models/`: catálogo principal de assets listos para web.
- `models/large/`: activos >100 MB y <2 GB, aislados para facilitar revisión y control.
- `models/projects/`: proyectos fuente y materiales (`.blend`, `.fbx`, etc.).
- `models/2gb-plus/`: ecosistema reservado para activos >2 GB que se mantienen fuera del repositorio o con LFS.

## Flujo de ejecución

1. Se añade un archivo `.glb` a `models/`.
2. Se ejecuta `generate_assets_data.py`.
3. El script compara los archivos con el catálogo existente.
4. Se actualiza `assets.json` con nuevos assets si procede.
5. `index.html` hace `fetch('assets.json')` y renderiza la colección.
6. El navegador muestra el visor 3D y ofrece la descarga del modelo.

## Restricciones actuales

- no hay backend
- no hay base de datos de producción
- no hay autenticación real
- no hay pruebas automatizadas en la capa de negocio
- la metadata está contenida en JSON y no en un sistema estructurado
- el catálogo depende de la disciplina del usuario a la hora de añadir modelos y describirlos

## Dirección de evolución

La arquitectura actual es una base estática y simple. La evolución natural es separar mejor:

- contenido y metadata
- validación y catálogo
- publicación y mantenimiento
- gestión administrativa y visibilidad

Esto permite crecer hacia un catálogo más rico sin cambiar la base estática inicial.

## Opciones de arquitectura futuras (resumen y recomendaciones)

A continuación se almacenan las alternativas y recomendaciones discutidas para futuras evoluciones. Sirven como guía para decidir migraciones cuando la necesidad técnica las justifique.

1. Mantener estático y simple (recomendado por defecto)

- Frontend: HTML/CSS/JS estático que consume `assets.json`.
- Scripts: Python para exploración de ficheros, validación y generación de catálogo.
- Por qué: baja fricción, fácil mantenimiento, ideal para repositorios pequeños.
- Cuándo: catálogo pequeño, pocos colaboradores, sin necesidad de backend.

1. Crecer modularmente (si la base aumenta)

- Convertir scripts en paquete Python (ej: src/pygen) y exponer un CLI (entrypoint). Añadir pyproject.toml.
- Introducir linters (black, flake8), pruebas más completas y CI (GitHub Actions).
- Frontend: mantener estático pero modularizar; usar un bundler ligero (Vite) si crece la complejidad.
- Considerar migración gradual a pytest y mypy si se necesita mayor ergonomía de tests y type checking.

1. Unificar en JavaScript/TypeScript (cuando el equipo y los requisitos lo pidan)

- Ventaja: una sola stack para frontend y scripts si se prefiere unificar en Node.js.
- Coste: mayor tooling, menos ergonomía para operaciones del sistema en comparación con Python.
- Recomendación: sólo migrar si el equipo prefiere JS/TS y hay razones claras (p. ej. añadir lógica compartida que deba ejecutarse en node en producción).

1. Aplicación de escritorio para operación (opcional, herramienta de operador)

- Opción ligera: mantener la lógica en Python y crear GUI con PySide6 o CustomTkinter (rápido de implementar, integración directa con scripts actuales).
- Opción nativa/pulida: .NET (WPF/WinUI/MAUI) para apps Windows/ multiplataforma más «oficiales».
- Opción web híbrida: Electron/Tauri si se quiere UI web empaquetada (mayor coste en recursos).
- Recomendación: empezar con Python+PySide6 si la app es una herramienta local; migrar a .NET solo si se necesita experiencia Windows nativa y se justifica el coste.

1. CI / calidad y ergonomía de desarrollo

- Recomendado: GitHub Actions que ejecute linter y tests en cada PR.
- Mantener TESTING.md y AGENTS.md sincronizados con la política de ejecución de tests.

1. Herramientas complementarias

- Blender: imprescindible para validar/editar modelos `.glb` (herramienta de contenido, no IDE del repo).
- PyCharm / VS Code / WebStorm: elegir según foco (Python-heavy → PyCharm; frontend-heavy → WebStorm; equilibrio y agente work → VS Code).

Criterios para decidir migraciones

- Migrar solo cuando haya una ganancia clara en productividad, colaboración o rendimiento.
- Priorizar migraciones incrementales: empaquetar scripts, añadir CI, refactorizar en módulos, luego considerar cambio de lenguaje o GUI.
- Documentar cada migración en docs/ARCHITECTURE.md y docs/task.md, y actualizar AGENTS.md para las nuevas reglas operativas.

---

Las opciones y recomendaciones anteriores quedan registradas aquí para referencia futura. Si quieres, puedo extraerlas además a un archivo separado (docs/ARCHITECTURE_OPTIONS.md) o añadir entradas en SPECIFICATIONS.md y AGENTS.md para hacerlas ejecutables por agentes.
