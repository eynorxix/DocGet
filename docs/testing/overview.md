# Testing

**Framework**: pytest

## Ejecutar tests

```bash
cd docgent
poetry run pytest -v
```

## Estructura

```
tests/
+-- conftest.py              Fixtures compartidos
+-- test_health.py           Test del health endpoint
+-- test_chat.py             Tests del agente IA (herramientas, headers, endpoint)
+-- test_documents.py        Tests de documentos (upload, generate, download, preview, list)
+-- test_skills.py           Tests de skills (CRUD, exclusion de .py)
+-- test_file_reader.py      Tests de lectura de archivos
```

## Test por archivo

### test_health.py
- `GET /health` devuelve estado OK
- `GET /` devuelve HTML (interfaz web)

### test_chat.py
- `process_message()` con herramientas (list_skills, list_documents)
- `process_message()` sin herramientas (respuesta directa)
- `POST /api/chat` endpoint funcional
- Header `X-Caratula` se incluye en el prompt
- Header `X-Gemini-Keys` se usa para la llamada a Gemini

### test_documents.py
- `generate_docx()` con y sin `base_documento.py`
- `generate_docx()` con logo fallback
- `generate_docx()` con contenido de tablas
- `generate_docx()` con contenido vacio
- Listar documentos: `GET /api/documents/list`
- Descargar documento: `GET /api/documents/download/{filename}`
- Vista previa: `GET /api/documents/preview/{filename}`
- Subir archivo: `POST /api/documents/upload`
- Eliminar archivo: `DELETE /api/documents/uploads/{filename}`
- Descargar documento inexistente devuelve 404

### test_skills.py
- `list_skills()` excluye archivos `.py`
- `get_skill()` encuentra archivos `.py` aunque no esten en el listado
- Crear y eliminar skill
- CRUD via API endpoints (crear, listar, obtener, actualizar, eliminar)

### test_file_reader.py
- `ensure_upload_dir()` crea directorio si no existe
- `get_file_summary()` devuelve resumen de archivo
- Archivo inexistente devuelve None

## Fixtures (conftest.py)

- `client`: `TestClient` de FastAPI para tests de integracion
- `sample_skill_data`: datos de ejemplo para crear skills en tests

## Notas

- Los tests usan la API de Gemini real si hay `GEMINI_API_KEY` configurada
- Sin key, usan fallback local (no requieren internet)
- Los tests crean archivos temporales en `data/` que se limpian automaticamente
