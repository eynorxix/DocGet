"""Pruebas de caja negra y blanca para el módulo de skills (CRUD)."""

import pytest
from app.services import skill_loader


# ─── PRUEBAS DE CAJA BLANCA (unitarias, sobre skill_loader) ───

class TestSkillLoaderWhiteBox:
    """Pruebas unitarias directas sobre skill_loader (estructura interna)."""

    def test_list_skills_returns_list(self):
        skills = skill_loader.list_skills()
        assert isinstance(skills, list)

    def test_list_skills_excludes_py(self):
        """Los archivos .py NO deben aparecer en el listado."""
        skills = skill_loader.list_skills()
        ids = [s["id"] for s in skills]
        assert "base_documento" not in ids

    def test_get_skill_returns_none_for_missing(self):
        skill = skill_loader.get_skill("no_existe")
        assert skill is None

    def test_get_skill_still_finds_py(self):
        """get_skill() sí debe encontrar .py aunque no aparezcan en listado."""
        skill = skill_loader.get_skill("base_documento")
        assert skill is not None
        assert skill["type"] == "py"

    def test_create_and_delete_skill(self):
        name = "__test_temp_skill__"
        r = skill_loader.create_skill(name, "test", "contenido", "md")
        assert r["name"] == name
        assert r["type"] == "md"

        found = skill_loader.get_skill(r["id"])
        assert found is not None

        deleted = skill_loader.delete_skill(r["id"])
        assert deleted is True

        gone = skill_loader.get_skill(r["id"])
        assert gone is None


# ─── PRUEBAS DE CAJA NEGRA (integración, vía API REST) ───

class TestSkillsAPIBlackBox:
    """Pruebas de integración contra los endpoints REST de skills."""

    def test_list_skills_endpoint(self, client):
        resp = client.get("/api/skills")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_create_skill_endpoint(self, client, sample_skill_data):
        resp = client.post("/api/skills", json=sample_skill_data)
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == sample_skill_data["name"]

        # limpieza
        skill_loader.delete_skill(data["id"])

    def test_get_skill_by_id(self, client, sample_skill_data):
        r = client.post("/api/skills", json=sample_skill_data)
        sid = r.json()["id"]

        resp = client.get(f"/api/skills/{sid}")
        assert resp.status_code == 200
        assert resp.json()["name"] == sample_skill_data["name"]

        skill_loader.delete_skill(sid)

    def test_delete_skill_endpoint(self, client, sample_skill_data):
        r = client.post("/api/skills", json=sample_skill_data)
        sid = r.json()["id"]

        resp = client.delete(f"/api/skills/{sid}")
        assert resp.status_code == 200

        resp2 = client.get(f"/api/skills/{sid}")
        assert resp2.status_code == 404

    def test_404_for_missing_skill(self, client):
        resp = client.get("/api/skills/no_existe")
        assert resp.status_code == 404
