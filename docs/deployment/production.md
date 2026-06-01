# Despliegue en produccion

## Opciones gratis (sin tarjeta de credito)

### Hugging Face Spaces (recomendado)

[Hugging Face Spaces](https://huggingface.co/spaces) corre Python en contenedores Docker. No pide tarjeta.

#### Como subirlo:

1. Ve a [huggingface.co/spaces](https://huggingface.co/spaces) → "Create new Space"
2. Configura:
   - **Space Name**: `docgent`
   - **License**: `MIT`
   - **Space SDK**: `Docker`
   - **Docker template**: `Python 3.12`
3. Clic en "Create Space"
4. Sube los archivos:
   - Opcion A: `git clone` el repo y haz `git push`
   - Opcion B: arrastra los archivos por la web (Upload files)
5. Ve a la pestana **Settings** → **Repository Secrets** y agrega:
   - `GEMINI_API_KEY` = tu API key de Gemini
6. El build empieza solo. Espera 2-3 min.
7. Listo. Tu URL sera `https://eynor-docgent.hf.space` (o similar)

**Tu laptop no necesita estar encendida.** Corre en los servidores de Hugging Face.

#### Capacidad (plan free):
| Recurso | Limite |
|---|---|
| CPU | 1 nucleo |
| RAM | 8 GB |
| Usuarios simultaneos | 10-15 normales, ~5 generando docs |
| Se duerme | No, pero si hay inactividad prolongada (~30-45 min) el contenedor se pausa |
| Despertar | ~30s al entrar de nuevo |

#### Nota:
El proyecto ya incluye `Dockerfile` y `README.md` configurados.

### Koyeb

[Koyeb](https://www.koyeb.com) corre contenedores Docker, sin tarjeta en el plan free.

1. Conecta tu repositorio de GitHub
2. Selecciona `docgent`
3. Koyeb detecta automaticamente el `Dockerfile`
4. Define `GEMINI_API_KEY` como variable de entorno
5. Despliega

### Render (requiere tarjeta)

Render ofrece hosting gratuito para servicios web Python.

1. Sube el proyecto a GitHub
2. Crea un Web Service en Render
3. Configura:

| Campo | Valor |
|---|---|
| Build Command | `poetry install --no-root` |
| Start Command | `poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Environment Variable | `GEMINI_API_KEY=tu_key` |

### Railway (requiere tarjeta)

1. Conecta el repositorio
2. Railway detecta automaticamente Poetry
3. Define el comando de inicio

## Limitaciones de Free Tiers

| Servicio | Sin tarjeta | Se duerme | Limite |
|---|---|---|---|
| Hugging Face Spaces | ✅ Si | ~30 min | 1 CPU, 8 GB RAM |
| Koyeb | ✅ Si | Si | 1 CPU, 512 MB RAM |
| Render | ❌ No | Si (15 min) | 512 MB RAM |
| Railway | ❌ No | No | $5 de credito gratis |

## Alternativas de pago

- Railway ($5+/mes)
- Fly.io ($3+/mes)
- DigitalOcean Apps ($5+/mes)
