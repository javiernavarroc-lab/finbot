from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def chat(texto):
    return client.post("/chat", json={"mensaje": texto})


def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json() == {"status": "ok"}


def test_pagina_html():
    assert "Finbot" in client.get("/").text


def test_cuota():
    r = chat("cuota crédito 10000000 12 36")
    assert r.status_code == 200
    assert r.json()["fuente"] == "reglas"
    assert "332,143" in r.json()["respuesta"]


def test_meta_de_ahorro():
    r = chat("ahorro 1200 12")
    assert r.json()["fuente"] == "reglas" and "100.00" in r.json()["respuesta"]


def test_glosario():
    r = chat("¿qué es la UF?")
    assert r.json()["fuente"] == "glosario" and "Unidad de Fomento" in r.json()["respuesta"]


def test_mensaje_vacio_rechazado():
    assert chat("").status_code == 422
    assert chat("   ").status_code == 422
    assert client.post("/chat", json={}).status_code == 422


def test_pregunta_abierta_sin_clave(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert "No entendí" in chat("hola").json()["respuesta"]
