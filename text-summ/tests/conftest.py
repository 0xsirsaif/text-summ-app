import os

import pytest
# this is come directly from starlette.testclient
from fastapi.testclient import TestClient


from app import main
from app.config import get_settings, Settings


def get_settings_overrides():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_client():
    app = main.generate_app()
    app.dependency_overrides[get_settings] = get_settings_overrides
    with TestClient(app) as test_client:
        yield test_client
