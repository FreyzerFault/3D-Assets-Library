# Cola de trabajo

## Snapshot breve

- Proyecto: biblioteca estática de assets 3D.
- Stack: HTML/CSS/JS (frontend), `model-viewer` (visor), Python 3 (scripts), `assets.json` (catálogo), `models/` (GLB).
- Estado: catálogo funcional con 28 assets, validación normalizada, métricas registradas y flujos automatizados listos.
- Calidad: suite estable, cobertura registrada en `docs/metrics_log.json`, script de registro automático y CI configurado.

## Cómo se usa este archivo

- La cola activa son las tareas pendientes, ordenadas por prioridad.
- Cada tarea declara Qué / Por qué / DoD para poder verificarla sin ambigüedad.
- Al cerrar una tarea, se mueve a `docs/task_archive.md` con su evidencia.
- El backlog extendido recoge ideas sin compromiso, todavía sin DoD.

## Cola activa (pendiente)

### Ahora

- [ ] **T11 — Asociación asset ↔ proyectos fuente** (impacto medio / coste medio)
  - Qué: soportar campo opcional `projects` en `assets.json` (lista de rutas relativas a `models/projects/`), preservado por la normalización, validado (debe existir y estar bajo `models/projects/`), y visible en la web como insignias/enlaces.
  - Por qué: es el item de backlog "many-to-many con `.blend`" en versión estática: sin backend, el catálogo enlaza cada asset con sus fuentes de autoría.
  - DoD: `normalize_asset` preserva/normaliza `projects`; `validate_assets` reporta rutas inexistentes o fuera de `models/projects/`; `index.html` muestra los proyectos enlazados; tests de preservación y validación.

- [ ] **T12 — Historial de cambios del catálogo** (impacto bajo / coste medio)
  - Qué: `generate_assets_data.py` mantiene `assets-history.json` con el último estado conocido y un registro de eventos (`added`/`removed`/`updated` con fecha) calculado por diff en cada ejecución.
  - Por qué: es el item de backlog "historial de cambios por asset" en versión estática: trazabilidad sin backend ni base de datos.
  - DoD: el historial se crea/actualiza en cada run, registra altas/bajas/cambios (tamaño, fecha, nombre), limita el log (p. ej. 500 eventos), y tiene tests con directorios temporales.

### Aparcado (requiere decisión explícita)

- Historial y versionado por asset: depende de que el catálogo crezca y de T6.
- Visibilidad pública/privada y capa de administración: contradice el no-goal "sin backend" hasta que se pida explícitamente.
- Asociación many-to-many con proyectos `.blend`: depende de T6.
- Migración a paquete Python (`src/`, `pyproject.toml`) o bundler de frontend: solo si crecen el catálogo y los colaboradores.

## Backlog extendido (sin DoD todavía)

- Asociación many-to-many con proyectos `.blend` u otros.
- Historial de cambios por asset.
- Políticas y herramientas para manejar archivos grandes (mover a carpeta / usar LFS), más allá de la comprobación de T4.
- Visibilidad (public/private/unlisted) y capa de administración: solo con decisión explícita sobre backend.

## Reglas de priorización y trabajo

- Priorizar cambios que mejoren la calidad del catálogo y reduzcan riesgo de ruptura de la web.
- Preferir soluciones simples y reversibles antes que re-arquitecturas.
- Documentar cada cambio en README y en SPECIFICATIONS.md / ARCHITECTURE.md.
- Cerrar una tarea solo cuando su DoD sea verificable; entonces se mueve a `docs/task_archive.md`.

---

Este fichero es la cola activa. Los flujos base (catálogo, validación, CI, despliegue, métricas y automatización) ya están cerrados y archivados en `docs/task_archive.md`; el trabajo pendiente es el de la cola de arriba.
