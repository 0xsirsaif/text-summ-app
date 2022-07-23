import json

import pytest


# Create
def test_create_valid_summary(test_client_with_db):
    response = test_client_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://facebook.com"})
    )
    assert response.status_code == 201
    assert response.json()["url"] == "https://facebook.com"


def test_create_invalid_summary(test_client_with_db):
    response = test_client_with_db.post("/summaries/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }

    response = test_client_with_db.post(
        "/summaries/", data=json.dumps({"url": "invalid://url"})
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"


# Get
def test_get_single_summary(test_client_with_db):
    new_summary = test_client_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://facebook.com"})
    )
    summary_id = new_summary.json()["id"]

    assert (
        summary_id == test_client_with_db.get(f"/summaries/{summary_id}").json()["id"]
    )
    assert new_summary.status_code == 201

    new_summary_json = new_summary.json()
    assert new_summary_json["id"] == summary_id
    assert new_summary_json["url"] == "https://facebook.com"
    # assert new_summary_json["summary"]
    # assert new_summary_json["created_at"]


def test_get_non_existed_summary(test_client_with_db):
    response = test_client_with_db.get("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"

    response = test_client_with_db.get("/summaries/0/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "summary_id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_get_all_summaries(test_client_with_db):
    # --- SetUp/Given --- #
    data_posted = test_client_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://SOSO.com"})
    )

    # --- When --- #
    response = test_client_with_db.get("/summaries/")
    # -- Then --- #
    assert response.status_code == 200
    assert (
        len(
            list(
                filter(
                    lambda record: record["id"] == data_posted.json()["id"],
                    response.json(),
                )
            )
        )
        == 1
    )


# Delete
def test_delete_certain_summary(test_client_with_db):
    # Given: add dummy one
    dummy_summary = test_client_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://saif.exeplains.com/"})
    )
    dummy_summary_id = dummy_summary.json()["id"]

    assert dummy_summary.status_code == 201
    assert dummy_summary.json()["url"] == "https://saif.exeplains.com/"

    # Then: Delete it
    response = test_client_with_db.delete(f"/summaries/{dummy_summary_id}/")

    # Assert: Dummy deleted
    assert response.status_code == 200
    assert response.json() == {
        "id": dummy_summary_id,
        "url": "https://saif.exeplains.com/",
    }


def test_delete_invalid_summary(test_client_with_db):
    # Given: no
    # Then
    response = test_client_with_db.delete("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"
    # Then
    response = test_client_with_db.delete("/summaries/0/")
    # Assert
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "summary_id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


# Update
def test_update_summary(test_client_with_db):
    response = test_client_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_client_with_db.put(
        f"/summaries/{summary_id}/",
        data=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"] == "updated!"
    assert response_dict["created_at"]


def test_update_summary_incorrect_id(test_client_with_db):
    response = test_client_with_db.put(
        "/summaries/999/",
        data=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary_invalid_json(test_client_with_db):
    not_found_summary = test_client_with_db.put(
        "/summaries/999/",
        data=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
    )
    assert not_found_summary.status_code == 404
    assert not_found_summary.json()["detail"] == "Summary not found"

    invalid_id_summary = test_client_with_db.put(
        "/summaries/0/",
        data=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
    )
    assert invalid_id_summary.status_code == 422
    assert invalid_id_summary.json() == {
        "detail": [
            {
                "loc": ["path", "summary_id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_update_summary_invalid_keys(test_client_with_db):
    response = test_client_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_client_with_db.put(
        f"/summaries/{summary_id}/", data=json.dumps({"url": "https://foo.bar"})
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "summary"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }

    response = test_client_with_db.put(
        f"/summaries/{summary_id}/",
        data=json.dumps({"url": "invalid://url", "summary": "updated!"}),
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"


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
    test_client_with_db, summary_id, payload, status_code, detail
):
    response = test_client_with_db.put(
        f"/summaries/{summary_id}/", data=json.dumps(payload)
    )
    assert response.status_code == status_code
    assert response.json()["detail"] == detail


def test_update_summary_invalid_url(test_client):
    response = test_client.put(
        "/summaries/1/",
        data=json.dumps({"url": "invalid://url", "summary": "updated!"}),
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"
