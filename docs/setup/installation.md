# Instalacion

## Requisitos

- Python 3.11 o superior
- Poetry (gestor de paquetes)
- Git (opcional)

## Instalar Poetry

```bash
# Linux / macOS / WSL
curl -sSL https://install.python-poetry.org | python3 -

# Verificar
poetry --version
```

## Clonar o copiar el proyecto

```bash
cd /home/eynor/Documentos/Biblioteca/docgent
```

## Instalar dependencias

```bash
cd /home/eynor/Documentos/Biblioteca/docgent
poetry install --no-root
```

Esto instala:
- fastapi
- uvicorn
- python-docx
- jinja2
- pydantic
- python-multipart
- aiofiles
- google-generativeai
- python-dotenv

## Configurar Gemini API (opcional)

1. Obtener una API key en https://aistudio.google.com/apikey
2. Crear archivo `.env` en la raiz del proyecto:

```
GEMINI_API_KEY=tu_api_key_aqui
```

Sin API key, el sistema funciona con contenido de relleno (modo fallback).

## Ejecutar

```bash
poetry run python -m app.main
```

Abrir en el navegador: http://localhost:8000
