"""Pruebas de caja negra para el módulo de chat (endpoints y flujo)."""

import pytest
from app.services import chat_service


class TestChatServiceWhiteBox:
    """Pruebas unitarias sobre chat_service."""

    def test_process_message_returns_dict(self):
        result = chat_service.process_message("Hola", [])
        assert "response" in result
        assert "data" in result
        assert "action" in result

    def test_process_message_no_tool(self):
        """Un mensaje simple no debería activar herramientas."""
        result = chat_service.process_message("Hola, ¿cómo estás?", [])
        assert result["action"] is None
        assert result["data"] is None

    def test_execute_tool_list_skills(self):
        msg, data = chat_service._execute_tool("list_skills", {})
        assert data is None or "skills" in data

    def test_execute_tool_unknown(self):
        msg, data = chat_service._execute_tool("no_existe", {})
        assert "No reconozco" in msg

    def test_execute_tool_request_skill_select(self):
        msg, data = chat_service._execute_tool("request_skill_select", {})
        assert data is not None
        assert data["action"] == "skill_select"

    def test_execute_tool_request_file_upload(self):
        msg, data = chat_service._execute_tool("request_file_upload", {})
        assert data is not None
        assert data["action"] == "upload"

    def test_execute_tool_web_search(self):
        msg, data = chat_service._execute_tool("web_search", {"query": "python programming"})
        assert data is not None
        assert "web_results" in data

    def test_execute_tool_web_search_no_query(self):
        msg, data = chat_service._execute_tool("web_search", {})
        assert "No especificaste" in msg


class TestChatAPIBlackBox:
    """Pruebas de integración contra el endpoint de chat."""

    def test_chat_endpoint_returns_200(self, client):
        resp = client.post(
            "/api/chat",
            json={"message": "Hola", "history": []},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "response" in data

    def test_chat_with_caratula_header(self, client):
        """Enviar datos de carátula como header."""
        resp = client.post(
            "/api/chat",
            json={"message": "genera un documento", "history": []},
            headers={"X-Caratula": '{"titulo":"Test","autor":"Yo","tutor":"El"}'},
        )
        assert resp.status_code == 200

    def test_chat_with_invalid_caratula(self, client):
        """Carátula inválida no debe romper el endpoint."""
        resp = client.post(
            "/api/chat",
            json={"message": "Hola", "history": []},
            headers={"X-Caratula": "no-es-json"},
        )
        assert resp.status_code == 200

    def test_chat_with_api_keys_header(self, client):
        resp = client.post(
            "/api/chat",
            json={"message": "Hola", "history": []},
            headers={"X-Gemini-Keys": '["fake-key"]'},
        )
        assert resp.status_code == 200
