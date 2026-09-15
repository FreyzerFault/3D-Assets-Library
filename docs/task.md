# Backlog y Snapshot (versión SDD, resumida)

## Snapshot breve

- Proyecto: Biblioteca estática de assets 3D.
- Stack: HTML/CSS/JS (frontend), `model-viewer` (visor), Python 3 (scripts), `assets.json` (catálogo), `models/` (GLB).
- Estado: prototipo funcional, catálogo con ~28 assets, validación normalizada, seguimiento de métricas y calidad local automatizada.
- Calidad: suite de tests estable, cobertura registrada en docs/metrics_log.json, scripts de registro/monitorización añadidos y flujos de validación preparados.

## Trabajo completado (evidencia)

- Resolución de rutas relativa al script (BASE_DIR). (`generate_assets_data.py`)
- Normalización de nombres y rutas en `assets.json`.
- Añadidos tests de smoke que pasan (`tests/test_generate_assets_data.py`).
- Validación básica de duplicados y archivos faltantes.
- Metadata operativa añadida: `size_bytes` y `modified_at` para cada asset, con avisos por archivos >10 MB y >100 MB.

## Prioridad actual (próximo sprint)

Ordenado por impacto y coste (alta → baja). Cada ítem incluye criterio de aceptación (DoD).

- [COMPLETADO] Metadata operativa y tamaño (Alta)
  - Qué: extraer tamaño de archivo, fecha de modificación y añadir campos `size_bytes`, `modified_at` al catálogo.
  - Por qué: detectar assets pesados y habilitar filtros/umbrales.
  - DoD cumplido: `generate_assets_data.py` añade `size_bytes` y `modified_at`; el script reporta avisos para archivos >10MB y >100MB.

- [COMPLETADO] Política de naming y normalización (Alta)
  - Qué: definir y aplicar reglas simples de limpieza de nombres y detectar conflictos tras normalizar.
  - DoD cumplido: el script normaliza `name` y `file`, elimina espacios redundantes y reporta nombres duplicados tras la normalización.

- [COMPLETADO] Validación y reporting (Media)
  - Qué: mejorar mensajes de validación, salida CLI y generar un `assets-report.json` con issues detectados.
  - DoD cumplido: ejecución `python generate_assets_data.py --report` genera `assets-report.json` con listas `errors` y `warnings`.

- [COMPLETADO] UX móvil: paginación / lazy loading (Media)
  - Qué: implementar paginación simple + lazy-loading de visores para reducir consumo en móviles.
  - DoD cumplido: la vista carga un bloque inicial de assets, permite cargar más y retarda la carga del `model-viewer` hasta que entra en pantalla.

- [COMPLETADO] CI de generación y validación (Baja)
  - Qué: añadir workflow de GitHub Actions que ejecute los tests y valide que el catálogo y el reporte se regeneran correctamente.
  - DoD cumplido: existe `.github/workflows/ci.yml`, con ejecución automática en push/PR y validación del catálogo y `assets-report.json`.

- [COMPLETADO] Despliegue automático a GitHub Pages (Baja)
  - Qué: preparar un workflow que publique el sitio estático completo en GitHub Pages.
  - DoD cumplido: existe `.github/workflows/deploy-pages.yml` para despliegue manual o automático desde la rama principal.

- [COMPLETADO] Calidad local y cobertura (Alta)
  - Qué: añadir pre-commit para lint/format y un job de coverage en CI con artefacto local.
  - Por qué: evitar regresiones pequeñas, mantener el código legible y documentar el nivel de cobertura real.
  - DoD cumplido: existen `.pre-commit-config.yaml`, `.flake8`, `.coveragerc` y el workflow CI ejecuta lint + coverage + validación del catálogo.

- [COMPLETADO] Registro de métricas y tendencia (Alta)
  - Qué: añadir scripts para registrar cobertura, generar un log histórico y producir una tendencia ASCII legible.
  - Por qué: monitorizar el progreso del proyecto con historial de tests y cobertura sin quitar sencillez ni complejidad.
  - DoD cumplido: existen `scripts/record_metrics.py`, `scripts/metrics_trend.py`, `docs/METRICS.md`, `docs/metrics_log.md` y `docs/metrics_log.json`.

- [COMPLETADO] Punto único de automatización (Alta)
  - Qué: añadir `run_automation.py` y `run_automation.bat` como entrada única para regenerar el catálogo, ejecutar tests y registrar métricas con un solo clic.
  - Por qué: reducir fricción operativa y hacer más mantenible la rutina de validación del proyecto.
  - DoD cumplido: el launcher invoca la generación, validación y métricas en secuencia y puede ejecutarse mediante doble clic en Windows.

- [COMPLETADO] Bucle de autopilot y webhook de ejemplo (Alta)
  - Qué: añadir `run_autopilot_loop.py`, `run_autopilot_loop.bat` y `scripts/autopilot_webhook_server.py` para repetir iteraciones, notificar al terminar y preparar un canal de recepción HTTP opcional.
  - Por qué: permitir un ciclo local de supervisión y ejecución indefinida sin depender de intervención manual en cada vuelta.
  - DoD cumplido: el bucle ejecuta `run_automation.py` iterativamente, notifica al usuario y permite opcionalmente enviar el mensaje a un webhook seguro configurado con variables de entorno.

- [COMPLETADO] Higiene del repositorio y artefactos locales (Media)
  - Qué: excluir cachés y artefactos generados del versionado y mantener el repositorio limpio.
  - Por qué: evitar ruido en git y conservar la trazabilidad del proyecto.
  - DoD cumplido: existe `.gitignore` con exclusiones para cachés Python y cobertura local.

- [COMPLETADO] Tests de regresión para scripts de métricas (Media)
  - Qué: validar analizadores del historial, cobertura y tendencia para evitar roturas del pipeline de métricas.
  - DoD cumplido: existe `tests/test_metrics_scripts.py` y pasa en la suite del proyecto.

## Backlog extendido (para fases siguientes)

- Historia/versionado por asset (historial mínimo en JSON).
- Tags, visibilidad (public/private/unlisted) y filtros asociados.
- Asociación many-to-many con proyectos `.blend` u otros.
- Políticas y herramientas para manejar archivos grandes (mover a carpeta / usar LFS).
- Interfaz admin segura (requiere backend o token-based flow).

## Reglas de priorización y trabajo

- Priorizar cambios que mejoren la calidad del catálogo y reduzcan riesgo de ruptura de la web.
- Prefieren soluciones simples y reversibles antes que re-arquitecturas.
- Documentar cada cambio en README y en SPECIFICATIONS.md / ARCHITECTURE.md.

## Próximos pasos recomendados (acción inmediata)

1. Implementar la prioridad media siguiente: UX móvil con paginación/lazy loading.
2. Preparar el flujo de CI para validación automática y despliegue manual.
3. Mantener el backlog sincronizado con la documentación cuando cambien requisitos o arquitectura.

---

Resumen: task.md ahora es un backlog compacto, alineado con SPECIFICATIONS.md y ARCHITECTURE.md, priorizando estabilidad y facilidad de revisión por agentes y humanos.
