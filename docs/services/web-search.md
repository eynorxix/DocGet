# Web Search Service

**Archivo**: `app/services/web_search.py`

## Proposito

Busca informacion actualizada en internet usando DuckDuckGo. No requiere API key, es completamente gratuito.

## Funciones

```python
search_web(query: str, max_results: int = 5) -> list[dict]
```
Busca en internet y devuelve resultados como lista de diccionarios con `title`, `href`, `body`.

```python
search_web_formatted(query: str, max_results: int = 5) -> str
```
Busca y devuelve resultados formateados como Markdown para incluir en prompts de IA o mostrar al usuario.

## Integracion

La busqueda web se usa en dos lugares:

1. **chat_service.py** — Herramienta `web_search()` que el agente IA puede invocar cuando necesita informacion actualizada
2. **gemini_service.py** — Al generar documentos, busca automaticamente informacion sobre el tema indicado y la incluye como contexto en el prompt de Gemini

## Estrategia de busqueda

Cuando una query en español no encuentra resultados, el servicio automaticamente:

1. **Simplifica** la query eliminando palabras vacias (articulos, preposiciones, etc.)
2. **Traduce** terminos técnicos españoles a ingles (ej: "sistema operativo" → "operating system", "distribuciones" → "distributions")
3. **Intenta la version en ingles** de la query simplificada
4. **Combina resultados** de todas las variantes, evitando URLs duplicadas

## Uso como fallback de Gemini

Cuando `gemini_service.py` no puede contactar a la API de Gemini (todas las keys en cooldown), automaticamente usa `web_search` para generar el contenido del documento a partir de resultados de internet, en lugar de devolver un mensaje de error. Esto asegura que el usuario siempre reciba un documento con informacion util, incluso sin IA.

## Dependencias

- `ddgs` (>=9.14.4) — Cliente DuckDuckGo Search
