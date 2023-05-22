from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
import json
from fastapi import status
import pytest
from app.models import DateTimeEncoder
from main import app
import os
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime


client = TestClient(app=app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to ImagePlotter"}


def test_upload_and_calculate_phash():
    test_images_dir = "/home/royga/eass/finalproject/myImages/test_images"
    test_images = ["IMG_11.jpeg", "IMG_12(copy).jpeg"]
    files = [
        ("images", (open(os.path.join(test_images_dir, image_name), "rb")))
        for image_name in test_images
    ]
    response = client.post("/images/", files=files)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["status"] == "success"
    assert response.json()["message"] == f"{len(test_images)} images uploaded"


test_image_name = "image5.jpg"
test_image_name2 = "image7.jpg"
test_date = datetime(2022, 6, 2, 12, 0, 0)


def test_get_image():
    response = client.get(f"/images/{test_image_name}")
    assert response.status_code == 200
    assert response.json()["name"] == test_image_name
    response = client.get("/images/nonexistent_image.jpg")
    assert response.status_code == 404


def test_get_images():
    response = client.get("/images")
    assert response.status_code == 200
    images = response.json()
    assert len(images) > 0


def test_delete_image():
    response = client.delete(f"/deleteImage/{test_image_name}")
    assert response.status_code == 200
    assert response.json()["message"] == f"{test_image_name} deleted"
    fake_image_name = "fake_image.jpg"
    response = client.delete(f"/deleteImage/{fake_image_name}")
    assert response.status_code == 404


def test_find_duplicate():
    with pytest.warns(
        RuntimeWarning, match="Parameter num_enc_workers has no effect"
    ):
        response = client.get("/findDuplicateImages")
    assert response.status_code == 200
    assert "image7.jpg" in response.json()["duplicates"]


def test_datetime_encoder():
    dt = datetime(2023, 5, 7, 14, 30)
    encoded_dt = json.dumps(dt, cls=DateTimeEncoder)
    assert encoded_dt == '"2023-05-07 14:30:00"'
