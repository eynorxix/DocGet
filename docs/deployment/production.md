# Despliegue en produccion

## Opciones gratis

### Render (recomendado)

Render ofrece hosting gratuito para servicios web Python.

1. Sube el proyecto a GitHub
2. Crea un Web Service en Render
3. Configura:

| Campo | Valor |
|---|---|
| Build Command | `poetry install --no-root` |
| Start Command | `poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Environment Variable | `GEMINI_API_KEY=tu_key` |

### Hugging Face Spaces

1. Crea un Space con Docker o Gradio
2. Agrega el `Dockerfile`:

```dockerfile
FROM python:3.12-slim
RUN pip install poetry
WORKDIR /app
COPY . .
RUN poetry install --no-root
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### Railway

1. Conecta el repositorio
2. Railway detecta automaticamente Poetry
3. Define el comando de inicio

## Limitaciones de Free Tiers

| Servicio | Se duerme | Limite |
|---|---|---|
| Render | Si (15 min inactividad) | 512 MB RAM |
| Hugging Face | No | 1 CPU, 8 GB RAM |
| Railway | No | $5 de credito gratis |

## Alternativas de pago

- Railway ($5+/mes)
- Fly.io ($3+/mes)
- DigitalOcean Apps ($5+/mes)
