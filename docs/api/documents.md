# API de Documentos

## Subir archivo

```http
POST /api/documents/upload
Content-Type: multipart/form-data

file: @archivo.md
```

Respuesta:

```json
{
  "filename": "archivo.md",
  "extension": ".md",
  "size_kb": 1.5,
  "preview": "# Contenido del archivo\n..."
}
```

Formatos aceptados: `.md`, `.py`, `.txt`, `.csv`, `.json`, `.yaml`, `.yml`.

## Listar archivos subidos

```http
GET /api/documents/uploads
```

## Eliminar archivo subido

```http
DELETE /api/documents/uploads/{filename}
```

## Generar documento

```http
POST /api/documents/generate
Content-Type: application/json

{
  "skill_id": "EstructuraIntegrador",
  "title": "Titulo del Proyecto",
  "author": "Nombre Autor",
  "tutor": "Nombre Tutor",
  "content_input": "Instrucciones para el contenido del documento"
}
```

Campos:
- `skill_id` (requerido): ID de la skill a usar
- `title` (requerido): Titulo del documento
- `author`: Nombre del autor (para la caratula)
- `tutor`: Nombre del tutor (para la caratula)
- `content_input`: Instrucciones adicionales para la IA

Respuesta:

```json
{
  "status": "success",
  "download_url": "/api/documents/download/Titulo_del_Proyecto.docx",
  "filename": "Titulo_del_Proyecto.docx"
}
```

## Descargar documento

```http
GET /api/documents/download/{filename}
```

Devuelve el archivo `.docx` para descargar.

## Listar documentos generados

```http
GET /api/documents/list
```

```json
[
  {
    "filename": "Titulo_del_Proyecto.docx",
    "size_kb": 165.2,
    "created": 1748564321.0
  }
]
```

## Generar documento directo (sin IA)

```http
POST /api/documents/generate-direct
Content-Type: application/json

{
  "title": "Distribuciones de Linux",
  "author": "Brayan Quispe",
  "tutor": "Lazcano Andres",
  "topic": "principales distribuciones de linux usos y caracteristicas"
}
```

Este endpoint:
1. Busca informacion en internet sobre el `topic` usando DuckDuckGo
2. Estructura los resultados como contenido del documento
3. Usa la primera skill disponible como plantilla
4. Genera el `.docx` sin necesidad de API keys de Gemini

Respuesta:

```json
{
  "status": "success",
  "download_url": "/api/documents/download/Distribuciones_de_Linux.docx",
  "filename": "Distribuciones_de_Linux.docx"
}
```

## Vista previa del documento

```http
GET /api/documents/preview/{filename}
```

Devuelve JSON estructurado con el contenido del `.docx`:

```json
{
  "paragraphs": [
    {"text": "Titulo del documento", "bold": true, "italic": false, "size": 24, "style": "Title"},
    {"text": "Contenido del parrafo...", "bold": false, "italic": false, "size": 12, "style": "Normal"}
  ],
  "tables": [
    [["Col1", "Col2"], ["Val1", "Val2"]]
  ]
}
```

Usado por el modal `#previewOverlay` en el frontend para mostrar una vista previa antes de descargar.
