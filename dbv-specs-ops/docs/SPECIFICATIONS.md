# Especificaciones del proyecto

## Visión general

Este proyecto es una biblioteca estática de assets 3D creada para exhibir modelos GLB y permitir su descarga desde un navegador.

El uso común será personal para catalogar, organizar y almacenar modelos 3D que voy creando.
Y ocasionalmente para mostrar a otros usuarios o clientes una especie de Portfolio rápido.

Debe ser lo más simple y ligero posible, y que no necesite apenas mantenimiento.
Todo proceso que se pueda automatizar debe estar automatizado.

Interfaz muy directa basada en HTML, CSS y JavaScript básico, con posible futura expansión a otros frameworks.

## Objetivo principal

El sitio permite visualizar cada modelo en un visor 3D integrado y ofrecer un enlace de descarga del archivo `.glb` asociado.

El catálogo se alimenta desde un archivo `assets.json`, que describe cada asset con nombre, ruta, categoría y descripción.

Queda pendiente explorar otras alternativas de formato o infraestructura para metadatos y taxonomía para mejorar la gestión de la colección.

El script `generate_assets_data.py` escanea la carpeta `models/` para detectar nuevos archivos GLB y añadirlos automáticamente al JSON existente con todos los metadatos necesarios y opcionales.

## Requisitos funcionales actuales

- El usuario debe poder abrir la página principal y ver una colección de tarjetas con preview 3D de cada asset.
- Cada tarjeta debe incluir:
  - nombre visible del modelo
  - categoría
  - descripción opcional
  - visor 3D con giro/cámara
  - herramienta sobre la que se creó el modelo (si se conoce)
- El catálogo debe poder actualizarse sin tocar manualmente el archivo JSON cuando se añaden nuevos modelos.
- La ruta del modelo y del archivo de metadata debe ser resoluble de forma estable, sin depender del directorio de trabajo actual.

## Requisitos no funcionales observados

El proyecto prioriza simplicidad, portabilidad y facilidad de uso sobre escalabilidad o arquitectura de aplicación compleja.

La solución está diseñada para un despliegue estático (principalmente GitHub Pages).

La colección es dependiente del sistema de archivos local para la gestión de assets, no de una base de datos ni de una API. Por ahora.

## Datos y modelo de dominio

El archivo `assets.json` contiene una lista de objetos con este formato aproximado:

```json
{
  "name": "Nombre del modelo",
  "description": "Texto descriptivo",
  "file_name": "archivo",
  "version": "1.1",
  "fav": true,
  "status": "WIP",
  "visibility": "public",
  "files": [
    "models/archivo.glb",
    "models/archivo_hd.glb",
    "models/archivo_lp.glb",
    "projects/archivo/archivo.blend",
    "projects/sandbox.blend",
    "projects/archivo/albedo.png"
  ],
  "tags": ["Props", "Weapons", "LowPoly"],
  "project_app": "Blender 5.1",
  "size_mb": [24, 80.2, 12.5],
  "date_created": "2024-01-01",
  "date_modified": "2024-01-15",
  "related_links": ["daviduvi.dev", "itch.io/FreyzerFault/game"],
  "keywords": ["marchita_campina", "sword"]
}
```

Las categorías deben tener su icono asociado y un color de fondo único para la tarjeta de visualización.

## Estado real del proyecto

El proyecto está en fase de prototipo / biblioteca funcional en crecimiento, sin backend ni pipeline de tests formal.

El código está orientado a conveniencia y uso personal, con poca infraestructura de validación automática.

Faltan definiciones de negocio más detalladas: criterios de catalogación, política de nombres, versión de assets, clasificación por colección o autor, etc.

No hay documentado un flujo formal de contribución ni de revisión de assets antes de publicarlos.

---

## Objetivos del producto y dirección de ingeniería

El objetivo principal del proyecto es convertir una colección de modelos 3D en una biblioteca reutilizable, navegable y administrable, con capacidad de publicación en web estática y gestión de metadatos estructurados.

La intención del proyecto no es solo "mostrar modelos", sino construir un sistema de catálogo de contenido 3D que pueda escalar: crecer, organizarse, filtrarse, validarse y publicarse sin depender de un backend complejo.

El proyecto actual se apoya en `assets.json` como fuente de verdad del catálogo y en `generate_assets_data.py` como automatizador de mantenimiento.

La visión ambiciosa del usuario incluye: automatización del catálogo, gestión de metadatos avanzados, control de visibilidad, optimización para web, roles del usuario y administración del contenido, subpáginas de detalles individuales para cada modelo.

### Objetivos funcionales prioritarios

#### 1. Catálogo automático y fiable

Cada nuevo archivo `.glb` añadido a `models/` debe poder detectarse automáticamente y resolverse como un asset válido del catálogo.

El sistema debe registrar todos los datos del json de ejemplo para cada asset, y revisar que los assets ya almacenados cumplan con los criterios de validación y no le falte ningún campo.

El catálogo debe mantener un historial de cambios, versiones y fechas de modificación para detectar modelos actualizados y no solo añadidos.

Las versiones deben ser automáticas salvo que el usuario la defina manualmente, a través de el nombre del archivo o de un campo de metadata.

El sistema debe validar que cada nombre siga una convención estable del proyecto antes de publicarse.

Se debe detectar archivos con mayor peso del esperado y moverlos a una carpeta de assets pesados, o marcar su visibilidad como "no listada" hasta que se resuelva su publicación.

#### 2. Exposición del catálogo en web

La web debe mostrar cada modelo en un visor 3D con sus metadatos de manera compacta.

La web debe soportar navegación eficiente en dispositivos de baja potencia y móviles, con paginación, carga diferida y reducción de visores activos o adaptación de sus parámetros de renderizado según el hardware.

La interfaz debe permitir filtros por nombre, categoría, fecha, peso, visibilidad y otras propiedades relevantes.

#### 3. Administración y visibilidad del contenido

El propietario o administrador debe poder distinguir entre contenido público, privado y no listado u oculto.

El sistema debe permitir marcar favoritos, distinguir visibilidad y controlar qué assets y datos se muestran por defecto para usuarios no autorizados.

Debe existir una capa de administración segura para evitar falsos admins o acceso no autorizado.

#### 4. Soporte para proyectos de origen

El sistema debería poder asociar un modelo con uno o varios archivos de proyecto (Blender, BlockBench, Maya, 3DS Max, etc.), evitando depender de un solo formato.

La relación entre asset y proyecto debe ser explícita para evitar duplicidades o ambigüedades en la gestión del contenido.

### Criterios de aceptación para SDD y IA agente

La especificación debe ser ejecutable por agentes: clara, verificable, con límites y riesgos definidos.

Cada objetivo debe responder a una pregunta concreta: qué debe pasar, qué debe evitarse y cuál es el criterio de éxito.

Cada feature de negocio debe tener un "Definition of Done" mínimo: entrada de datos, validación, persistencia, visualización y posible rollback.

El sistema debe distinguir entre requisitos actuales, aspiracionales y riesgos de arquitectura.

La web debe ser consumible por agentes con buenas prácticas.

### Restricciones y supuestos

El proyecto sigue siendo estático y no tiene backend de producción establecido.

Se prioriza simplicidad y velocidad de ejecución sobre complejidad de infraestructura.

El repositorio está pensado para GitHub Pages o entorno estático equivalente, no para un sistema multiusuario con base de datos real en producción.

La solución actual debe asumir que no existe una identidad de usuario robusta ni una capa de seguridad avanzada por defecto.

### Problemas futuros y riesgos de estos objetivos

El principal riesgo es que el proyecto crezca demasiado rápido en complejidad sin una base de datos o una capa de dominio clara. Eso puede derivar en:

- metadata inconsistente
- nombrado heterogéneo
- archivos duplicados o rutas rotas
- validaciones dispersas entre scripts y UI

El manejo de archivos pesados puede convertirse en un problema de coste real: GitHub, almacenamiento, rendimiento de carga, sincronización y despliegue.

Si se implementa visibilidad, admin y favoritos sin una capa de autenticación real, se corre el riesgo de introducir "admin oculto" o bypasses de seguridad por lógica frágil.

La relación Many-to-Many entre modelos y proyectos de software puede volverse difícil de mantener si no se define un modelo de entidad claro y una política de consistencia.

La web en GitHub Pages puede degradar el rendimiento con demasiados visores 3D activos simultáneamente, especialmente en móviles o equipos modestos.

La automatización del catálogo puede volverse costosa si se hace sin un historial estable, validación de cambios y estrategia de versionado.

La escalabilidad del contenido puede terminar en un repositorio difícil de gestionar si no se separan responsabilidades: archivos fuente, metadata, catálogo público y procesos de publicación.

### Recomendación de redacción para agentes

La forma más útil de expresar estos objetivos es en lenguaje de especificación con tres capas: objetivo de negocio, requerimiento funcional y riesgo/limitación.

Para IA agente, conviene dejar explícito lo siguiente en cada feature:

- entrada de datos
- validación
- persistencia
- renderizado o uso
- condición de error
- criterio de aceptación
- riesgo asociado

Esta estructura reduce ambigüedad, mejora la coherencia del trabajo en paralelo y hace que los agentes puedan actuar sin interpretar suposiciones ocultas.

---

## Requisitos adicionales del usuario (roadmap aspiracional)

El usuario ha indicado una serie de objetivos avanzados para expandir la biblioteca desde un catálogo estático a una plataforma más inteligente y administrable.

### Backend

- Automatizar la adición y actualización de modelos cuando cambien sus metadatos o su fecha de modificación.
- Mantener un historial de versiones y cambios de cada asset.
- Validar el nombre del archivo y el naming convention del proyecto.
- Analizar e indexar propiedades del modelo: tamaño, topología, formato, tags, fecha de creación/modificación, y otros atributos útiles.
- Detectar tamaños de archivo críticos y mover modelos pesados a carpetas gestionadas explícitamente.
- Llevar un registro del espacio ocupado por los modelos y de la cantidad de assets por categoría, para poder filtrar y optimizar la carga.
- Definir una estrategia de seguridad para distinguir propietario, admin y usuario estándar.
- Soportar proyectos de origen asociados a cada asset, independientemente del software utilizado.
- Establecer una relación muchos-a-muchos entre modelos y proyectos de creación.

### Frontend

- Optimizar el catálogo para móvil y pantallas de baja capacidad con paginación, carga diferida y adaptaciones automáticas.
- Detectar capacidades del dispositivo y ajustar la carga de visores 3D.
- Añadir filtros por nombre, categoría, peso, fecha y visibilidad.
- Mejorar la UI responsive y la legibilidad del catálogo.
- Añadir iconos, etiquetas y metadatos visuales para programas, tags y umbrales de peso.
- Añadir descripción breve, enlaces externos y contexto de uso del asset.
- Implementar un sistema de paginación flexible y usable.
- Permitir búsqueda por palabras clave, tags y categorías.
- Permitir ordenación por distintas propiedades de forma aditiva.
- Añadir elementos cosméticos que realcen el atractivo de la web.
- Añadir elementos cosméticos animados que den dinamismo y vida a la web.

### Admin / propietario

- Permitir visibilidad pública, privada o no listada.
- Permitir filtrar contenido según visibilidad para admin o propietario.
- Añadir favoritos con flag de usuario.
- Añadir una vía oculta de administración segura para activación de modo admin.
- Permitir descarga directa del modelo y del proyecto asociado.

### Infraestructura y mantenimiento

- Añadir marcas de tiempo que registren el tiempo que tarda la web en cargar y renderizar cada asset para profiling.
- Reconsiderar la base de datos o capa de persistencia a medida que el catálogo crezca.
- Diseñar un flujo de CI/CD para actualización del catálogo y despliegue en GitHub Pages.
- Añadir recordatorios y validaciones de publicación para evitar que la web quede desactualizada respecto al repositorio.
