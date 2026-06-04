import json
import re
import os
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from app.services import skill_loader, file_reader, document_generator, web_search

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEFAULT_SKILL_ID = "indice"

TOOL_DESC = """
## Herramientas disponibles:

### `list_skills()`
Lista todas las skills disponibles.

### `get_skill(skill_id)`
Muestra el contenido completo de una skill.

### `create_skill(name, description, content, type="md")`
Crea una skill nueva. Si el usuario no da el contenido completo, generalo tú.

### `update_skill(skill_id, name, description, content)`
Actualiza name, description o content de una skill existente.

### `delete_skill(skill_id)`
Elimina una skill.

    ### `generate_document(skill_id, title, author, tutor, content_input)`
    Genera un documento .docx. 
    - skill_id: requerido (default "indice")
    - title: auto-generado si no se da (max 20 palabras)
    - author: "Sin asignar" si no se da
    - tutor: "Sin asignar" si no se da
    - content_input: "" si no se da

### `list_uploads()`
Lista archivos subidos por el usuario.

### `list_documents()`
Lista documentos .docx generados.

### `request_file_upload()`
Pide al usuario que suba un archivo (abre el selector de archivos).

### `request_skill_select()`
Muestra al usuario un selector visual de skills para que elija cuál usar. Usa esto cuando el usuario quiera generar un documento y necesites que seleccione una skill.

### `web_search(query)`
Busca en internet información actualizada sobre un tema. Úsalo cuando el usuario pida información reciente, datos específicos, o cuando necesites contexto actualizado para generar un documento de calidad. El query debe ser en español o inglés según corresponda.
"""

SYSTEM_PROMPT = f"""Eres un asistente conversacional integrado en DocXIX, un generador de documentos .docx académicos.

{TOOL_DESC}

INSTRUCCIONES:
1. Responde en español, en el mismo tono que el usuario.
2. Para SOLICITAR INFORMACIÓN al usuario, responde naturalmente.
3. Para EJECUTAR una acción, usa este formato exacto AL FINAL de tu respuesta:

---TOOL---
{{"name": "nombre_herramienta", "params": {{...}}}}

4. Cuando el usuario pida generar un documento, EJECUTA generate_document INMEDIATAMENTE sin preguntar nada.
   - Si no dio skill_id, usa "indice".
   - Si no dio title, genera UN TÍTULO AUTOMÁTICAMENTE (max 20 palabras, basado en el tema/archivos).
   - Si no dio author, usa "Sin asignar".
   - Si no dio tutor, usa "Sin asignar".
   - Si no dio content_input, usa "".
   - NO preguntes "¿está todo listo?". NO pidas confirmación. NO pidas datos faltantes con Y/N.
5. El usuario NUNCA debe confirmar ni responder Y/N. Solo genera.
6. Para crear skills, si el usuario da instrucciones parciales, completa el contenido tú mismo.
7. IMPORTANTE: No inventes IDs de skills. Siempre lista primero o pide el nombre.
8. Cuando crees contenido para un documento, sé detallado y profesional. Usa `web_search()` para obtener información actualizada de internet cuando sea relevante.
9. Cuando recibas "SISTEMA: El usuario seleccionó la skill: NOMBRE", analiza si el NOMBRE de la skill coincide con el tema que el usuario quiere documentar.
   - Si la skill es de un tema diferente (ej: skill "microcontrolador" para un documento sobre "Linux"), ADVIERTE al usuario: "La skill que seleccionaste es sobre [tema skill], pero tu documento es sobre [tema usuario]. No es la más adecuada. ¿Quieres seleccionar otra skill o igual la usamos como plantilla genérica?"
   - Si el usuario insiste o no hay otra skill, usa la que eligió.
10. Si recibes "SISTEMA: El usuario subió el archivo...", confirma que el archivo está disponible como contexto.

SKILL POR DEFECTO:
Existe una skill llamada "Índice General" (ID: indice) con una estructura genérica de índice académico. Úsala como predeterminada cuando el usuario quiera generar un documento pero no haya seleccionado una skill específica.

DATOS DE CARÁTULA:
11. Si ves "SISTEMA: Datos de carátula disponibles:", úsalos directamente.
12. Si no ves datos de carátula, usa "Sin asignar" para autor y tutor, y genera un título automático.
"""

_key_cooldowns: dict[str, float] = {}

def _parse_retry_delay(body: str) -> float:
    m = re.search(r'"retryDelay"\s*:\s*"(\d+(?:\.\d+)?)s"', body)
    return float(m.group(1)) if m else 30.0

def _get_available_keys(keys: list[str]) -> list[str]:
    now = time.time()
    return [k for k in keys if k and (k not in _key_cooldowns or now >= _key_cooldowns[k])]

def _call_gemini(messages: list, api_keys: list[str] | None = None) -> str:
    keys = api_keys or ([GEMINI_API_KEY] if GEMINI_API_KEY else [])
    if not keys:
        return "No tengo conexión con la IA. No se encontró una API key de Gemini."
    import httpx
    payload = {"contents": messages}
    last_error = ""
    attempted = set()
    for _ in range(len(keys)):
        available = _get_available_keys(keys)
        if not available:
            return "Todas las API keys en cooldown. Espera unos segundos y vuelve a intentar."
        key = available[0]
        attempted.add(key)
        try:
            resp = httpx.post(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
                headers={"Content-Type": "application/json", "X-goog-api-key": key},
                json=payload,
                timeout=30,
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
            return f"Error de Gemini: {body[:300]}"
        except Exception as e:
            last_error = str(e)
            continue
    return f"Todas las API keys agotadas. {last_error}"


def _execute_tool(name: str, params: dict, api_keys: list[str] | None = None, modelo: str = "docxix") -> tuple[str, dict | None]:
    try:
        if name == "list_skills":
            skills = skill_loader.list_skills()
            if not skills:
                return "No hay skills todavía.", None
            return f"Skills disponibles ({len(skills)}):", {"skills": skills}

        elif name == "get_skill":
            skill = skill_loader.get_skill(params["skill_id"])
            if not skill:
                return f"No encontré la skill '{params['skill_id']}'.", None
            return f"**{skill['name']}**\n\n{skill['content']}", {"skill": skill}

        elif name == "create_skill":
            r = skill_loader.create_skill(
                name=params["name"],
                description=params.get("description", ""),
                content=params["content"],
                skill_type=params.get("type", "md"),
            )
            _cleanup_uploads()
            return f"Skill **{r['name']}** creada.", {"skill": r}

        elif name == "update_skill":
            r = skill_loader.update_skill(
                skill_id=params["skill_id"],
                name=params.get("name"),
                description=params.get("description"),
                content=params.get("content"),
            )
            if not r:
                return f"Skill '{params['skill_id']}' no encontrada.", None
            _cleanup_uploads()
            return f"Skill **{r['name']}** actualizada.", {"skill": r}

        elif name == "delete_skill":
            ok = skill_loader.delete_skill(params["skill_id"])
            if not ok:
                return f"Skill '{params['skill_id']}' no encontrada.", None
            return f"Skill eliminada.", None

        elif name == "generate_document":
            skill = skill_loader.get_skill(params["skill_id"])
            if not skill:
                skill = skill_loader.get_skill(DEFAULT_SKILL_ID)
                if not skill:
                    return f"Skill '{params['skill_id']}' no encontrada.", None
            uploaded = file_reader.extract_all_uploaded_content()
            from app.services import gemini_service
            content = gemini_service.generate_document_content(
                skill_content=skill["content"],
                uploaded_content=uploaded,
                user_input=params.get("content_input") or "",
                api_keys=api_keys,
            )
            from app.routers import modelos as modelos_router
            modelo_data = modelos_router.get_modelo_by_code(modelo) or modelos_router.get_modelo(modelo)
            if not modelo_data or isinstance(modelo_data, dict) and modelo_data.get("error"):
                modelo_data = {"logo_path": None}
            m_logo = modelo_data.get("logo_path")
            logo = None
            if m_logo:
                PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
                if m_logo.startswith("/assets/"):
                    lp = PROJECT_ROOT / m_logo.lstrip("/")
                elif m_logo.startswith("/"):
                    lp = Path(m_logo)
                else:
                    lp = PROJECT_ROOT / m_logo.lstrip("/")
                if lp.exists():
                    logo = str(lp)
            path = document_generator.generate_docx(
                title=params.get("title") or "",
                author=params.get("author") or "",
                tutor=params.get("tutor") or "",
                skill_type=skill["type"],
                document_content=content,
                logo_path=logo,
                modelo=modelo_data if isinstance(modelo_data, dict) and not modelo_data.get("error") else None,
            )
            _cleanup_uploads()
            return f"Documento **{path.name}** generado.", {"download_url": f"/api/documents/download/{path.name}", "filename": path.name}

        elif name == "list_uploads":
            file_reader.ensure_upload_dir()
            upload_dir = Path(file_reader.UPLOAD_DIR)
            files = []
            for f in sorted(upload_dir.iterdir()):
                if f.is_file():
                    info = file_reader.get_file_summary(str(f))
                    files.append(info)
            if not files:
                return "No hay archivos subidos.", None
            return f"Archivos subidos ({len(files)}):", {"files": files}

        elif name == "list_documents":
            output_dir = Path(document_generator.OUTPUT_DIR)
            output_dir.mkdir(parents=True, exist_ok=True)
            files = []
            for f in sorted(output_dir.iterdir()):
                if f.suffix == ".docx":
                    files.append({"filename": f.name, "size_kb": round(f.stat().st_size / 1024, 2)})
            if not files:
                return "No hay documentos generados.", None
            return f"Documentos generados ({len(files)}):", {"documents": files}

        elif name == "request_file_upload":
            return "Por favor, usa el botón de subir archivo en la barra lateral.", {"action": "upload"}

        elif name == "request_skill_select":
            skills = skill_loader.list_skills()
            if not skills:
                return "No hay skills disponibles. Crea una primero.", None
            return "Selecciona una skill de la lista:", {"action": "skill_select", "skills": skills}

        elif name == "web_search":
            query = params.get("query", "")
            if not query:
                return "No especificaste qué buscar.", None
            result = web_search.search_web_formatted(query, max_results=7)
            return f"Resultados de búsqueda para \"{query}\":\n\n{result}", {"web_results": result}

        return f"No reconozco la herramienta '{name}'.", None
    except Exception as e:
        return f"Error: {str(e)}", None


def _cleanup_uploads():
    upload_dir = Path(file_reader.UPLOAD_DIR)
    if upload_dir.exists():
        for f in upload_dir.iterdir():
            if f.is_file():
                f.unlink()


def process_message(message: str, history: list[dict], api_keys: list[str] | None = None, caratula: dict | None = None, modelo: str = "docxix") -> dict:
    messages = [{"role": "user", "parts": [{"text": SYSTEM_PROMPT}]}]

    if caratula:
        parts = []
        if caratula.get("titulo"):
            parts.append(f"título: {caratula['titulo']}")
        if caratula.get("autor"):
            parts.append(f"autor: {caratula['autor']}")
        if caratula.get("tutor"):
            parts.append(f"tutor: {caratula['tutor']}")
        if parts:
            msg = f"SISTEMA: Datos de carátula disponibles:\n" + "\n".join(parts)
            messages.append({"role": "user", "parts": [{"text": msg}]})

    for h in history[-10:]:
        role = "user" if h.get("role") == "user" else "model"
        messages.append({"role": role, "parts": [{"text": h.get("content", "")}]})
    messages.append({"role": "user", "parts": [{"text": message}]})

    resp = _call_gemini(messages, api_keys=api_keys)

    tool_pattern = r'---TOOL---\s*\n\s*({.*})'
    match = re.search(tool_pattern, resp, re.DOTALL)

    if match:
        try:
            spec = json.loads(match.group(1))
            tool_name = spec.get("name")
            tool_params = spec.get("params", {})
            text_before = resp[:match.start()].strip()
            result_msg, data = _execute_tool(tool_name, tool_params, api_keys=api_keys, modelo=modelo)
            full_response = text_before + "\n\n" + result_msg if text_before else result_msg
            return {"response": full_response, "data": data, "action": tool_name}
        except (json.JSONDecodeError, KeyError) as e:
            return {"response": resp, "data": None, "action": None}

    return {"response": resp, "data": None, "action": None}
