# Skill Loader Service

**Archivo**: `app/services/skill_loader.py`

## Proposito

Gestiona las Skills (plantillas de estructura documental) almacenadas como archivos en `data/skills/`.

## Funciones principales

```python
list_skills() -> list[dict]
```
Lista todas las skills disponibles. **Excluye archivos `.py`** intencionalmente (solo lista `.md`, `.txt`, `.json`).
Cada skill incluye:
- `id`: nombre del archivo sin extension
- `name`: primera linea del contenido (limpia de # o """)
- `description`: linea posterior a "## Descripcion"
- `type`: extension (md, txt, json)
- `filename`: nombre del archivo
- `content`: contenido completo
- `created_at`: fecha de modificacion del archivo

```python
get_skill(skill_id: str) -> dict | None
```
Obtiene una skill por su ID. Busca en orden: `.md`, `.py`, `.txt`, `.json`. **Si encuentra `.py`**, lo incluye en la respuesta (aunque no aparezca en `list_skills()`).

```python
create_skill(name, description, content, skill_type="md") -> dict
```
Crea un nuevo archivo de skill en `data/skills/`. Si es `.md`, antepone `# Nombre` y `## Descripcion`. Si es `.py`, envuelve en docstring `"""..."""`.

```python
update_skill(skill_id, name, description, content) -> dict | None
```
Actualiza el contenido de una skill existente.

```python
delete_skill(skill_id) -> bool
```
Elimina el archivo de skill.

## Logica de exclusion de .py

Los archivos `.py` en `data/skills/` son skills de **sistema** (como `base_documento.py`) usadas internamente por `document_generator.py`. No deben aparecer en el listado de skills del usuario para evitar confusion.

- `list_skills()`: excluye `.py`
- `get_skill()`: **si** encuentra `.py` (para uso interno)
- El frontend usa `list_skills()` para mostrar la lista, por lo que el usuario nunca ve `base_documento.py`

## Formato de archivos

### Markdown (.md)
```markdown
# Nombre de Skill

## Descripcion
Descripcion corta

## Contenido
Estructura del documento...
```

### Python (.py)
```python
"""
Nombre de Skill

Descripcion corta
"""

def generar():
    pass
```

### Texto (.txt)
```
Contenido plano...
```
