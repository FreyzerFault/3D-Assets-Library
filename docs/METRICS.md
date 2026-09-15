# METRICS.md

## Propósito

Este documento define las métricas que se recogen para el proyecto, explica dónde se almacenan y qué eventos disparan una medición. Sirve de referencia para agentes y colaboradores humanos: qué medir, por qué y cómo interpretar los valores.

## Anomalías relevantes detectadas y medidas

Durante la revisión del proyecto, la anomalía más destacable no fue un fallo funcional sino una deriva de mantenimiento: las propias herramientas de métricas (`scripts/record_metrics.py` y `scripts/metrics_trend.py`) estaban poco cubiertas por tests y su salida podía quedar desalineada con la documentación si no se regeneraba desde una única fuente de verdad.

Medidas aplicadas:

- incluir tests específicos para `main()` y para los flujos de escritura de historial y tendencia,
- tratar la cobertura de estas herramientas como un indicador operativo más, no como dato anecdótico,
- mantener la métrica de cobertura en un único punto de generación (`python scripts/record_metrics.py`) y usar esa salida como referencia para badge y registro,
- revisar el historial de métricas cuando se complete un hito para detectar regresiones de calidad o del flujo de automatización.

## Dónde se almacenan las métricas

- Log legible histórico: docs/metrics_log.md — se añade una entrada cada vez que se ejecuta la medición (normalmente tras una actualización de tests o al completar un hito relevante).
- Log estructurado: docs/metrics_log.json — versión JSON con el mismo historial para análisis automático y dashboards.
- Artefactos intermedios: coverage.json (generado temporalmente por el script), assets-report.json (generado por generate_assets_data.py), docs/metrics_trend.txt (resumen visual generado por scripts/metrics_trend.py) — el script de registro extrae valores de estos artefactos.

## Eventos que disparan una medición

- Cuando se actualizan tests (nuevos tests añadidos, tests modificados o reorganizados).
- Tras completar un hito mayor ("hito" = cambios que afectan funcionalidad o arquitectura; e.g., migración, reescritura de módulo, gran refactor).
- En la CI: tras ejecución de la suite en la rama principal o en PRs relevantes (opcionalmente como paso de validación).

## Formato del registro

Cada entrada en docs/metrics_log.md es un bloque legible con: fecha, commit, resumen de resultados (tests pasados/fallidos), cobertura total, cobertura por fichero (resumen), número de tests, duración aproximada, y métricas del catálogo (issues/warnings desde assets-report.json). El script scripts/record_metrics.py genera y añade la entrada.

## Métricas importantes (DoD: siempre recolectar)

- Fecha y hora de la medición
- Commit (SHA corto) y branch
- Resultado de la suite de tests (passed/failed)
- Número de tests ejecutados y tiempo total de ejecución
- Cobertura total (%) — líneas cubiertas / líneas totales
- Cobertura por archivo (lista de archivos relevantes con %)
- Branch coverage (%) cuando esté disponible
- Lista o número de tests fallados y sus nombres (si los hay)
- Conteo de issues y warnings del catálogo (assets-report.json): errores, advertencias
- Número total de assets y tamaño total agregado (bytes)
- Conteo de assets grandes (por umbrales configurados) y lista corta
- Estado de lint/pre-commit (passed/failed)
- Churn de código desde último commit (líneas añadidas/eliminadas)

## Métricas sugeridas (opcional)

- Tiempo medio de ejecución por test
- Tasa de cambio de cobertura desde la última medición (delta %)
- Número de archivos modificados en el commit
- Size of artifacts (assets.json size, assets-report.json size)
- Métricas de rendimiento del frontend (FCP, LCP) si se incorporan pruebas de navegador
- Vulnerabilidades conocidas en dependencias (vulnerabilities count)
- Complejidad ciclomática por fichero (si se integra herramienta)
- Mutation score (si se adopta mutation testing)

## Explicaciones breves de cada métrica

- Fecha y hora: histórico; permite ordenar y correlacionar con commits/PRs.
- Commit SHA: precisa vinculación a código fuente.
- Resultado tests: indicador básico de salud; si falla, no se debe avanzar en otras tareas.
- Número de tests y duración: ayuda a estimar coste y regresiones temporales.
- Cobertura total: proporción de código ejecutado por tests; útil para priorizar áreas sin pruebas.
- Cobertura por archivo: identifica ficheros críticos con poca cobertura.
- Branch coverage: muestra decisiones lógicas no probadas.
- Tests fallados: punto directo de acción para debugging.
- Issues/warnings del catálogo: indica problemas específicos del dominio (assets faltantes, rutas absolutas, archivos grandes).
- Número total de assets / tamaño total: útil para dimensionar storage y detectar crecimiento inesperado.
- Assets grandes: lista que ayuda a decidir políticas (LFS, mover, optimizar).
- Lint status: asegura calidad de estilo y evita ruido de formato.
- Churn y files changed: identificar cambios grandes que requieren revisiones más cuidadosas.

## Buenas prácticas y recomendaciones

- Automatizar la generación y el registro: scripts/record_metrics.py debe usarse desde CI y localmente cuando se toquen tests.
- Mantener el log legible y compacto: preferir resúmenes y enlazar artefactos más detallados (coverage.json) en lugar de volcar grandes tablas.
- Correlacionar métricas con PR/issue/hitos para trazabilidad.
- Revisar y actualizar METRICS.md tras cada hito importante para reflejar medidas nuevas o cambiar prioridades.

---

(Cualquier cambio al esquema de métricas debe documentarse aquí con fecha y motivo.)
