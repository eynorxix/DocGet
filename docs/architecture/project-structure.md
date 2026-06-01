# Estructura del proyecto

```
docgent/
+-- pyproject.toml              Configuracion de Poetry
+-- .env                        Variables de entorno (GEMINI_API_KEY)
+-- .env.example                Plantilla del .env
+-- app/
|   +-- __init__.py
|   +-- main.py                 Punto de entrada: FastAPI + load_dotenv + Jinja2Templates
|   +-- models/
|   |   +-- __init__.py
|   |   +-- schemas.py          Esquemas Pydantic (SkillCreate, GenerateRequest,
|   |                            GenerateDirectRequest, UploadResponse, etc.)
|   +-- routers/
|   |   +-- __init__.py
|   |   +-- skills.py           Endpoints CRUD de skills
|   |   +-- documents.py        Endpoints: upload, generate, generate-direct,
|   |   |                        generate-demo, download, list, preview, delete
|   |   +-- chat.py             Endpoint POST /api/chat (agente IA conversacional)
|   +-- services/
|   |   +-- __init__.py
|   |   +-- skill_loader.py     Lectura/escritura de skills en disco (excluye .py)
|   |   +-- file_reader.py      Lectura de archivos subidos (multi-formato)
|   |   +-- document_generator.py  Generacion de .docx con python-docx
|   |   |                        (soporta **bold** y *italic* inline en parrafos)
|   |   +-- gemini_service.py   Integracion con Google Gemini API + busqueda web
|   |   |                        (fallback con web_search cuando Gemini no disponible)
|   |   +-- chat_service.py     Agente IA con 11 herramientas y rotacion de keys
|   |   +-- web_search.py       Busqueda en internet via DuckDuckGo (sin API key)
|   |                            (traduccion español->ingles, multi-query retry)
|   +-- static/
|   |   +-- css/
|   |   |   +-- style.css       Tema oscuro completo (200 lineas)
|   |   +-- js/
|   |       +-- app.js          Toda la logica del frontend (~620 lineas)
|   +-- templates/
|       +-- index.html          Orquestador Jinja2 (incluye 7 partials)
|       +-- partials/
|           +-- _header.html
|           +-- _sidebar.html   (sidebar con caratula, demo, skills, acciones)
|           +-- _workspace.html
|           +-- _input.html     (3 botones circulares: Documentos, Skill, Generar)
|           +-- _file_inputs.html
|           +-- _modals.html    (8 modales: skill, editar, keys, selector, generar,
|                                bienvenida, donacion, preview)
|           +-- _lightbox.html
+-- data/
|   +-- skills/                 Skills precargadas y creadas por el usuario
|   |   +-- base_documento.py   Modulo base de python-docx (formato APA 7) - OCULTO
|   |   |                        (add_paragraph/add_bullets soportan **bold** y *italic*)
|   |   +-- EstructuraIntegrador.md  Skill para tesis UNIFRANZ
|   |   +-- humano.md           Skill de estilo de escritura humana
|   |   +-- Skill-Controladores.md   Skill para documentos tecnicos IoT
|   +-- uploads/                Archivos subidos por usuarios
|   +-- output/                 Documentos .docx generados
+-- assets/
|   +-- cripto/                 QR codes para donaciones
|       +-- Bitcoin.jpg
|       +-- Polygon.jpg
|       +-- BnBChain.jpg
+-- tests/
|   +-- conftest.py             Fixtures compartidos (TestClient, sample_skill_data)
|   +-- test_health.py          Health endpoint
|   +-- test_chat.py            Agente IA, herramientas, headers, web_search
|   +-- test_documents.py       CRUD documentos, generate, preview, descarga, demo
|   +-- test_skills.py          CRUD skills, exclusion de .py
|   +-- test_file_reader.py     Lectura de archivos
+-- docs/                       Documentacion (markdown)
    +-- index.md
    +-- architecture/
    +-- setup/
    +-- api/
    +-- frontend/
    +-- services/
    +-- skills/
    +-- deployment/
    +-- testing/
```

## Notas

- Los archivos `.py` en `data/skills/` (como `base_documento.py`) **no aparecen** en el listado de skills del usuario, pero si se pueden obtener individualmente con `get_skill()`. Logica intencional para skills de sistema.
- `data/output/` y `data/uploads/` se crean automaticamente al primer uso.
- El frontend usa **Jinja2 partials** (7 archivos) orquestados desde `index.html`.
- Los estilos y scripts estan en archivos separados (`static/css/style.css`, `static/js/app.js`).
- La busqueda web usa `ddgs` v9 (DuckDuckGo), sin API key, con reintentos automaticos y traduccion de terminos español a ingles.
