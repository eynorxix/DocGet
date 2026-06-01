# API REST

Base URL: `http://localhost:8000/api`

## Endpoints

| Metodo | Ruta | Descripcion |
|---|---|---|
| `GET` | `/health` | Estado del servidor |
| `GET` | `/` | Interfaz web (HTML) |
| `POST` | `/api/chat` | Chat con agente IA (headers: `X-Gemini-Keys`, `X-Caratula`) |
| `GET` | `/api/skills` | Listar skills (excluye `.py`) |
| `GET` | `/api/skills/{id}` | Obtener skill por ID (incluye `.py`) |
| `POST` | `/api/skills` | Crear skill |
| `PUT` | `/api/skills/{id}` | Actualizar skill |
| `DELETE` | `/api/skills/{id}` | Eliminar skill |
| `POST` | `/api/documents/upload` | Subir archivo |
| `GET` | `/api/documents/uploads` | Listar archivos subidos |
| `DELETE` | `/api/documents/uploads/{filename}` | Eliminar archivo subido |
| `POST` | `/api/documents/generate` | Generar documento .docx |
| `GET` | `/api/documents/download/{filename}` | Descargar .docx |
| `GET` | `/api/documents/list` | Listar documentos generados |
| `GET` | `/api/documents/preview/{filename}` | Vista previa del documento (JSON con parrafos y tablas) |
| `POST` | `/api/documents/generate-direct` | Generar documento directo con busqueda web (sin IA) |
| `POST` | `/api/documents/generate-demo` | Generar documento demo con todas las capacidades (tablas, indices, formato APA) |

## Autenticacion

No requiere autenticacion en esta version. Corresponde al usuario implementarla (API keys).

Las API keys de Gemini se pasan por header `X-Gemini-Keys` como JSON array, no por autenticacion HTTP.

## Formato

Todas las peticiones y respuestas usan JSON, excepto:
- `POST /api/documents/upload` usa `multipart/form-data`
- `GET /api/documents/download/{filename}` devuelve el archivo binario
- `GET /` devuelve HTML
