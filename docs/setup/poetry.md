# Uso de Poetry

Este proyecto usa **Poetry** como gestor de paquetes y dependencias.

## Poetry en tu sistema

Poetry está instalado globalmente:

```
$ which poetry
/usr/bin/poetry

$ poetry --version
Poetry (version 2.4.1)
```

Si no lo tuvieras, se instala con:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## Comandos esenciales

### Instalar dependencias del proyecto

```bash
cd /home/eynor/Documentos/Biblioteca/docgent
poetry install --no-root
```

Esto crea el `.venv/` con todas las dependencias de `pyproject.toml`.

### Agregar una nueva dependencia

```bash
poetry add nombre_del_paquete
```

Ejemplo:
```bash
poetry add requests
```

### Ejecutar el servidor

```bash
poetry run python -m app.main
```

### Ejecutar cualquier comando dentro del venv

```bash
poetry run <comando>
```

### Entrar al entorno virtual

```bash
poetry shell
```

### Actualizar dependencias

```bash
poetry update
```

### Ver dependencias instaladas

```bash
poetry show
```

### Ruta del `.venv`

Poetry crea el entorno virtual dentro del proyecto en `.venv/`. Si necesitas el Python del venv directamente:

```bash
.venv/bin/python -c "..."
```

## Estructura de `pyproject.toml`

```toml
[project]
name = "docgent"
version = "0.1.0"
requires-python = "^3.11"
dependencies = [
    "fastapi (>=0.136.3,<0.137.0)",
    "uvicorn (>=0.48.0,<0.49.0)",
    "python-docx (>=1.2.0,<2.0.0)",
    "google-generativeai (>=0.8.6,<0.9.0)",
    ...
]

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

Nota: `package-mode = false` indica que el proyecto no es una librería instalable, sino una aplicación.
