import json
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from app.services import chat_service

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


class ChatResponse(BaseModel):
    response: str
    data: dict | None = None
    action: str | None = None


@router.post("/chat", response_model=ChatResponse)
def chat(data: ChatRequest, x_gemini_key: Optional[str] = Header(None), x_gemini_keys: Optional[str] = Header(None), x_caratula: Optional[str] = Header(None), x_modelo: Optional[str] = Header(None)): 
    try:
        keys = []
        if x_gemini_keys:
            try:
                keys = json.loads(x_gemini_keys)
            except json.JSONDecodeError:
                pass
        if not keys and x_gemini_key:
            keys = [x_gemini_key]
        caratula = None
        if x_caratula:
            try:
                caratula = json.loads(x_caratula)
            except json.JSONDecodeError:
                pass
        modelo = x_modelo or "docxix"
        result = chat_service.process_message(data.message, data.history, api_keys=keys, caratula=caratula, modelo=modelo)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
