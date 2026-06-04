# Chat Service

**Archivo**: `app/services/chat_service.py`

## Proposito

Agente IA conversacional que entiende lenguaje natural y ejecuta acciones a traves de herramientas.

## Como funciona

1. Recibe un mensaje del usuario via `POST /api/chat`
2. Construye un prompt completo con:
   - System prompt (75 lineas con instrucciones detalladas)
   - Historial de la conversacion
   - Datos de caratula (del header `X-Caratula`)
   - API keys (del header `X-Gemini-Keys` o `GEMINI_API_KEY` de `.env`)
3. Envia a Gemini API
4. Gemini responde con texto o con `---TOOL---` + JSON para ejecutar una herramienta

## Herramientas disponibles

El agente tiene acceso a **10 herramientas**:

| Herramienta | Descripcion |
|---|---|
| `list_skills()` | Lista todas las skills |
| `get_skill(skill_id)` | Muestra contenido completo de una skill |
| `create_skill(name, desc, content, type)` | Crea skill (genera contenido si falta) |
| `update_skill(skill_id, name, desc, content)` | Actualiza skill existente |
| `delete_skill(skill_id)` | Elimina skill |
| `generate_document(...)` | Genera .docx completo (skill_id, title, author, tutor, content_input) |
| `list_uploads()` | Lista archivos subidos |
| `list_documents()` | Lista documentos generados |
| `request_file_upload()` | Pide al usuario subir un archivo |
| `request_skill_select()` | Muestra selector visual de skills en el frontend |
| `web_search(query)` | Busca informacion actualizada en internet (DuckDuckGo) para mejorar la calidad del contenido |

## Ejecucion de herramientas

Cuando Gemini responde con `---TOOL---`, el servicio:

1. Extrae el JSON con `name` y `args`
2. Busca la funcion en el registro de herramientas
3. Ejecuta la funcion con los argumentos
4. Formatea el resultado
5. Lo devuelve como parte del response

### Limpieza automatica de uploads

Despues de ejecutar `generate_document`, `create_skill` o `update_skill`, el sistema llama a `_cleanup_uploads()` que elimina todos los archivos en `data/uploads/`. Esto evita que archivos temporales (subidos via Caja Negra o como contexto) persistan y contaminen generaciones futuras.

Los archivos subidos via Caja Negra tambien se limpian al abrir una nueva sesion de Caja Negra (el frontend elimina uploads previos antes de subir nuevos).

## Rotacion de API Keys

- Mantiene un diccionario compartido `_key_cooldowns` con timestamps de cooldown
- `_get_available_keys()`: filtra keys que no estan en cooldown
- Si todas las keys estan en cooldown, usa fallback local
- Si una key responde `429`, se pone en cooldown por el tiempo indicado en `retryDelay`

## Formato de respuesta

```python
{
    "response": str,   # Texto en Markdown para mostrar al usuario
    "data": dict,      # Datos extra (resultados de herramientas, previews)
    "action": str|null # Accion a ejecutar en el frontend (ej: "request_skill_select")
}
```

## Dependencias

- `google-generativeai` (Gemini API)
- `skill_loader` (para operaciones con skills)
- `document_generator` (para generar documentos)
- `file_reader` (para listar uploads)
- `web_search` (busqueda en internet via DuckDuckGo)
