import json
from pathlib import Path
from fastapi import APIRouter

router = APIRouter(prefix="/api/modelos", tags=["modelos"])

MODELOS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "modelos"


@router.get("")
def list_modelos():
    MODELOS_DIR.mkdir(parents=True, exist_ok=True)
    modelos = []
    for f in sorted(MODELOS_DIR.iterdir()):
        if f.suffix == ".json":
            data = json.loads(f.read_text(encoding="utf-8"))
            modelos.append({
                "id": data["id"],
                "name": data["name"],
                "label": data.get("label", ""),
                "tipo_universidad": data.get("tipo_universidad", ""),
            })
    return {"modelos": modelos}


@router.get("/{modelo_id}")
def get_modelo(modelo_id: str):
    MODELOS_DIR.mkdir(parents=True, exist_ok=True)
    f = MODELOS_DIR / f"{modelo_id}.json"
    if not f.exists():
        return {"error": "Modelo no encontrado"}
    return json.loads(f.read_text(encoding="utf-8"))


def get_modelo_by_code(code: str) -> dict | None:
    MODELOS_DIR.mkdir(parents=True, exist_ok=True)
    for f in MODELOS_DIR.iterdir():
        if f.suffix == ".json":
            data = json.loads(f.read_text(encoding="utf-8"))
            if data.get("codigo_activacion") and data["codigo_activacion"].lower() == code.lower().strip():
                return data
    return None
