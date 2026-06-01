"""Fixtures compartidos para todas las pruebas."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Cliente HTTP de prueba para la API."""
    return TestClient(app)


@pytest.fixture
def sample_skill_data():
    """Datos de ejemplo para crear una skill."""
    return {
        "name": "Test Skill",
        "description": "Skill de prueba",
        "content": "# Test Skill\n\nContenido de prueba para verificar el sistema.",
        "type": "md",
    }
