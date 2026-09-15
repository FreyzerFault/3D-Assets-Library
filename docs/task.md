# Backlog y Snapshot (versión SDD, resumida)

## Snapshot breve

- Proyecto: Biblioteca estática de assets 3D.
- Stack: HTML/CSS/JS (frontend), `model-viewer` (visor), Python 3 (scripts), `assets.json` (catálogo), `models/` (GLB).
- Estado: prototipo funcional, catálogo con ~28 assets. Validación y normalización básicas ya aplicadas.
- Calidad: pruebas de smoke añadidas; transformación y validación inicial implementadas.

## Trabajo completado (evidencia)

- Resolución de rutas relativa al script (BASE_DIR). (`generate_assets_data.py`)
- Normalización de nombres y rutas en `assets.json`.
- Añadidos tests de smoke que pasan (`tests/test_generate_assets_data.py`).
- Validación básica de duplicados y archivos faltantes.

## Prioridad actual (próximo sprint)

Ordenado por impacto y coste (alta → baja). Cada ítem incluye criterio de aceptación (DoD).

1. Metadata operativa y tamaño (Alta)

- Qué: extraer tamaño de archivo, fecha de modificación y añadir campos `size_bytes`, `modified_at` al catálogo.
- Por qué: detectar assets pesados y habilitar filtros/umbrales.
- DoD: `generate_assets_data.py` añade `size_bytes` y `modified_at`; se generan warnings para archivos >10MB y >100MB.

1. Política de naming y normalización (Alta)

- Qué: definir y aplicar reglas simples (trim, reemplazar espacios por guiones opcional, normalizar mayúsculas) y rechazar/renombrar nombres problemáticos.
- DoD: script normaliza `name` y `file`; se documenta la convención en README; no hay duplicados tras normalizar.

1. Validación y reporting (Media)

- Qué: mejorar mensajes de validación, salida CLI y generar un `assets-report.json` con issues detectados.
- DoD: ejecución `python generate_assets_data.py --report` produce `assets-report.json` con listas `errors` y `warnings`.

1. UX móvil: paginación / lazy loading (Media)

- Qué: implementar paginación simple + lazy-loading de visores para reducir consumo en móviles.
- DoD: página carga y muestra primero N assets (configurable) y carga el resto al hacer scroll; sin caídas en navegadores móviles razonables.

1. CI de generación y despliegue (Baja)

- Qué: añadir workflow de GitHub Actions que ejecute el script y (opcional) despliegue en GitHub Pages bajo control manual.
- DoD: action que ejecuta tests y, si se aprueba, puede actualizar `assets.json` en una rama `gh-pages` mediante trigger manual.

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

1. Implementar tarea (1) Metadata operativa — añadir size/modified_at.
2. Implementar tarea (2) Naming & normalization.
3. Abrir PR por cada cambio pequeño y ejecutar tests de smoke.

---

Resumen: task.md ahora es un backlog compacto, alineado con SPECIFICATIONS.md y ARCHITECTURE.md, priorizando estabilidad y facilidad de revisión por agentes y humanos.
