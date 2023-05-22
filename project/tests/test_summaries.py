import json

import pytest


def test_create_summary(test_app_with_db):
    payload = {"url": "https://foo.bar"}
    response = test_app_with_db.post("/summaries/", json=payload)

    assert response.status_code == 201
    assert response.json()["url"] == payload["url"]


def test_create_summaries_invalid_json(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={})

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }


def test_read_summary(test_app_with_db):
    payload = {"url": "https://foo.bar"}
    response = test_app_with_db.post("/summaries/", json=payload)
    summary_id = response.json()["id"]

    response = test_app_with_db.get(f"/summaries/{summary_id}/")
    response_dict = response.json()

    assert response.status_code == 200
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == payload["url"]
    assert response_dict["summary"]
    assert response_dict["created_at"]


def test_read_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/summaries/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_read_all_summaries(test_app_with_db):
    payload = {"url": "https://foo.bar"}
    response = test_app_with_db.post("/summaries/", json=payload)
    summary_id = response.json()["id"]

    response = test_app_with_db.get("/summaries/")
    response_list = response.json()

    assert response.status_code == 200
    assert len(list(filter(lambda x: x["id"] == summary_id, response_list))) == 1
