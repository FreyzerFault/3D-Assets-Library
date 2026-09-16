# Archivo de tareas completadas

Histórico de tareas cerradas del proyecto. La cola activa vive en `docs/task.md`; aquí solo se conserva lo ya hecho, con la evidencia que lo demuestra.

Regla: al cerrar una tarea, moverla desde `docs/task.md` a este fichero con su DoD cumplido y la evidencia verificable (fichero, comando o test).

---

## Calidad y agent tooling

- [x] T7 — Descriptions reales en el frontmatter de los SKILL.md
  - Qué: los tres `SKILL.md` llevaban `description: Brief description of what this skill does` como marcador de posición, y sus secciones `## Usage` eran frases sueltas poco informativas.
    - DoD: cada `SKILL.md` describe en una línea qué hace y cuándo usarla, sin marcadores de posición.
  - Evidencia: `.agents/skills/implement-task/SKILL.md`, `.agents/skills/project-review/SKILL.md` y `.agents/skills/test-and-verify/SKILL.md` ahora tienen descripciones concretas en el frontmatter y secciones `## Usage` descriptivas. Verificado con búsqueda de `Brief description` en el repositorio (0 coincidencias restantes).

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
- [x] Categorías reales y tags por asset (Media)
  - Qué: definir categorías útiles y soportar tags por asset en `assets.json` y en la UI.
  - Evidencia: `normalize_tags` en `generate_assets_data.py` (normaliza, deduplica y omite la clave si queda vacía) con 3 tests; chips de tags en `index.html` construidos con `textContent`; 28 assets reclasificados en 8 categorías (Personajes 10, Anatomía 5, Armas 5, Props 3, Arquitectura 2, Criaturas 1, Robótica 1, Vehículos 1) y 26 con tags. Suite en verde con **44 tests, OK**; script validado con `node --check`; modelo de datos documentado en `docs/SPECIFICATIONS.md`.
- [x] Verificar la política de archivos grandes (Media)
  - Qué: comprobación reproducible que detecte activos mal ubicados según la política (`models/large/` para >100 MB, `models/2gb-plus/` para >2 GB) y avise con instrucciones.
  - Evidencia: `check_size_policy` en `generate_assets_data.py`, integrada en `main()` y en `assets-report.json`; 7 tests nuevos (`test_check_size_policy_*` y `test_main_includes_policy_issues_in_report`), suite en verde con **41 tests, OK**. El catálogo real (28 assets) no genera avisos de política. El test de aceptación destapó un bug de la primera implementación (un fichero correcto en `models/2gb-plus/` se marcaba como mal ubicado), corregido antes de cerrar la tarea.

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

- [x] Cubrir los caminos de error de los scripts operativos (Alta)
  - Qué: tests para los caminos de error de `record_metrics.py`, `metrics_trend.py` y `run_automation.py`.
  - Evidencia: 13 tests nuevos; suite en verde con **34 tests, OK** (`python -m unittest discover -s tests -v`). Cobertura por fichero (`coverage.json`): `run_automation.py` 92%, `scripts/metrics_trend.py` 97%, `scripts/record_metrics.py` 75%, todos por encima del umbral `fail_under = 70` de `.coveragerc`; cobertura total 83%.
  - Nota: `record_metrics.py` se ejecutó dos veces en la misma sesión y dejó dos entradas consecutivas en `docs/metrics_log.md`; es un artefacto de la sesión, no del pipeline.
- [x] Registro de métricas y tendencia (Alta)
  - Evidencia: `scripts/record_metrics.py` (historial legible + `docs/metrics_log.json`), `scripts/metrics_trend.py` (`docs/metrics_trend.txt`) y `docs/METRICS.md`.
- [x] Documentar la métrica de cobertura de referencia
  - Evidencia: sección "Métrica de cobertura de referencia" en `docs/METRICS.md`; badge del README marcado como referencia, no como cobertura global.
- [x] Punto único de automatización (Alta)
  - Evidencia: `run_automation.py` y `run_automation.bat` encadenan generación, tests y métricas con un solo clic.

## Web y UX

- [x] Búsqueda y filtros en la web (Media)
  - Qué: filtro por categoría y búsqueda por nombre sobre `assets.json`, integrados con la paginación existente.
  - Evidencia: sección `#controls` en `index.html` con input de búsqueda, select de categorías poblado desde el catálogo y contador de resultados. Filtrado sin recargar (`applyFilters`, insensible a mayúsculas y acentos) que reinicia la paginación (`resetRenderedAssets`) y vuelve a renderizar por bloques de `PAGE_SIZE` manteniendo el botón y el sentinel; mensaje vacío cuando no hay coincidencias. Las tarjetas se insertan ahora antes del botón "Cargar más" para no romper el orden del grid al paginar. Sintaxis del script validada con `node --check`; el proyecto no tiene tooling de pruebas de navegador.

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