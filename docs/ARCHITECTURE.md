# Arquitectura actual

## Stack

- HTML5 + CSS + JavaScript vanilla
- `model-viewer` de Google cargado desde CDN
- Python 3 para la generación del catálogo
- `assets.json` como fuente de datos del frontend
- archivos `.glb` en `models/`
- despliegue estático (GitHub Pages o hosting equivalente)

## Estructura del proyecto

```text
.
├── README.md
├── index.html
├── style.css
├── assets.json
├── generate_assets_data.py
├── models/
├── dbv-specs-ops/
│   └── docs/
│       ├── SPECIFICATIONS.md
│       ├── ARCHITECTURE.md
│       └── task.md
└── tests/
```

## Componentes principales

### `index.html`

Es la capa de presentación. Carga `assets.json`, crea las tarjetas de los assets y renderiza cada visor 3D con `model-viewer`.

### `assets.json`

Es la fuente de verdad del catálogo visible. Contiene los assets que se muestran en la web y su metadata mínima.

### `generate_assets_data.py`

Script de mantenimiento que:

- detecta modelos nuevos en `models/`
- normaliza nombres y rutas
- valida entradas duplicadas o rotas
- actualiza `assets.json`

### `models/`

Directorio de archivos 3D. Actualmente se sirve directamente al navegador en formato `.glb`.

## Flujo de ejecución

1. Se añade un archivo `.glb` a `models/`.
2. Se ejecuta `generate_assets_data.py`.
3. El script compara los archivos con el catálogo existente.
4. Se actualiza `assets.json` con nuevos assets si procede.
5. `index.html` hace `fetch('assets.json')` y renderiza la colección.
6. El navegador muestra el visor 3D y ofrece la descarga del modelo.

## Restricciones actuales

- no hay backend
- no hay base de datos de producción
- no hay autenticación real
- no hay pruebas automatizadas en la capa de negocio
- la metadata está contenida en JSON y no en un sistema estructurado
- el catálogo depende de la disciplina del usuario a la hora de añadir modelos y describirlos

## Dirección de evolución

La arquitectura actual es una base estática y simple. La evolución natural es separar mejor:

- contenido y metadata
- validación y catálogo
- publicación y mantenimiento
- gestión administrativa y visibilidad

Esto permite crecer hacia un catálogo más rico sin cambiar la base estática inicial.
