# Arquitectura del sistema

## Diagrama general

```
[Usuario/Navegador]
     |
     | HTTP (localhost:8000)
     v
[FastAPI Server]
     |
     |--- /api/chat/*           --> Agente IA conversacional (chat_service.py)
     |--- /api/skills/*          --> CRUD de skills (archivos en data/skills/)
     |--- /api/documents/*       --> Upload, generar, generate-direct, generate-demo,
     |                               descargar, preview, listar
     |--- /                      --> Interfaz web HTML (Jinja2)
     |
     v
[Servicios internos]
     |
     |--- chat_service.py        --> Agente IA con 11 herramientas
     |--- skill_loader.py        --> Lee/escribe skills en data/skills/
     |--- file_reader.py         --> Lee archivos subidos (data/uploads/)
     |--- web_search.py          --> Busqueda DuckDuckGo (traduccion ES->EN, multi-query)
     |--- gemini_service.py      --> LLama a Gemini API, fallback con web_search
     |--- document_generator.py  --> Genera .docx con python-docx (formato APA 7,
     |                               **bold**, *italic*, tablas, listas)
     |
     v
[data/]
     |--- skills/   Archivos .md, .py, .txt
     |--- uploads/  Archivos subidos por usuarios
     |--- output/   Documentos .docx generados
```

## Flujo de generacion de documento (con IA)

1. Usuario selecciona una Skill (o la crea)
2. Usuario escribe instrucciones y hace click en "generar"
3. `documents.py` router recibe la peticion
4. `skill_loader.py` carga el contenido de la skill desde `data/skills/`
5. `file_reader.py` extrae el contenido de todos los archivos subidos
6. `web_search.py` busca en internet informacion relevante sobre el tema
7. `gemini_service.py` envia a Gemini: skill + archivos + busqueda web + instrucciones
8. Gemini devuelve el contenido del documento en Markdown
9. `document_generator.py` genera un `.docx` con formato APA 7 (caratula, TOC, tablas,
   **negritas**, *cursivas*, listas, referencias, numeracion de pagina)
10. El archivo se guarda en `data/output/` y se devuelve la URL de descarga

## Flujo de generacion directa (sin IA, con busqueda web)

1. Usuario hace clic en boton **"Generar"** del panel de input
2. O llama a `POST /api/documents/generate-direct`
3. `web_search.py` busca en internet sobre el topic indicado
4. Los resultados se estructuran directamente como contenido del documento
5. `document_generator.py` genera el `.docx`
6. Se devuelve URL de descarga, sin necesidad de API keys de Gemini

## Flujo de chat con agente IA

1. Usuario escribe un mensaje en el input
2. Se envia a `POST /api/chat` con historial y headers `X-Gemini-Keys` + `X-Caratula`
3. `chat_service.py` procesa: envia a Gemini con system prompt y **11 herramientas**
4. Si Gemini responde con `---TOOL---`, se ejecuta la herramienta correspondiente
5. Si Gemini responde con texto normal, se devuelve al usuario formateado en Markdown
6. El agente puede: listar/crear/editar/eliminar skills, generar documentos, buscar en
   internet, solicitar archivos, mostrar selector visual de skills
7. El agente **valida que la skill coincida con el tema** solicitado por el usuario

## Modo sin IA

Si no hay `GEMINI_API_KEY` configurada (ni en `.env` ni en headers):

- El **chat** funciona igual pero con respuestas genericas de fallback
- La **generacion de documentos** usa `web_search()` para buscar informacion en internet
  y estructurarla como contenido, sin pasar por Gemini
- El boton **"Generar"** del frontend siempre funciona sin IA
- Sirve para probar todo el sistema sin depender de APIs externas

## Rotacion de API Keys

- Se pueden configurar hasta **4 keys de Gemini** en el frontend
- Si una key responde con `429` (quota exceeded), se pone en cooldown y se prueba la siguiente
- Se necesitan keys de **al menos 2 cuentas distintas** de Google Cloud para que la rotacion sea efectiva

## Herramientas del agente

| Herramienta | Descripcion |
|---|---|
| `list_skills()` | Lista todas las skills disponibles |
| `get_skill(skill_id)` | Muestra contenido completo de una skill |
| `create_skill(...)` | Crea una nueva skill |
| `update_skill(...)` | Actualiza skill existente |
| `delete_skill(skill_id)` | Elimina una skill |
| `generate_document(...)` | Genera documento .docx completo |
| `list_uploads()` | Lista archivos subidos |
| `list_documents()` | Lista documentos generados |
| `request_file_upload()` | Pide al usuario que suba un archivo |
| `request_skill_select()` | Abre el modal visual de seleccion de skills |
| `web_search(query)` | Busca informacion actualizada en internet |
