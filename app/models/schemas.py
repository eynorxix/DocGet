from pydantic import BaseModel
from typing import Optional


class SkillCreate(BaseModel):
    name: str
    description: str
    content: str
    type: str = "md"


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None


class SkillResponse(BaseModel):
    id: str
    name: str
    description: str
    type: str
    filename: str
    created_at: str


class GenerateRequest(BaseModel):
    skill_id: str
    title: str
    author: str = ""
    tutor: str = ""
    content_input: str = ""


class GenerateDirectRequest(BaseModel):
    title: str
    author: str = ""
    tutor: str = ""
    topic: str = ""


class UploadResponse(BaseModel):
    filename: str
    size: int
    content_preview: str
