import json
import os
from fastapi.testclient import TestClient
from fastapi import status
import pytest
import sys
from pathlib import Path

os.environ["TESTING"] = "1"
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))
from main import app
from data_base import database


@pytest.fixture
def test_app() -> TestClient:
    return TestClient(app)


def test_home(test_app: TestClient):
    response = test_app.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Backend is up and running!"}
