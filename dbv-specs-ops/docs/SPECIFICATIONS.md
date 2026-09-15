# Especificaciones del proyecto

## Visión general

[CONFIRMADO] Este proyecto es una biblioteca estática de assets 3D creada para exhibir modelos GLB y permitir su descarga desde un navegador.

[INFERIDO] El objetivo principal es mantener un catálogo visual de piezas 3D reutilizables (props, accesorios, elementos de referencia) sin depender de un backend ni de un framework de frontend complejo.

[INFERIDO] La biblioteca se usa como un portafolio o repositorio personal de modelos 3D, con una interfaz muy directa basada en HTML, CSS y JavaScript.

## Objetivo principal

[CONFIRMADO] El sitio permite visualizar cada modelo en un visor 3D integrado y ofrecer un enlace de descarga del archivo `.glb` asociado.

[CONFIRMADO] El catálogo se alimenta desde un archivo `assets.json`, que describe cada asset con nombre, ruta, categoría y descripción.

[CONFIRMADO] El script `generate_assets_data.py` escanea la carpeta `models/` para detectar nuevos archivos GLB y añadirlos automáticamente al JSON existente.

## Requisitos funcionales actuales

- El usuario debe poder abrir la página principal y ver una colección de tarjetas con preview 3D de cada asset.
- Cada tarjeta debe incluir:
  - nombre visible del modelo
  - categoría
  - descripción opcional
  - visor 3D con giro/cámara
  - botón de descarga del GLB
- El catálogo debe poder actualizarse sin tocar manualmente el archivo JSON cuando se añaden nuevos modelos.
- La ruta del modelo y del archivo de metadata debe ser resoluble de forma estable, sin depender del directorio de trabajo actual.

## Requisitos no funcionales observados

[INFERIDO] El proyecto prioriza simplicidad, portabilidad y facilidad de uso sobre escalabilidad o arquitectura de aplicación compleja.

[INFERIDO] La solución está diseñada para un despliegue estático (por ejemplo, GitHub Pages o hosting estático similar).

[INFERIDO] La colección es dependiente del sistema de archivos local para la gestión de assets, no de una base de datos ni de una API.

## Datos y modelo de dominio

[CONFIRMADO] El archivo `assets.json` contiene una lista de objetos con este formato aproximado:

```json
{
  "name": "Nombre del modelo",
  "file": "models/archivo.glb",
  "category": "Props",
  "description": "Texto descriptivo"
}
```

[INFERIDO] La categoría actual parece ser homogénea (`Props`), aunque el proyecto tiene margen para modelar tipos más específicos en el futuro.

[INFERIDO] El contenido del campo `description` es opcional y puede estar vacío.

## Estado real del proyecto

[CONFIRMADO] El proyecto está en fase de prototipo / biblioteca funcional en crecimiento, sin backend ni pipeline de tests formal.

[INFERIDO] El código está orientado a conveniencia y uso personal, con poca infraestructura de validación automática.

[ PENDIENTE ] Faltan definiciones de negocio más detalladas: criterios de catalogación, política de nombres, versión de assets, clasificación por colección o autor, etc.

[ PENDIENTE ] No hay documentado un flujo formal de contribución ni de revisión de assets antes de publicarlos.

---

## Objetivos del producto y dirección de ingeniería

[CONFIRMADO] El objetivo principal del proyecto es convertir una colección de modelos 3D en una biblioteca reutilizable, navegable y administrable, con capacidad de publicación en web estática y gestión de metadatos estructurados.

[INFERIDO] La intención del proyecto no es solo "mostrar modelos", sino construir un sistema de catálogo de contenido 3D que puedaescala: crecer, organizarse, filtrarse, validarse y publicarse sin depender de un backend complejo.

[CONFIRMADO] El proyecto actual se apoya en `assets.json` como fuente de verdad del catálogo y en `generate_assets_data.py` como automatizador de mantenimiento.

[CONFIRMADO] La visión ambiciosa del usuario incluye: automatización del catálogo, gestión de metadatos avanzados, control de visibilidad, optimización para web y administración del contenido.

### Objetivos funcionales prioritarios

#### 1. Catálogo automático y fiable

[CONFIRMADO] Cada nuevo archivo `.glb` añadido a `models/` debe poder detectarse automáticamente y resolverse como un asset válido del catálogo.

[CONFIRMADO] El sistema debe registrar nombre, ruta, categoría y descripción para cada asset.

[PENDIENTE] El catálogo debe mantener un historial de cambios, versiones y fechas de modificación para detectar modelos actualizados y no solo añadidos.

[PENDIENTE] El sistema debe validar que cada nombre siga una convención estable del proyecto antes de publicarse.

#### 2. Metadatos útiles para navegación y administración

[PENDIENTE] Cada modelo debería incluir información útil para la gestión operativa del repositorio: tamaño, fecha de creación, fecha de modificación, formato, tags, categoría, visibilidad y relación con proyectos de origen.

[PENDIENTE] La metadata debe ser suficiente para buscar, filtrar y tomar decisiones de publicación sin inspeccionar manualmente cada archivo.

#### 3. Exposición del catálogo en web

[CONFIRMADO] La web debe mostrar cada modelo en un visor 3D con descarga directa.

[PENDIENTE] La web debe soportar navegación eficiente en dispositivos de baja potencia y móviles, con paginación, carga diferida y reducción de visores activos según el hardware.

[PENDIENTE] La interfaz debe permitir filtros por nombre, categoría, fecha, peso, visibilidad y otras propiedades relevantes.

#### 4. Administración y visibilidad del contenido

[PENDIENTE] El propietario o administrador debe poder distinguir entre contenido público, privado y no listado.

[PENDIENTE] El sistema debe permitir marcar favoritos, distinguir visibilidad y controlar qué assets se muestran por defecto para usuarios no autorizados.

[PENDIENTE] Debe existir una capa de administración segura para evitar falsos admins o acceso no autorizado.

#### 5. Soporte para proyectos de origen

[PENDIENTE] El sistema debería poder asociar un modelo con uno o varios archivos de proyecto (Blender, BlockBench, Maya, 3DS Max, etc.), evitando depender de un solo formato.

[PENDIENTE] La relación entre asset y proyecto debe ser explícita para evitar duplicidades o ambigüedades en la gestión del contenido.

### Criterios de aceptación para SDD y IA agente

[CONFIRMADO] La especificación debe ser ejecutable por agentes: clara, verificable, con límites y riesgos definidos.

[CONFIRMADO] Cada objetivo debe responder a una pregunta concreta: qué debe pasar, qué debe evitarse y cuál es el criterio de éxito.

[PENDIENTE] Cada feature de negocio debe tener un "Definition of Done" mínimo: entrada de datos, validación, persistencia, visualización y posible rollback.

[PENDIENTE] El sistema debe distinguir entre requisitos actuales, aspiracionales y riesgos de arquitectura.

### Restricciones y supuestos

[CONFIRMADO] El proyecto sigue siendo estático y no tiene backend de producción establecido.

[CONFIRMADO] Se prioriza simplicidad y velocidad de ejecución sobre complejidad de infraestructura.

[INFERIDO] El repositorio está pensado para GitHub Pages o entorno estático equivalente, no para un sistema multiusuario con base de datos real en producción.

[INFERIDO] La solución actual debe asumir que no existe una identidad de usuario robusta ni una capa de seguridad avanzada por defecto.

### Problemas futuros y riesgos de estos objetivos

[INFERIDO] El principal riesgo es que el proyecto crezca demasiado rápido en complejidad sin una base de datos o una capa de dominio clara. Eso puede derivar en:
  - metadata inconsistente
  - nombrado heterogéneo
  - archivos duplicados o rutas rotas
  - validaciones dispersas entre scripts y UI

[INFERIDO] El manejo de archivos pesados puede convertirse en un problema de coste real: GitHub, almacenamiento, rendimiento de carga, sincronización y despliegue.

[INFERIDO] Si se implementa visibilidad, admin y favoritos sin una capa de autenticación real, se corre el riesgo de introducir "admin oculto" o bypasses de seguridad por lógica frágil.

[INFERIDO] La relación Many-to-Many entre modelos y proyectos de software puede volverse difícil de mantener si no se define un modelo de entidad claro y una política de consistencia.

[INFERIDO] La web en GitHub Pages puede degradar el rendimiento con demasiados visores 3D activos simultáneamente, especialmente en móviles o equipos modestos.

[INFERIDO] La automatización del catálogo puede volverse costosa si se hace sin un historial estable, validación de cambios y estrategia de versionado.

[INFERIDO] La escalabilidad del contenido puede terminar en un repositorio difícil de gestionar si no se separan responsabilidades: archivos fuente, metadata, catálogo público y procesos de publicación.

### Recomendación de redacción para agentes

[CONFIRMADO] La forma más útil de expresar estos objetivos es en lenguaje de especificación con tres capas: objetivo de negocio, requerimiento funcional y riesgo/limitación.

[CONFIRMADO] Para IA agente, conviene dejar explícito lo siguiente en cada feature:
  - entrada de datos
  - validación
  - persistencia
  - renderizado o uso
  - condición de error
  - criterio de aceptación
  - riesgo asociado

[INFERIDO] Esta estructura reduce ambigüedad, mejora la coherencia del trabajo en paralelo y hace que los agentes puedan actuar sin interpretar suposiciones ocultas.

---

## Requisitos adicionales del usuario (roadmap aspiracional)

[CONFIRMADO] El usuario ha indicado una serie de objetivos avanzados para expandir la biblioteca desde un catálogo estático a una plataforma más inteligente y administrable.

### Backend

- [PENDIENTE] Automatizar la adición y actualización de modelos cuando cambien sus metadatos o su fecha de modificación.
- [PENDIENTE] Mantener un historial de versiones y cambios de cada asset.
- [PENDIENTE] Validar el nombre del archivo y el naming convention del proyecto.
- [PENDIENTE] Analizar e indexar propiedades del modelo: tamaño, topología, formato, tags, fecha de creación/modificación, y otros atributos útiles.
- [PENDIENTE] Detectar tamaños de archivo críticos y mover modelos pesados a carpetas gestionadas explícitamente.
- [PENDIENTE] Definir una estrategia de seguridad para distinguir propietario, admin y usuario estándar.
- [PENDIENTE] Soportar proyectos de origen asociados a cada asset, independientemente del software utilizado.
- [PENDIENTE] Establecer una relación muchos-a-muchos entre modelos y proyectos de creación.

### Frontend

- [PENDIENTE] Optimizar el catálogo para móvil y pantallas de baja capacidad con paginación, carga diferida y adaptaciones automáticas.
- [PENDIENTE] Detectar capacidades del dispositivo y ajustar la carga de visores 3D.
- [PENDIENTE] Añadir filtros por nombre, categoría, peso, fecha y visibilidad.
- [PENDIENTE] Mejorar la UI responsive y la legibilidad del catálogo.
- [PENDIENTE] Añadir iconos, etiquetas y metadatos visuales para programas, tags y umbrales de peso.
- [PENDIENTE] Añadir descripción breve, enlaces externos y contexto de uso del asset.

### Admin / propietario

- [PENDIENTE] Permitir visibilidad pública, privada o no listada.
- [PENDIENTE] Permitir filtrar contenido según visibilidad para admin o propietario.
- [PENDIENTE] Añadir favoritos con flag de usuario.
- [PENDIENTE] Añadir una vía oculta de administración segura para activación de modo admin.
- [PENDIENTE] Permitir descarga directa del modelo y del proyecto asociado.

### Infraestructura y mantenimiento

- [PENDIENTE] Reconsiderar la base de datos o capa de persistencia a medida que el catálogo crezca.
- [PENDIENTE] Diseñar un flujo de CI/CD para actualización del catálogo y despliegue en GitHub Pages.
- [PENDIENTE] Añadir recordatorios y validaciones de publicación para evitar que la web quede desactualizada respecto al repositorio.
