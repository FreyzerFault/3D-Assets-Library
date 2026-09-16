# Especificaciones del proyecto

## 1. Propósito

Este proyecto es una biblioteca estática de assets 3D para visualizar modelos `.glb` en navegador, consultar su información y descargarlos sin depender de un backend complejo.

El sistema actual prioriza simplicidad, portabilidad y facilidad de gestión sobre escalabilidad de infraestructura.

## 2. Estado actual

- El catálogo principal es `assets.json`.
- Los modelos reales viven en `models/` y siguen una política de almacenamiento por tamaño.
- La página web se genera con HTML, CSS y JavaScript puro.
- El script `generate_assets_data.py` detecta nuevos modelos y actualiza el catálogo.
- El proyecto mantiene una validación automatizada con tests `unittest` y una base mínima de CI.
- No existe backend ni base de datos productiva.

## 3. Requisitos funcionales actuales

### 3.1 Catalogación de modelos

- El sistema debe detectar automáticamente nuevos archivos `.glb` en `models/` y subcarpetas autorizadas.
- El sistema debe crear una entrada de catálogo para cada modelo nuevo.
- El sistema debe evitar duplicados y rutas no válidas.
- El catálogo debe conservar `name`, `file`, `category` y `description`.
- El catálogo debe almacenar metadatos operativos útiles: `size_bytes` y `modified_at`.
- El sistema debe advertir cuando un archivo supera los umbrales de tamaño de 10 MB y 100 MB.
- La estructura de almacenamiento debe respetar la política: `models/large/` para >100 MB, `models/projects/` para fuentes de autoría y `models/2gb-plus/` como compartimento exclusivo para archivos >2 GB no versionados en Git.
- El sistema debe detectar los activos mal ubicados según esa política y proponer la carpeta correcta en la salida y en `assets-report.json`.

### 3.2 Visualización en web

- La web debe renderizar cada asset en un visor 3D.
- Cada asset debe mostrar nombre, categoría, descripción y botón de descarga.
- La visualización debe funcionar sin un backend ni un build step.
- La web debe cargar los assets por bloques y diferir la creación de cada visor hasta que entre en pantalla.

### 3.3 Mantenibilidad

- El procedimiento de actualización del catálogo debe poder ejecutarse desde la línea de comandos.
- Las rutas deben resolverse respecto al script, no al directorio de trabajo actual.
- El sistema debe tolerar nombres no normalizados y reportarlos o corregirlos de forma consistente.

## 4. Requisitos no funcionales

- Debe ser fácil de desplegar en GitHub Pages o hosting estático.
- Debe ser compatible con navegadores modernos.
- Debe minimizar la complejidad operativa.
- Debe mantener una estructura de datos clara y legible para IA u otros agentes.

## 5. Modelo de datos

El catálogo actual usa esta estructura mínima:

```json
{
  "name": "Nombre del modelo",
  "file": "models/archivo.glb",
  "category": "Props",
  "description": "Texto descriptivo",
  "tags": ["low-poly", "ejercicio"],
  "size_bytes": 123456,
  "modified_at": "2026-09-15T20:00:00+00:00"
}
```

Reglas actuales:
- `file` debe ser una ruta relativa al proyecto.
- `category` debe ser una etiqueta simple (Personajes, Armas, Anatomía, Vehículos, Arquitectura, Criaturas, Robótica, Props).
- `description` es opcional.
- `tags` es una lista opcional de etiquetas en minúsculas; se normaliza y deduplica automáticamente y se omite cuando queda vacía.
- `size_bytes` y `modified_at` se rellenan automáticamente cuando se ejecuta el script de mantenimiento.

## 6. Reglas de nomenclatura y normalización

- Se deben eliminar espacios redundantes, rutas absolutas y caracteres innecesarios.
- Los nombres visibles deben normalizarse en formato título: `My Asset Model`.
- Los nombres se deducen del nombre del archivo cuando el campo `name` está vacío.
- Los assets con el mismo nombre normalizado se consideran conflicto y deben revisarse.

## 7. Objetivos aspiracionales

Estos objetivos no forman parte del estado actual, pero sí de la dirección deseada del proyecto:

- mantener historial de cambios de los assets
- preparar metadatos avanzados (peso, fecha, tags, visibilidad, proyecto origen)
- soportar proyectos asociados de Blender u otros programas
- preparar una capa de administración con visibilidad pública/privada

## 8. Riesgos y limitaciones

- El crecimiento del catálogo puede volver la gestión del JSON más frágil.
- El peso de los modelos puede afectar a rendimiento y almacenamiento.
- La gestión de visibilidad y roles sin backend real puede introducir riesgos de seguridad.
- La web estática puede limitar el rendimiento con muchos visores activos simultáneamente.
- Si se quiere escalar sin una base de datos, la metadata puede terminar dispersa y difícil de mantener.

## 9. Criterios de aceptación para cambios

Un cambio será aceptado si:

- resuelve el problema sin introducir nueva complejidad innecesaria,
- mantiene el catálogo legible y reproducible,
- no depende del directorio de ejecución del usuario,
- no rompe la carga de la web ni la estructura del proyecto,
- queda documentado en el código o en la documentación relevante.

## 10. Roadmap simplificado

### Fase 1: estabilidad

- validación básica de rutas y duplicados
- normalización de nombres
- pruebas de smoke para el script

### Fase 2: metadata útil

- peso, fecha, tags, visibilidad, proyecto origen
- catálogo más estructurado

### Fase 3: experiencia web

- filtros, paginación y carga diferida
- optimización para móviles

### Fase 4: administración

- modelo de visibilidad, favoritos y gestión de proyecto asociado

## 11. Conclusión

La especificación actual del proyecto debe mantener una línea clara: prioridad a una solución simple, robusta y fácil de mantener, con margen para crecer hacia un catálogo más rico sin romper la base actual.
