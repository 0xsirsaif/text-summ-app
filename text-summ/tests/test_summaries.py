import json


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
    response = test_client_with_db.get("/summaries/100000000000")

    assert response.status_code == 404
    assert response.json() == {"detail": "Summary 100000000000 not found!"}


def test_get_all_summaries(test_client_with_db):
    # --- SetUp/Given --- #
    data_posted = test_client_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://SOSO.com"})
    )

    # --- When --- #
    response = test_client_with_db.get("/summaries")
    print(response)
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
