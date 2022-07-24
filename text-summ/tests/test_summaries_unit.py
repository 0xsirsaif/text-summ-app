import json
from datetime import datetime

import pytest

from app.api import crud, summaries


# Create
def test_create_valid_summary(test_client, monkeypatch):
    def mock_generate_summary(mock_summary_id, url):
        return None

    monkeypatch.setattr(summaries, "generate_summary", mock_generate_summary)

    test_request_payload = {"url": "https://foo.bar"}
    test_response_payload = {"id": 1, "url": "https://foo.bar"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_client.post("/summaries/", data=json.dumps(test_request_payload))

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_invalid_summaries(test_client, monkeypatch):
    test_data = {
        "id": 1,
        "url": "https://foo.bar",
        "summary": "summary",
        "created_at": datetime.utcnow().isoformat(),
    }

    async def mock_get(mock_id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_client.get("/summaries/1/")
    assert response.status_code == 200
    assert response.json() == test_data


# GET / Read
def test_read_summary(test_client, monkeypatch):
    test_data = {
        "id": 1,
        "url": "https://foo.bar",
        "summary": "summary",
        "created_at": datetime.utcnow().isoformat(),
    }

    async def mock_get(mock_id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_client.get("/summaries/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_summary_incorrect_id(test_client, monkeypatch):
    async def mock_get(mock_id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_client.get("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_read_all_summaries(test_client, monkeypatch):
    test_data = [
        {
            "id": 1,
            "url": "https://foo.bar",
            "summary": "summary",
            "created_at": datetime.utcnow().isoformat(),
        },
        {
            "id": 2,
            "url": "https://testdrivenn.io",
            "summary": "summary",
            "created_at": datetime.utcnow().isoformat(),
        },
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_client.get("/summaries/")
    assert response.status_code == 200
    assert response.json() == test_data


# Delete
def test_remove_summary(test_client, monkeypatch):
    test_data = {
        "id": 1,
        "url": "https://foo.bar",
        "summary": "summary",
        "created_at": datetime.utcnow().isoformat(),
    }

    async def mock_get(mock_id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(mock_id):
        return mock_id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_client.delete("/summaries/1/")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "url": "https://foo.bar"}


def test_remove_summary_incorrect_id(test_client, monkeypatch):
    async def mock_get(mock_id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_client.delete("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


# PUT / Update
def test_update_summary(test_client, monkeypatch):
    test_request_payload = {"url": "https://foo.bar", "summary": "updated"}
    test_response_payload = {
        "id": 1,
        "url": "https://foo.bar",
        "summary": "summary",
        "created_at": datetime.utcnow().isoformat(),
    }

    async def mock_put(mock_id, payload):
        return test_response_payload

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_client.put("/summaries/1/", data=json.dumps(test_request_payload))
    assert response.status_code == 200
    assert response.json() == test_response_payload


@pytest.mark.parametrize(
    "summary_id, payload, status_code, detail",
    [
        [
            999,
            {"url": "https://foo.bar", "summary": "updated!"},
            404,
            "Summary not found",
        ],
        [
            0,
            {"url": "https://foo.bar", "summary": "updated!"},
            422,
            [
                {
                    "loc": ["path", "summary_id"],
                    "msg": "ensure this value is greater than 0",
                    "type": "value_error.number.not_gt",
                    "ctx": {"limit_value": 0},
                }
            ],
        ],
        [
            1,
            {},
            422,
            [
                {
                    "loc": ["body", "url"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "summary"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ],
        ],
        [
            1,
            {"url": "https://foo.bar"},
            422,
            [
                {
                    "loc": ["body", "summary"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ],
        ],
    ],
)
def test_update_summary_invalid(
    test_client, monkeypatch, summary_id, payload, status_code, detail
):
    async def mock_put(mock_id, mock_payload):
        return None

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_client.put(f"/summaries/{summary_id}/", data=json.dumps(payload))
    assert response.status_code == status_code
    assert response.json()["detail"] == detail


def test_update_summary_invalid_url(test_client, monkeypatch):
    async def mock_put(mock_id, mock_payload):
        return None

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_client.put(
        "/summaries/1/",
        data=json.dumps({"url": "invalid://url", "summary": "updated!"}),
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"
