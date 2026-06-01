import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "data" / "skills"))

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn

from app.routers import skills, documents, chat

ASSETS_DIR = ROOT / "assets"
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

app = FastAPI(
    title="DocGent",
    description="Generador de documentos .docx con Skills e IA",
    version="1.0.0",
)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

app.mount("/static", StaticFiles(directory=str(ROOT / "app" / "static")), name="static")

app.include_router(skills.router)
app.include_router(documents.router)
app.include_router(chat.router)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})


@app.get("/health")
def health():
    return {"status": "ok", "project": "DocGent"}


def main():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
