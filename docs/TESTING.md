# TESTING.md

## Propósito

---

Este documento describe la metodología de testing del proyecto, cómo ejecutar la suite existente, criterios de calidad y prácticas que deben seguir tanto colaboradores humanos como agentes.

## Ejecutar los tests

---

- Ejecutar con unittest integrado de Python (sin introducir nuevas dependencias de runtime):
  python -m unittest discover -v

  Nota: en algunos entornos con rutas especiales/disco con espacios la detección automática puede fallar; como alternativa ejecutar los módulos de tests explícitamente:
  python -m unittest tests.test_generate_assets_data tests.test_generate_assets_data_more -v

- Ejecutar un único archivo de tests:
  python -m unittest tests.test_generate_assets_data -v

- Ejecutar cobertura local:
  python -m pip install coverage
  coverage run -m unittest discover -s tests -v
  coverage report --show-missing

- Recomendación: ejecutar desde la raíz del repositorio. Las utilidades del proyecto (generate_assets_data.py) ya están pensadas para resolver rutas relativas al script.

## Validaciones locales y pre-commit

---

- Instalar herramientas de calidad localmente:
  python -m pip install pre-commit black flake8 coverage

- Preparar hooks locales:
  pre-commit install

- Ejecutar todas las validaciones manualmente:
  pre-commit run --all-files
  python -m unittest discover -v
  coverage run -m unittest discover -s tests -v
  coverage report --show-missing

## Estrategia y convenciones

---

- Mantener tests unitarios pequeños, deterministas y rápidos.
- Usar archivos temporales (tempfile.TemporaryDirectory) cuando sea necesario para evitar efectos colaterales.
- Evitar mocks excesivos: preferir crear artefactos reales en directorios temporales cuando el código interactúa con el sistema de archivos.
- Los tests deben comprobar tanto el comportamiento nominal como los casos de error (archivos faltantes, rutas absolutas, entradas inválidas).
- Nombrado: tests/test\__.py y clases Test_ para mantener consistencia con unittest.

## Política de agentes y flujo de trabajo (resumen)

---

- Ejecutar la suite de tests tras completar cualquier tarea o cambio en código.
- Si los tests fallan:
  1. Re-ejecutar los tests (descartar fallos transitorios).
  2. Revisar si los tests están mal escritos o desactualizados; si es el caso, corregir los tests.
  3. Si los tests son correctos, priorizar arreglar el código hasta que la suite pase.
  4. No proseguir con nuevas tareas si la suite está rota.

## Cobertura y qué añadir ahora

---

Priorizar tests para:

- Carga/parseo de assets.json (formato inválido, archivo inexistente).
- Normalización de nombres y rutas (incluyendo separadores Windows y Unix).
- Detección de duplicados (por archivo y por nombre normalizado).
- Rechazo de rutas absolutas en assets.json.
- Metadatos de archivo (size_bytes y modified_at), incluyendo comportamiento cuando falta el archivo.
- Umbrales de advertencia para archivos grandes (10 MB / 100 MB), incluyendo límites exactos.
- collect_new_assets: detectar que sólo se añaden .glb y que no se duplican entradas.

## Buenas prácticas de mantenimiento

---

- Los tests deben ser parte integrante de cada cambio: actualizar tests cuando la especificación cambia.
- Mantener la suite rápida (< 5s para cambios pequeños) para feedback rápido.
- Añadir pruebas de integración mínimas cuando se cambie la persistencia o el formato del catálogo.

## Sugerencia para CI

---

- Añadir un workflow de GitHub Actions que ejecute: python -m unittest discover -v. Esto proporciona verificación de PR y evita regresiones.

## Notas finales

---

Este documento pretende ser conciso y accionable. Si se añade una nueva herramienta de testing más adelante (pytest, coverage), documentarla aquí y convertir los tests gradualmente manteniendo compatibilidad.
