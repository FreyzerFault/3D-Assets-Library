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

- [ ] **T1 — Normalizar las rutas de documentación en los SKILL.md** (impacto medio / coste bajo)
  - Qué: `.agents/skills/implement-task/SKILL.md`, `.agents/skills/project-review/SKILL.md` y `.agents/skills/test-and-verify/SKILL.md` referencian `docs/architecture.md`, `docs/specifications.md`, `docs/testing.md` y `docs/metrics.md` en minúsculas, pero los ficheros reales están en mayúsculas.
  - Por qué: en Linux (CI) esas rutas no existen y los flujos de agentes leen documentación inexistente.
  - DoD: los tres SKILL.md usan los nombres reales y no queda ninguna referencia en minúsculas.

- [ ] **T2 — Cubrir los caminos de error de los scripts operativos** (impacto alto / coste medio) — *implementado; falta verificar cobertura*
  - Qué: tests para `scripts/record_metrics.py` (coverage.json ausente o inválido, `assets-report.json` corrupto, fallo de `git rev-parse`, historial JSON corrupto o no-lista), `scripts/metrics_trend.py` (historial vacío, entradas sin `coverage_total`, fichero ausente, payload no-lista, rango plano en `make_bar`) y `run_automation.py` (parada temprana, secuencia completa, `main()` y propagación de fallo).
  - Por qué: es el pipeline que sostiene las métricas; un fallo silencioso deja el registro desactualizado sin avisar.
  - DoD: nuevos tests en verde y cobertura de `scripts/` y `run_automation.py` por encima del umbral `fail_under = 70` de `.coveragerc`.
  - Estado: 13 tests nuevos añadidos; suite en verde con **34 tests, OK**. Falta ejecutar `scripts/record_metrics.py` y comprobar la cobertura por fichero para cerrar el DoD.

### Siguiente

- [ ] **T4 — Verificar la política de archivos grandes** (impacto medio / coste medio)
  - Qué: comprobación reproducible que detecte activos mal ubicados según la política (`models/large/` para >100 MB, `models/2gb-plus/` para >2 GB fuera de git) y avise con instrucciones.
  - Por qué: hoy la política existe solo como convención documentada; nada la hace cumplir.
  - DoD: la comprobación lista los activos mal ubicados y está cubierta por tests.

- [ ] **T5 — Búsqueda y filtros en la web** (impacto medio / coste medio)
  - Qué: filtro por categoría y búsqueda por nombre sobre `assets.json`, integrados con la paginación existente.
  - Por qué: con 28 assets, recorrer la cuadrícula a mano ya es incómodo.
  - DoD: se puede filtrar y buscar sin recargar y la paginación sigue funcionando.

- [ ] **T6 — Categorías reales y tags por asset** (impacto medio / coste medio)
  - Qué: hoy todo asset nuevo entra como `category: "Props"` y sin tags. Definir categorías útiles y tags legibles, soportados en `assets.json` y en la UI.
  - Por qué: habilita T5 y mejora la descripción del catálogo.
  - DoD: el catálogo admite varios valores de categoría y tags, y la web los muestra.

- [ ] **T7 — Descriptions reales en el frontmatter de los SKILL.md** (impacto bajo / coste bajo)
  - Qué: los tres `SKILL.md` llevan `description: Brief description of what this skill does` como marcador de posición, y sus secciones `## Usage` son frases sueltas poco informativas.
  - Por qué: es el texto que ve un agente para decidir si la skill encaja; un marcador de posición anula esa señal.
  - DoD: cada `SKILL.md` describe en una línea qué hace y cuándo usarla, sin marcadores de posición.

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
