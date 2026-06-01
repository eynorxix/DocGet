# Gemini Service

**Archivo**: `app/services/gemini_service.py`

## Proposito

Integracion con Google Gemini API para generar contenido de documentos usando IA.

## Funcionamiento

```python
generate_document_content(skill_content, uploaded_content, user_input) -> str
```

Construye un prompt con:
1. **Skill**: La estructura/plantilla del documento (primeros 4000 caracteres)
2. **Archivos subidos**: Contenido extraido de los archivos (primeros 6000 caracteres)
3. **Instrucciones del usuario**: Lo que el usuario pide

Envía el prompt a Gemini y devuelve el contenido generado en Markdown.

## Modelo usado

`gemini-2.0-flash` - rapido y gratuito dentro de los limites del tier free.

## Fallback (sin API key)

Si `GEMINI_API_KEY` no esta configurada, `generate_document_content()` devuelve contenido basico con la fecha y las instrucciones del usuario. Esto permite probar el sistema sin depender de APIs externas.

## Configuracion

```bash
# .env
GEMINI_API_KEY=tu_api_key
```

Obtener API key en: https://aistudio.google.com/apikey

Tambien se pueden pasar keys por el header `X-Gemini-Keys` (JSON array) desde el frontend, lo que permite hasta **4 keys simultaneas**.

## Multi-key y rotacion

Si se configuran multiples keys (via header `X-Gemini-Keys`), el sistema:

1. Prueba la primera key disponible
2. Si recibe `429` (quota exceeded), pone esa key en cooldown
3. Prueba la siguiente key
4. Si todas fallan, usa fallback local

**Importante**: Las keys del mismo proyecto Google Cloud comparten cuota. Para que la rotacion sea efectiva, se necesitan keys de al menos 2 cuentas distintas.

## Busqueda web automatica

Al generar un documento, el servicio busca automaticamente en internet informacion relevante sobre el tema indicado por el usuario (usando DuckDuckGo). Los resultados se incluyen en el prompt de Gemini como contexto adicional, lo que permite generar documentos mas ricos y actualizados.

La busqueda se activa solo si `user_input` no esta vacio.

## Modo sin API key

Si no hay keys configuradas, `generate_document_content()` devuelve contenido placeholder. Permite probar la estructura sin depender de APIs externas.

## Límites del tier gratis

- 60 requests por minuto
- 1500 requests por dia
- Modelo Gemini 2.0 Flash
