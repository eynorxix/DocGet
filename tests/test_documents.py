"""Pruebas de caja negra y blanca para el módulo de documentos."""

import os
from pathlib import Path
import pytest
from app.services import document_generator


OUTPUT_DIR = document_generator.OUTPUT_DIR
SKILLS_DIR = Path(__file__).resolve().parent.parent / "data" / "skills"


# ─── PRUEBAS DE CAJA BLANCA (generación de .docx) ───

class TestDocumentGeneratorWhiteBox:
    """Pruebas sobre la función generate_docx directamente."""

    def test_generate_docx_creates_file(self):
        path = document_generator.generate_docx(
            title="Test Document",
            author="Test Author",
            tutor="Test Tutor",
            skill_type="md",
            document_content="# Prueba\n\nEsto es una prueba.",
        )
        assert path.exists()
        assert path.suffix == ".docx"
        os.unlink(path)

    def test_generate_docx_with_logo_fallback(self):
        """Debe funcionar aunque el logo no exista."""
        path = document_generator.generate_docx(
            title="Sin Logo",
            author="Autor",
            tutor="Tutor",
            skill_type="md",
            document_content="Contenido",
            logo_path="/ruta/inexistente/logo.png",
        )
        assert path.exists()
        os.unlink(path)

    def test_generate_docx_content_with_tables(self):
        """Debe manejar tablas markdown en el contenido."""
        content = (
            "# Documento con tabla\n\n"
            "| Header1 | Header2 |\n"
            "|--------|--------|\n"
            "| Celda1 | Celda2 |\n"
        )
        path = document_generator.generate_docx(
            title="Tablas",
            author="Autor",
            tutor="Tutor",
            skill_type="md",
            document_content=content,
        )
        assert path.exists()
        os.unlink(path)

    def test_generate_docx_empty_content(self):
        """Debe manejar contenido vacío."""
        path = document_generator.generate_docx(
            title="Vacio",
            author="Autor",
            tutor="Tutor",
            skill_type="md",
            document_content="",
        )
        assert path.exists()
        os.unlink(path)


# ─── PRUEBAS DE CAJA NEGRA (vía API REST) ───

class TestDocumentsAPIBlackBox:
    """Pruebas de integración contra los endpoints de documentos."""

    def test_list_documents_endpoint(self, client):
        resp = client.get("/api/documents/list")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_download_nonexistent_returns_404(self, client):
        resp = client.get("/api/documents/download/no_existe.docx")
        assert resp.status_code == 404

    def test_preview_nonexistent_returns_404(self, client):
        resp = client.get("/api/documents/preview/no_existe.docx")
        assert resp.status_code == 404

    def test_upload_and_list_files(self, client):
        """Subir un archivo de prueba y verificar que aparece en uploads."""
        resp = client.post(
            "/api/documents/upload",
            files={"file": ("test.txt", b"contenido de prueba", "text/plain")},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["filename"] == "test.txt"

        # verificar que aparece en el listado
        list_resp = client.get("/api/documents/uploads")
        assert list_resp.status_code == 200
        files = list_resp.json()
        filenames = [f["filename"] for f in files]
        assert "test.txt" in filenames

        # limpiar
        client.delete("/api/documents/uploads/test.txt")

    def test_upload_and_delete(self, client):
        resp = client.post(
            "/api/documents/upload",
            files={"file": ("temp.txt", b"datos", "text/plain")},
        )
        assert resp.status_code == 200

        delete_resp = client.delete("/api/documents/uploads/temp.txt")
        assert delete_resp.status_code == 200
