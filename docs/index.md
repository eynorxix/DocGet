# DocGent

Generador de documentos `.docx` con Skills, IA (Gemini) y busqueda web (DuckDuckGo).

## Que es

DocGent es un servicio web que permite:

- Subir archivos de distintos tipos (`.md`, `.py`, `.txt`, `.csv`, `.json`, `.yaml`)
- Chatear con un **agente IA** que gestiona skills, archivos y generacion de documentos
- Crear y gestionar **Skills** (plantillas de estructura documental en Markdown o Python)
- Generar documentos `.docx` combinando contenido de archivos subidos + estructura de Skill + IA + **busqueda web**
- **Busqueda web automatica** via DuckDuckGo (sin API key) para informacion actualizada
- Generacion directa de documentos con **boton "Generar"** que busca en internet y produce el `.docx` sin preguntas
- **Documento demo** que muestra todas las capacidades del sistema (tablas, indices, formato APA)
- Vista previa de documentos generados
- Rotacion automatica de multiples API keys de Gemini

## Estructura rapida

```
docgent/
  app/              Codigo fuente del servidor FastAPI
    main.py         Punto de entrada
    routers/        Endpoints de la API REST
    services/       Logica interna (chat, IA, busqueda web, generacion de docs)
    static/         CSS y JS separados (modular)
    templates/      Jinja2 templates con partials
  data/
    skills/         Skills instaladas (archivos .md, .py, .txt)
    uploads/        Archivos subidos por el usuario
    output/         Documentos .docx generados
  assets/           Recursos estaticos (QR de donaciones, etc.)
  tests/            Suite de pruebas pytest (36 tests)
  docs/             Esta documentacion
```

## Tecnologias

| Componente | Tecnologia |
|---|---|
| Backend | Python + FastAPI |
| Frontend | HTML (Jinja2 partials) + Vanilla JS + CSS |
| Documentos | python-docx (con formato APA 7, tablas, `**bold**` y `*italic*` inline) |
| IA | Google Gemini API (rotacion de hasta 4 keys, cooldown por cuota) |
| Busqueda web | DuckDuckGo (ddgs v9, sin API key, con traduccion español->ingles) |
| Paqueteria | Poetry |
| Tests | pytest (34 + 2 de red) |
| Servidor | Uvicorn |

## Como empezar

```bash
cd docgent
poetry run python -m app.main
# Abrir http://localhost:8000
```
