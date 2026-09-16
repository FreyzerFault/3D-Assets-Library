# Archivo de tareas completadas

Histórico de tareas cerradas del proyecto. La cola activa vive en `docs/task.md`; aquí solo se conserva lo ya hecho, con la evidencia que lo demuestra.

Regla: al cerrar una tarea, moverla desde `docs/task.md` a este fichero con su DoD cumplido y la evidencia verificable (fichero, comando o test).

---

## Fundamentos del catálogo

- [x] Resolución de rutas relativa al script
  - Evidencia: `BASE_DIR` en `generate_assets_data.py`; catálogo y modelos se resuelven respecto al script, no al directorio de ejecución.
- [x] Normalización de nombres y rutas en `assets.json`
  - Evidencia: `normalize_name`, `format_name` y `normalize_file_path` convierten `\` en `/` y normalizan a formato título.
- [x] Validación de duplicados y archivos faltantes
  - Evidencia: `validate_assets` reporta archivo duplicado, nombre duplicado, ruta absoluta y fichero no encontrado.
- [x] Metadata operativa y tamaño (Alta)
  - Qué: añadir `size_bytes` y `modified_at` al catálogo.
  - Evidencia: `normalize_asset` rellena ambos campos y `warn_large_files` avisa por encima de 10 MB y 100 MB (`LARGE_FILE_WARNINGS`).
- [x] Política de naming y normalización (Alta)
  - Evidencia: nombres normalizados en formato título y conflictos detectados tras normalizar.
- [x] Validación y reporting (Media)
  - Evidencia: `python generate_assets_data.py --report` genera `assets-report.json` con listas `errors` y `warnings` y resumen de conteos.

## Tests y calidad

- [x] Tests de smoke del generador
  - Evidencia: `tests/test_generate_assets_data.py`.
- [x] Tests ampliados del generador
  - Evidencia: `tests/test_generate_assets_data_more.py` (rutas Windows, umbrales exactos de tamaño, JSON inválido, roundtrip de persistencia, rechazo de rutas absolutas).
- [x] Tests de regresión para scripts de métricas (Media)
  - Evidencia: `tests/test_metrics_scripts.py`, en verde dentro de la suite de 21 tests.
- [x] Calidad local y cobertura (Alta)
  - Evidencia: `.pre-commit-config.yaml` (black + flake8), `.flake8`, `.coveragerc` con `fail_under = 70` y job de cobertura en CI.
- [x] CI de generación y validación (Baja)
  - Evidencia: `.github/workflows/ci.yml` con jobs encadenados lint → test → validate.

## Automatización y métricas

- [x] Registro de métricas y tendencia (Alta)
  - Evidencia: `scripts/record_metrics.py` (historial legible + `docs/metrics_log.json`), `scripts/metrics_trend.py` (`docs/metrics_trend.txt`) y `docs/METRICS.md`.
- [x] Documentar la métrica de cobertura de referencia
  - Evidencia: sección "Métrica de cobertura de referencia" en `docs/METRICS.md`; badge del README marcado como referencia, no como cobertura global.
- [x] Punto único de automatización (Alta)
  - Evidencia: `run_automation.py` y `run_automation.bat` encadenan generación, tests y métricas con un solo clic.

## Web y UX

- [x] Paginación y carga diferida (Media)
  - Evidencia: `index.html` con `PAGE_SIZE = 6`, botón "Cargar más" e `IntersectionObserver` que asigna `model.src` solo cuando el visor entra en pantalla.

## Despliegue y repositorio

- [x] Despliegue automático a GitHub Pages (Baja)
  - Evidencia: `.github/workflows/deploy-pages.yml`.
- [x] Higiene del repositorio y artefactos locales (Media)
  - Evidencia: `.gitignore` excluye `__pycache__`, `*.py[cod]` y artefactos de cobertura; los `.pyc` que estaban rastreados se retiraron del índice de git.
- [x] Reconciliar el árbol de `docs/` en ARCHITECTURE.md
  - Qué: el árbol de `docs/ARCHITECTURE.md` listaba `metrics_log.md` pero omitía `TESTING.md`, `metrics_log.json`, `metrics_trend.txt` y `task_archive.md`.
  - Evidencia: el árbol refleja ahora los 9 ficheros reales de `docs/`. Se completó además el árbol raíz con los ficheros que faltaban (`CONTRIBUTING.md`, `assets-report.json`, `.pre-commit-config.yaml`, `.flake8`, `.coveragerc`, `.agents/`, contenido de `scripts/` y `.github/workflows/`).
- [x] Normalizar las rutas de documentación en los SKILL.md
  - Qué: los tres `SKILL.md` de `.agents/skills/` referenciaban `docs/architecture.md`, `docs/specifications.md`, `docs/testing.md` y `docs/metrics.md` en minúsculas.
  - Evidencia: los tres ficheros usan ahora los nombres reales (`docs/ARCHITECTURE.md`, `docs/SPECIFICATIONS.md`, `docs/TESTING.md`, `docs/METRICS.md`); verificado con búsqueda en el repositorio. Se corrigió además la cabecera `## Steps` vacía de `implement-task/SKILL.md`, que tenía los pasos bajo un `## Objective` mal colocado.
- [x] Retirar la feature descartada de autopilot
  - Evidencia: sin referencias a `run_autopilot_loop` ni `autopilot_webhook_server` en el repositorio.

---

Última actualización: 2026-09-16