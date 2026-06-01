# Ejemplos de uso con curl

## Listar skills

```bash
curl http://localhost:8000/api/skills
```

## Crear skill

```bash
curl -X POST http://localhost:8000/api/skills \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Documento Tecnico IoT",
    "description": "Estructura para documentos de sistemas embebidos",
    "type": "md",
    "content": "# {titulo}\n\n## Planteamiento\n\n## Solucion\n\n## Conclusiones"
  }'
```

## Subir archivo

```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -F "file=@/ruta/al/archivo.md"
```

## Generar documento

```bash
curl -X POST http://localhost:8000/api/documents/generate \
  -H "Content-Type: application/json" \
  -d '{
    "skill_id": "EstructuraIntegrador",
    "title": "Sistema IoT para Monitoreo de Temperatura",
    "author": "Juan Perez",
    "tutor": "Ing. Maria Lopez",
    "content_input": "Documento sobre un sistema con ESP32 y sensor DHT22"
  }'
```

## Descargar documento generado

```bash
curl -O -J http://localhost:8000/api/documents/download/Titulo_del_Proyecto.docx
```

## Ver estado del servidor

```bash
curl http://localhost:8000/health
```

## Integracion con otros agentes

Cualquier agente de IA o script puede llamar a estos endpoints HTTP. Ejemplo con Python:

```python
import requests

API = "http://localhost:8000"

# 1. Subir archivos de contexto
with open("datos.md", "rb") as f:
    requests.post(f"{API}/api/documents/upload", files={"file": f})

# 2. Generar documento
resp = requests.post(f"{API}/api/documents/generate", json={
    "skill_id": "EstructuraIntegrador",
    "title": "Mi Documento",
    "author": "Agente IA",
    "tutor": "Sistema",
    "content_input": "Genera el documento completo"
})

# 3. Descargar resultado
data = resp.json()
doc = requests.get(f"{API}{data['download_url']}")
with open(data["filename"], "wb") as f:
    f.write(doc.content)
```
