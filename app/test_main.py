from fastapi.testclient import TestClient
from fastapi import status
from main import app
import os
from PIL.ExifTags import TAGS, GPSTAGS

client = TestClient(app=app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to ImagePlotter"}

def test_upload_and_calculate_phash():
     test_images_dir = "test_images" #"/home/royga/eass/finalproject/myImages/test_images/"
     test_images = ["IMG_1.jpeg", "IMG_2.jpeg", "IMG_3.jpeg","IMG_4(copy).jpeg"]
     files = [("files", (open(os.path.join(test_images_dir, image_name), "rb"))) for image_name in test_images]
     response = client.post("/images/", files=files)
     assert response.status_code == status.HTTP_201_CREATED
     assert response.json()["status"] == "success"
     assert response.json()["message"] == f"{len(test_images)} images uploaded"


test_image_name = "image1.jpg"

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
    assert test_image_name in [image["name"] for image in images]







# def test_upload_and_calculate_phash():
#     test_images_dir = "test_images"
#     image_files = [
#         (image_file, open(os.path.join(test_images_dir, image_file), "rb"))
#         for image_file in os.listdir(test_images_dir)
#     ]

#     response = client.post(
#         "/images/",
#         files=[("files", (image_file, image_content, "image/jpeg")) for image_file, image_content in image_files]
#     )

#     for _, image_content in image_files:
#         image_content.close()

#     assert response.status_code == 201
#     assert response.json() == {"status": "success", "message": f"{len(image_files)} images uploaded"}