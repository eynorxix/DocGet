# API de Chat

## Chat con agente IA

```http
POST /api/chat
Content-Type: application/json
X-Gemini-Keys: ["key1", "key2"]
X-Caratula: {"titulo": "Mi Tesis", "autor": "Juan", "tutor": "Pedro"}
```

```json
{
  "message": "crea una skill de prueba",
  "history": [
    {"role": "user", "content": "mensaje anterior"},
    {"role": "assistant", "content": "respuesta anterior"}
  ]
}
```

Campos:
- `message` (requerido): Mensaje del usuario
- `history` (opcional): Array de mensajes previos para contexto

Headers (opcionales):
- `X-Gemini-Keys`: JSON array de API keys de Gemini para rotacion
- `X-Caratula`: JSON con `{titulo, autor, tutor}` para autocompletar documentos

Respuesta:

```json
{
  "response": "Texto Markdown de respuesta del agente",
  "data": {},
  "action": null
}
```

## Herramientas del agente

El agente IA tiene acceso a estas herramientas, que ejecuta automaticamente segun la conversacion:

| Herramienta | Descripcion |
|---|---|
| `list_skills()` | Lista todas las skills disponibles |
| `get_skill(skill_id)` | Muestra contenido completo de una skill |
| `create_skill(name, desc, content, type)` | Crea una nueva skill (genera contenido si no se provee) |
| `update_skill(skill_id, name, desc, content)` | Actualiza skill existente |
| `delete_skill(skill_id)` | Elimina skill |
| `generate_document(...)` | Genera documento .docx completo |
| `list_uploads()` | Lista archivos subidos |
| `list_documents()` | Lista documentos generados |
| `request_file_upload()` | Pide al usuario que suba un archivo |
| `request_skill_select()` | Abre el modal visual de seleccion de skills |
| `web_search(query)` | Busca en internet informacion actualizada (DuckDuckGo, sin API key) |

## Formato de ejecucion de herramientas

Gemini responde con:
```
---TOOL---
{"name": "list_skills", "args": {}}
```

El servidor ejecuta la herramienta y devuelve el resultado.

## Rotacion de API Keys

- Hasta **4 keys** en el header `X-Gemini-Keys`
- Si una key falla con `429` (quota exceeded), se pone en cooldown
- El sistema prueba la siguiente key disponible
- Las keys del mismo proyecto Google comparten cuota; se necesitan cuentas distintas
