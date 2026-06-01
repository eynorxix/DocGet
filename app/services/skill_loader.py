import os
import shutil
from pathlib import Path
from datetime import datetime


SKILLS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "skills"


def ensure_skills_dir():
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)


def list_skills() -> list[dict]:
    ensure_skills_dir()
    skills = []
    for f in sorted(SKILLS_DIR.iterdir()):
        if f.is_file() and f.suffix in (".md", ".txt", ".json"):
            content = f.read_text(encoding="utf-8", errors="replace")
            first_line = content.strip().split("\n")[0] if content else ""
            name = first_line.replace("#", "").replace('"""', "").strip()
            if not name:
                name = f.stem.replace("_", " ").replace("-", " ").title()
            skills.append({
                "id": f.stem,
                "name": name,
                "description": _extract_description(content),
                "type": f.suffix[1:],
                "filename": f.name,
                "content": content,
                "created_at": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
            })
    return skills


def get_skill(skill_id: str) -> dict | None:
    ensure_skills_dir()
    for ext in (".md", ".py", ".txt", ".json"):
        f = SKILLS_DIR / f"{skill_id}{ext}"
        if f.exists():
            content = f.read_text(encoding="utf-8", errors="replace")
            first_line = content.strip().split("\n")[0] if content else ""
            name = first_line.replace("#", "").strip()
            if not name:
                name = skill_id.replace("_", " ").replace("-", " ").title()
            return {
                "id": skill_id,
                "name": name,
                "type": ext[1:],
                "filename": f.name,
                "content": content,
            }
    return None


def create_skill(name: str, description: str, content: str, skill_type: str = "md") -> dict:
    ensure_skills_dir()
    file_stem = name.lower().replace(" ", "_").replace("-", "_")
    filename = f"{file_stem}.{skill_type}"
    filepath = SKILLS_DIR / filename

    if skill_type == "md":
        full_content = f"# {name}\n\n## Descripción\n{description}\n\n{content}"
    elif skill_type == "py":
        full_content = f'"""\n{name}\n\n{description}\n"""\n\n\n{content}'
    else:
        full_content = content

    filepath.write_text(full_content, encoding="utf-8")

    return {
        "id": file_stem,
        "name": name,
        "type": skill_type,
        "filename": filename,
        "content": full_content,
    }


def update_skill(skill_id: str, name: str | None, description: str | None, content: str | None) -> dict | None:
    skill = get_skill(skill_id)
    if not skill:
        return None

    filepath = SKILLS_DIR / skill["filename"]
    existing = filepath.read_text(encoding="utf-8")

    if name and content is None and description is None:
        pass

    if content is not None:
        filepath.write_text(content, encoding="utf-8")
    elif name or description:
        lines = existing.split("\n")
        if skill["type"] == "md":
            if name:
                lines[0] = f"# {name}"
            if description:
                for i, line in enumerate(lines):
                    if line.startswith("## Descripción"):
                        if i + 1 < len(lines):
                            lines[i + 1] = description
                        break
            filepath.write_text("\n".join(lines), encoding="utf-8")

    return get_skill(skill_id)


def delete_skill(skill_id: str) -> bool:
    skill = get_skill(skill_id)
    if not skill:
        return False
    filepath = SKILLS_DIR / skill["filename"]
    filepath.unlink()
    return True


def get_skill_content(skill_id: str) -> str | None:
    skill = get_skill(skill_id)
    return skill["content"] if skill else None


def _extract_description(content: str, max_len: int = 120) -> str:
    lines = content.strip().split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip().lower()
        if stripped.startswith("## descripción") or stripped.startswith("## descripcion"):
            if i + 1 < len(lines):
                desc = lines[i + 1].strip()
                return desc[:max_len] + "..." if len(desc) > max_len else desc
        if stripped.startswith("## descripcion"):
            if i + 1 < len(lines):
                desc = lines[i + 1].strip()
                return desc[:max_len] + "..." if len(desc) > max_len else desc
    first_line = lines[0].strip() if lines else ""
    desc = first_line.replace("#", "").replace('"""', "").strip()
    return desc[:max_len] + "..." if len(desc) > max_len else desc
