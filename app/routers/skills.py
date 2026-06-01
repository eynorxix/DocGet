from fastapi import APIRouter, HTTPException
from app.models.schemas import SkillCreate, SkillUpdate, SkillResponse
from app.services import skill_loader

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("")
def list_skills():
    skills = skill_loader.list_skills()
    return skills


@router.get("/{skill_id}")
def get_skill(skill_id: str):
    skill = skill_loader.get_skill(skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill no encontrada")
    return skill


@router.post("")
def create_skill(data: SkillCreate):
    try:
        result = skill_loader.create_skill(
            name=data.name,
            description=data.description,
            content=data.content,
            skill_type=data.type,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{skill_id}")
def update_skill(skill_id: str, data: SkillUpdate):
    result = skill_loader.update_skill(
        skill_id=skill_id,
        name=data.name,
        description=data.description,
        content=data.content,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Skill no encontrada")
    return result


@router.delete("/{skill_id}")
def delete_skill(skill_id: str):
    ok = skill_loader.delete_skill(skill_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Skill no encontrada")
    return {"status": "deleted", "id": skill_id}
