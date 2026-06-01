import os
from pathlib import Path


UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "uploads"


def ensure_upload_dir():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def read_text_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def read_python_file(filepath: str) -> str:
    content = read_text_file(filepath)
    lines = content.splitlines()
    docs = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
            docs.append(line)
    if docs:
        return "\n".join(docs[:50])
    return content[:2000]


def read_markdown_file(filepath: str) -> str:
    return read_text_file(filepath)


def get_file_summary(filepath: str) -> dict:
    ext = Path(filepath).suffix.lower()
    size = os.path.getsize(filepath)
    filename = Path(filepath).name

    if ext == ".py":
        content = read_python_file(filepath)
        summary = f"Archivo Python con {len(content.splitlines())} líneas"
    elif ext == ".md":
        content = read_markdown_file(filepath)
        summary = f"Archivo Markdown con {len(content.splitlines())} líneas"
    elif ext == ".txt":
        content = read_text_file(filepath)
        summary = f"Archivo texto con {len(content.splitlines())} líneas"
    elif ext == ".csv":
        content = read_text_file(filepath)
        summary = f"Archivo CSV con {len(content.splitlines())} filas"
    elif ext == ".json":
        content = read_text_file(filepath)
        summary = f"Archivo JSON con {len(content.splitlines())} líneas"
    elif ext == ".yaml" or ext == ".yml":
        content = read_text_file(filepath)
        summary = f"Archivo YAML con {len(content.splitlines())} líneas"
    else:
        content = read_text_file(filepath)
        summary = f"Archivo {ext} con {len(content.splitlines())} líneas"

    preview = content[:1500] if len(content) > 1500 else content

    return {
        "filename": filename,
        "extension": ext,
        "size": size,
        "size_kb": round(size / 1024, 2),
        "summary": summary,
        "preview": preview,
    }


def extract_all_uploaded_content() -> str:
    ensure_upload_dir()
    files = sorted(UPLOAD_DIR.iterdir())
    if not files:
        return ""

    parts = []
    for f in files:
        if f.is_file():
            info = get_file_summary(str(f))
            parts.append(f"=== {info['filename']} ===\n{info['preview']}\n")

    return "\n\n".join(parts)
