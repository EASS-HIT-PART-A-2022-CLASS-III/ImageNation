import warnings
from fastapi.testclient import TestClient
from fastapi import status
import pytest
import sys
from pathlib import Path

current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))
from main import app


@pytest.fixture
def test_app() -> TestClient:
    return TestClient(app)


def test_home(test_app: TestClient):
    response = test_app.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Image_Processor is UP"}


def test_process_image_file(test_app: TestClient):
    path = "test_images"
    test_images = ["testImage1.jpeg", "testImage2.jpeg", "testImageCopy.jpeg"]
    for image_name in test_images:
        image_path = f"{path}/{image_name}"
        with open(image_path, "rb") as image_file:
            response = test_app.post(
                "/process_image/",
                files={"image": (image_name, image_file, "image/jpeg")},
            )
        assert response.status_code == 200
        response_data = response.json()
        assert "name" in response_data
        assert "phash" in response_data
        assert "size" in response_data
        assert "gps" in response_data
        assert "location" in response_data
        assert "date" in response_data
        assert "content" in response_data
        assert "smallRoundContent" in response_data


def test_get_location_details(test_app: TestClient):
    latitude = 37.7749
    longitude = -122.4194
    response = test_app.get(
        f"/get_location_details/?latitude={latitude}&longitude={longitude}"
    )
    assert response.status_code == 200
    response_data = response.json()
    assert "country" in response_data
    assert "data" in response_data
    assert response_data["country"] == "United States"


def test_find_duplicates(test_app: TestClient):
    images = [
        {"name": "image1.jpg", "phash": "d1d1d1d1d1d1d1d1"},
        {"name": "image2.jpg", "phash": "d1d1d1d1d1d1d1d2"},
        {"name": "image3.jpg", "phash": "ffffffffffffffff"},
    ]
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", category=RuntimeWarning, module="imagededup.methods.hashing"
        )
        response = test_app.post("/find_duplicates/", json=images)
        assert response.status_code == 200
        response_data = response.json()
        assert "duplicates" in response_data
        assert "image2.jpg" in response_data["duplicates"]
