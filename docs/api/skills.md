# API de Skills

## Listar skills

```http
GET /api/skills
```

**Nota**: Este endpoint **excluye archivos `.py`** intencionalmente. Los skills `.py` (como `base_documento.py`) son de uso interno y no deben aparecer en el listado de usuario. Para obtener un `.py` individual, usar `GET /api/skills/{id}`.

Respuesta:

```json
[
  {
    "id": "EstructuraIntegrador",
    "name": "Skill: Generador de Documentos .docx (UNIFRANZ / APA 7)",
    "description": "Genera documentos...",
    "type": "md",
    "filename": "EstructuraIntegrador.md",
    "content": "# Skill: ...",
    "created_at": "2026-05-30T03:02:00"
  }
]
```

## Obtener skill

```http
GET /api/skills/{id}
```

## Crear skill

```http
POST /api/skills
Content-Type: application/json

{
  "name": "Mi Skill",
  "description": "Descripcion",
  "content": "# Estructura del documento\n\n## Seccion 1\n...",
  "type": "md"
}
```

Campos:
- `name` (requerido): Nombre de la skill
- `description`: Descripcion corta
- `content` (requerido): Contenido/estructura en Markdown o Python
- `type` (opcional, default `md`): `md`, `py` o `txt`

## Actualizar skill

```http
PUT /api/skills/{id}
Content-Type: application/json

{
  "name": "Nuevo nombre",
  "content": "Nuevo contenido..."
}
```

Todos los campos son opcionales en actualizacion.

## Eliminar skill

```http
DELETE /api/skills/{id}
```

Respuesta: `{ "status": "deleted", "id": "mi-skill" }`
