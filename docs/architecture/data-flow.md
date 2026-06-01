# Flujo de datos

## Upload de archivos

```
[Usuario] --POST /api/documents/upload--> [documents.py]
                                                |
                                          [file_reader.py]
                                                |
                                          data/uploads/archivo.ext
```

## CRUD de skills

```
[Usuario] --GET/POST/PUT/DELETE /api/skills/*--> [skills.py]
                                                      |
                                                [skill_loader.py]
                                                      |
                                                data/skills/nombre.md
```

## Generacion de documento (con IA)

```
[Usuario] --POST /api/documents/generate--> [documents.py]
                                                  |
                       +--------------------------+--------------------------+
                       |                          |                          |
                [skill_loader.py]         [file_reader.py]          [web_search.py]
                       |                          |                    (DuckDuckGo)
                data/skills/skill.md    data/uploads/*.*                  |
                       |                          |                    Internet
                       +--------------------------+--------------------------+
                                                  |
                                          [gemini_service.py]
                                   (skill + archivos + web + instrucciones)
                                                  |
                                                  v
                                             Gemini API
                                                  |
                                        [document_generator.py]
                                        (formato APA 7, **bold**, *italic*,
                                         tablas, listas, TOC, referencias)
                                                  |
                                                  +--> base_documento.py (formato)
                                                  |
                                          data/output/doc.docx
                                                  |
                                          URL de descarga al usuario
```

## Generacion directa (sin IA)

```
[Usuario] --click "Generar"--> [handleGenerateDirect()]
                                      |
                          POST /api/documents/generate-direct
                                      |
                              [web_search.py] (DuckDuckGo)
                                      |
                                  Internet
                                      |
                              Resultados estructurados
                                      |
                              [document_generator.py]
                                      |
                              data/output/doc.docx
                                      |
                              URL de descarga + preview
```

## Documento demo

```
[Usuario] --click "Documento .docx prueba"--> [generateDemoDoc()]
                                                    |
                                        POST /api/documents/generate-demo
                                                    |
                                        Contenido predefinido con:
                                        tablas, listas, bold, italic, indices
                                                    |
                                        [document_generator.py]
                                                    |
                                        data/output/Documento_de_Prueba.docx
                                                    |
                                        URL de descarga + preview
```

## Chat con agente IA

```
[Usuario] --POST /api/chat--> [chat.py]
                                   |
                          [chat_service.py]
                                   |
                     [Gemini API + 11 herramientas]
                                   |
               +-------------------+-------------------+
               |                                       |
        ---TOOL--- + JSON                        Texto normal
               |                                       |
        Ejecuta herramienta                     Renderiza Markdown
        (skills, uploads, docs,                     en workspace
         web_search, etc.)
               |
        {response, data, action}
```

## Preview de documento

```
[Usuario] --GET /api/documents/preview/{filename}--> [documents.py]
                                                             |
                                                   [document_generator.py]
                                                             |
                                                   Extrae: parrafos (estilo,
                                                   bold, italic, size) + tablas
                                                             |
                                                   JSON estructurado
                                                             |
                                                   Renderizado en #previewOverlay
```

## Flujo de donacion

```
[Usuario] click ❤️ Doname
                |
        Abre #donateOverlay
                |
        Muestra QR de 3 criptomonedas
                |
        Click en QR
                |
        Abre #lightbox con imagen grande
                |
        Auto-cierra a los 30s
```

## Formato de datos

### Request de generacion

```json
{
  "skill_id": "EstructuraIntegrador",
  "title": "Titulo del proyecto",
  "author": "Nombre del autor",
  "tutor": "Nombre del tutor",
  "content_input": "Instrucciones para la IA"
}
```

### Request de generacion directa

```json
{
  "title": "Distribuciones de Linux",
  "author": "Brayan Quispe",
  "tutor": "Lazcano Andres",
  "topic": "principales distribuciones de linux usos y caracteristicas"
}
```

### Response de generacion

```json
{
  "status": "success",
  "download_url": "/api/documents/download/doc.docx",
  "filename": "doc.docx"
}
```

### Chat request

```json
{
  "message": "crea una skill de pruebas",
  "history": []
}
```

Headers:
- `X-Gemini-Keys`: JSON array de keys (opcional)
- `X-Caratula`: JSON con {titulo, autor, tutor} (opcional)

### Chat response

```json
{
  "response": "Texto de respuesta del agente",
  "data": {},
  "action": null
}
```

### Preview response

```json
{
  "paragraphs": [
    {"text": "Texto del parrafo", "bold": false, "italic": false, "size": 12, "style": "Normal"},
    {"text": "Titulo", "bold": true, "italic": false, "size": 16, "style": "Heading 2"}
  ],
  "tables": [
    [["celda1", "celda2"], ["celda3", "celda4"]]
  ]
}
```

### Skill en disco (Markdown)

```markdown
# Nombre de la Skill

## Descripcion
Descripcion corta

## Contenido
Estructura del documento en Markdown...
```

### Skill en disco (Python)

```python
"""
Nombre de la Skill

Descripcion corta
"""

# Codigo Python con la logica de generacion
```
