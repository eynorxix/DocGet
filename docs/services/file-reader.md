# File Reader Service

**Archivo**: `app/services/file_reader.py`

## Proposito

Lee archivos subidos por el usuario y extrae su contenido para usarlo como contexto en la generacion de documentos.

## Formatos soportados

| Extension | Lectura | Resumen |
|---|---|---|
| `.md` | Texto completo | `Archivo Markdown con N lineas` |
| `.py` | Extrae comentarios/docstrings + preview | `Archivo Python con N lineas` |
| `.txt` | Texto completo | `Archivo texto con N lineas` |
| `.csv` | Texto completo | `Archivo CSV con N filas` |
| `.json` | Texto completo | `Archivo JSON con N lineas` |
| `.yaml` / `.yml` | Texto completo | `Archivo YAML con N lineas` |

## Funciones principales

```python
get_file_summary(filepath: str) -> dict
```
Devuelve filename, extension, size, preview (primeros 1500 caracteres).

```python
extract_all_uploaded_content() -> str
```
Concatena el contenido de todos los archivos subidos, separado por `=== filename ===`.

## Ubicacion de archivos

Los archivos se guardan en `data/uploads/`. El directorio se crea automaticamente si no existe.
