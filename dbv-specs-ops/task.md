# Backlog y Snapshot de Contexto SDD

## Snapshot de Contexto

- Proyecto: Biblioteca estática de assets 3D para visualización y descarga.
- Stack actual: HTML, CSS, JavaScript, Python 3, archivos GLB y assets.json.
- Estado del proyecto: prototipo funcional / desarrollo activo en progreso con catálogo real de modelos.
- Tests: ninguno detectado.
- Documentación existente: README básico, sin documentación técnica ni especificaciones de dominio.
- Historial git: activo, con varios commits de mejora en catálogo y visualización.
- Deuda técnica visible:
  - ausencia de pruebas automatizadas
  - catálogo manejado como JSON sin validación estructural
  - rutas dependientes del entorno de ejecución si no se resuelven desde el script
  - metadata incompleta y poco homogénea en muchos modelos
  - sin CI ni flujo de contribución formal

## Tareas en curso y detectadas

### 1. Mantenimiento del catálogo de assets

- Estado: activo
- Descripción: asegurar que la detección de modelos nuevos siga funcionando correctamente y que `assets.json` se actualice de forma segura.
- Evidencia: `generate_assets_data.py` recorre `models/*.glb` y escribe en `assets.json`.

### 2. Corrección de resolución de rutas

- Estado: corregido durante la adaptación SDD
- Descripción: la ruta del archivo JSON y del directorio `models` debe resolverse respecto al script, no respecto al directorio de ejecución del proceso.
- Evidencia: `Path(__file__).resolve().parent` se usa como base del proyecto.

### 3. Compatibilidad de consola en Windows

- Estado: corregido durante la adaptación SDD
- Descripción: evitar fallos de codificación al imprimir mensajes de resultado en entornos con codificación cp1252.
- Evidencia: se reemplazó la salida con texto ASCII seguro (`[OK]` en lugar de `✓`).

## Backlog de tareas pendientes

### Prioridad alta

- [PENDIENTE] Añadir validación de `assets.json` para detectar rutas rotas o entradas duplicadas.
- [PENDIENTE] Añadir un flujo de pruebas mínimo para verificar que el script genera el catálogo sin errores.
- [PENDIENTE] Normalizar el formato de nombres y categorías en los assets para evitar inconsistencias.

### Prioridad media

- [PENDIENTE] Mejorar la descripción de modelos vacíos con un valor por defecto más útil o un proceso de catalogación manual.
- [PENDIENTE] Crear una política de naming para archivos `.glb` para evitar mezclas de mayúsculas/minúsculas, espacios y guiones.
- [PENDIENTE] Definir una taxonomía de categorías más precisa (props, armas, personajes, arquitectura, vehículos, etc.).

### Prioridad baja

- [PENDIENTE] Documentar cómo añadir un modelo nuevo al repositorio.
- [PENDIENTE] Automatizar la generación del catálogo desde un CI o script de despliegue.
- [PENDIENTE] Añadir un sistema de revisión y aprobación antes de publicar assets.

## Tareas pendientes indicadas por el usuario

[ PENDIENTE ] No se ha recibido contexto adicional del usuario sobre objetivos de negocio, requisitos de catálogo o roadmap de producto.

## Recomendación de arranque SDD

La tarea más urgente es consolidar la base de conocimiento del proyecto mediante la definición del catálogo y la validación del script de generación. Esto reduce riesgo de errores de rutas, entradas duplicadas y inconsistencias al publicar nuevos modelos.

El siguiente paso recomendado es:

1. definir una política clara de nombrado y categorización,
2. añadir validación mínima en `generate_assets_data.py`,
3. crear tests de smoke para la generación del JSON.
