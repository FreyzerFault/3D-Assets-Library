# Organización de modelos

Esta carpeta contiene los activos 3D del catálogo.

## Convención de almacenamiento

- `models/`: modelos finales listos para consumir desde la web.
- `models/large/`: archivos de más de 100 MB y hasta 2 GB. Se mantienen separados para facilitar revisión y control de tamaño sin introducir complejidad innecesaria.
- `models/2gb-plus/`: archivos mayores de 2 GB. Se excluyen del repositorio y deben manejarse con Git LFS o almacenamiento externo según la política del proyecto.
- `models/projects/`: proyectos de origen del contenido (`.blend`, `.fbx`, `.max`, `.ma`, etc.) y archivos auxiliares no destinados a la web.

## Regla general

Los assets que se publican en la web deben seguir rutas relativas simples como `models/archivo.glb` o `models/large/archivo.glb`.
