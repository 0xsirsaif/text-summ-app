import os

import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app import main
from app.config import Settings, get_settings


def get_settings_overrides():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_client():
    app = main.generate_app()
    app.dependency_overrides[get_settings] = get_settings_overrides
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def test_client_with_db():
    app = main.generate_app()
    app.dependency_overrides[get_settings] = get_settings_overrides
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )

    with TestClient(app) as test_client_with_db:
        yield test_client_with_db
