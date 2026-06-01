# Ejecucion local

## Desarrollo

```bash
cd /home/eynor/Documentos/Biblioteca/docgent
poetry run python -m app.main
```

Esto inicia el servidor en `http://localhost:8000` con recarga automatica al editar codigo.

## Produccion local

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

Sin `--reload` para mejor rendimiento y estabilidad.

## Con systemd (Linux)

Crear `/etc/systemd/system/docgent.service`:

```ini
[Unit]
Description=DocGent
After=network.target

[Service]
Type=simple
User=eynor
WorkingDirectory=/home/eynor/Documentos/Biblioteca/docgent
ExecStart=/home/eynor/.local/bin/poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now docgent
```
