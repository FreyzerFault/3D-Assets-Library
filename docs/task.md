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

- (vacía — ver `docs/task_archive.md` para el trabajo completado)

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
