# Arquitectura actual

## Stack detectado

- Frontend estático: HTML5 + CSS + JavaScript puro
- Visor 3D: `model-viewer` de Google, cargado desde CDN
- Datos: `assets.json` como fuente de catálogo
- Generación de catalogación: Python 3
- Assets 3D: archivos `.glb` alojados en `models/`
- Despliegue: entorno estático sin build step ni framework de aplicación

## Estructura de archivos

```text
.
├── README.md
├── assets.json
├── generate_assets_data.py
├── index.html
├── models/
├── style.css
└── dbv-specs-ops/
    └── docs/
        ├── SPECIFICATIONS.md
        ├── ARCHITECTURE.md
        └── task.md
```

## Componentes principales

### 1. `index.html`

Es el punto de entrada de la UI.

Responsabilidades:

- cargar `assets.json`
- iterar sobre cada asset
- construir una tarjeta por modelo
- inyectar un `<model-viewer>` por cada elemento
- enlazar el botón de descarga con el archivo GLB
- mostrar un estado de error si el JSON no puede cargarse

### 2. `assets.json`

Es el catálogo de datos visibles para la aplicación.

Incluye entradas con:

- `name`
- `file`
- `category`
- `description`

Este archivo actúa como fuente de verdad del contenido visible.

### 3. `generate_assets_data.py`

Es el script de mantenimiento del catálogo.

Responsabilidades:

- localizar la carpeta base del proyecto con `Path(__file__).resolve().parent`
- leer `assets.json`
- recorrer `models/*.glb`
- detectar archivos no registrados
- añadir entradas nuevas con formato consistente
- guardar el JSON actualizado

### 4. `models/`

Directorio donde residen los modelos 3D finales. Actualmente se organiza por archivos `.glb` que se sirven directamente al navegador.

## Flujo de ejecución

1. El desarrollador añade un nuevo archivo GLB a `models/`.
2. Se ejecuta `generate_assets_data.py`.
3. El script compara los modelos detectados con los ya registrados en `assets.json`.
4. Si hay diferencias, añade las nuevas entradas con nombre generado a partir del nombre del archivo.
5. La UI carga `assets.json` mediante `fetch('assets.json')`.
6. El navegador renderiza cada modelo usando `model-viewer` y ofrece descarga directa.

## Dependencias y límites

### Dependencias externas

- `model-viewer` cargado desde la CDN de Google
- navegador moderno con soporte de módulos ES y WebGL

### Limitaciones actuales

- no hay backend
- no hay persistencia estructurada más allá del JSON
- no hay sistema de pruebas automatizadas
- no hay validación de metadata ni de integridad de rutas
- no hay proceso de CI/CD ni de publicación automatizada
- el catálogo depende de la disciplina manual a la hora de añadir modelos y describirlos

## Patrones de diseño observados

[INFERIDO] El proyecto usa un enfoque de “contenido estático + script de mantenimiento” más que un patrón de aplicación de frontend.

[INFERIDO] La lógica funcional principal está dividida entre:

- representación visual (`index.html` / `style.css`)
- estructura de datos (`assets.json`)
- automatización (`generate_assets_data.py`)

[INFERIDO] No existe un modelo de servicio ni un flujo de estado complejo; la aplicación es esencialmente una vista catalogada de archivos 3D.
