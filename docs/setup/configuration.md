# Configuracion

## Variables de entorno (`.env`)

| Variable | Obligatoria | Descripcion |
|---|---|---|
| `GEMINI_API_KEY` | No | API key de Google Gemini. Sin ella, el sistema usa contenido de relleno. |

## Puertos

El servidor corre en `0.0.0.0:8000` por defecto. Se puede cambiar en `app/main.py`:

```python
uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

## Directorios de datos

| Directorio | Proposito | Se crea automaticamente |
|---|---|---|
| `data/skills/` | Skills instaladas | Si, con copia de las originales |
| `data/uploads/` | Archivos subidos | Si, al primer upload |
| `data/output/` | Documentos generados | Si, al primer .docx |

## Skills precargadas

Las skills se copian desde `/home/eynor/Documentos/Biblioteca/skills/` al crear el proyecto. Los originales no se modifican.

Para aniadir mas skills precargadas, copia archivos `.md`, `.py` o `.txt` a `data/skills/`.

## Logo

El logo de UNIFRANZ se busca en `/home/eynor/Documentos/Biblioteca/logoUnifranz/logounifranz.png`. Si no existe, se genera el documento sin logo.
