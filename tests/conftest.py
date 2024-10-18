import pytest
from fastapi.testclient import TestClient

from back.app import app


@pytest.fixture
def client():
    return TestClient(app)
