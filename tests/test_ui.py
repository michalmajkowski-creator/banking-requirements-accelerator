from fastapi.testclient import TestClient

from bra.api import app


client = TestClient(app)


def test_form_is_served_at_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Analiza inicjatywy bankowej" in response.text
    assert "analysis-form" in response.text


def test_form_contract_runs_analysis_through_api():
    response = client.post(
        "/v1/runs",
        json={
            "pipeline": "mvp",
            "initiative": {
                "title": "Zmiana limitu",
                "problem": "Brak samoobsługi",
                "desired_outcome": "Bezpieczna samoobsługa",
                "sources": ["warsztat"],
                "stakeholders": ["Payments"],
                "constraints": ["audyt"],
            },
            "requirements": [],
        },
    )
    assert response.status_code == 200
    assert response.json()["pipeline"] == "mvp"
    assert response.json()["steps"]
