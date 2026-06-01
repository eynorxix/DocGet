import os
import re
import time
from dotenv import load_dotenv

load_dotenv()

from app.services import web_search

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


_key_cooldowns: dict[str, float] = {}

def _parse_retry_delay(body: str) -> float:
    m = re.search(r'"retryDelay"\s*:\s*"(\d+(?:\.\d+)?)s"', body)
    return float(m.group(1)) if m else 30.0

def _get_available_keys(keys: list[str]) -> list[str]:
    now = time.time()
    return [k for k in keys if k and (k not in _key_cooldowns or now >= _key_cooldowns[k])]

def generate_document_content(skill_content: str, uploaded_content: str, user_input: str, api_keys: list[str] | None = None) -> str:
    keys = api_keys or ([GEMINI_API_KEY] if GEMINI_API_KEY else [])
    if not keys:
        return _fallback_content(user_input)

    import httpx

    web_context = ""
    if user_input.strip():
        try:
            results = web_search.search_web(user_input, max_results=5)
            if results:
                lines = []
                for r in results:
                    lines.append(f"- {r['title']}: {r['body'][:500]}")
                web_context = "\n".join(lines)
        except Exception:
            pass

    prompt = f"""Eres un asistente experto en generar contenido académico para documentos .docx.

## SKILL (plantilla/estructura del documento):
```markdown
{skill_content[:4000]}
```

## INFORMACIÓN EXTRAÍDA DE ARCHIVOS SUBIDOS:
```
{uploaded_content[:6000] if uploaded_content else "No hay archivos subidos."}
```

## INFORMACIÓN DE INTERNET (búsqueda automática según el tema):
{web_context[:4000] if web_context else "No se encontró información relevante en internet."}

## INSTRUCCIÓN DEL USUARIO:
{user_input}

Genera el contenido completo del documento siguiendo ESTRICTAMENTE la estructura definida en la SKILL.
Usa la información de internet y archivos subidos como fuente de datos para crear un documento más rico y actualizado.
Usa formato Markdown limpio. Incluye títulos, subtítulos, párrafos y listas donde corresponda.
No agregues notas ni explicaciones adicionales fuera del contenido solicitado."""

    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    last_error = ""
    for _ in range(len(keys)):
        available = _get_available_keys(keys)
        if not available:
            return _fallback_web_content(user_input)
        key = available[0]
        try:
            resp = httpx.post(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
                headers={"Content-Type": "application/json", "X-goog-api-key": key},
                json=payload,
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except httpx.HTTPStatusError as e:
            body = e.response.text
            body_lower = body.lower()
            if "quota" in body_lower or "rate" in body_lower:
                delay = _parse_retry_delay(body)
                _key_cooldowns[key] = time.time() + delay
                last_error = f"Cuota excedida (cooldown {delay:.0f}s)."
                continue
            return _fallback_web_content(user_input)
        except Exception as e:
            last_error = str(e)
            continue
    return _fallback_web_content(user_input)


def _fallback_web_content(user_input: str) -> str:
    """Genera contenido usando busqueda web cuando Gemini no esta disponible."""
    import datetime
    today = datetime.date.today().isoformat()
    results = web_search.search_web(user_input, max_results=6)
    if results:
        lines = [f"# {user_input}", "", f"## Fecha", today, "", "## Informacion recopilada de internet", ""]
        for i, r in enumerate(results, 1):
            lines.append(f"### {i}. {r['title']}")
            lines.append("")
            lines.append(r['body'])
            lines.append("")
        return "\n".join(lines)
    return f"""# {user_input}

## Fecha
{today}

## Contenido
Documento generado sobre: {user_input}
"""
