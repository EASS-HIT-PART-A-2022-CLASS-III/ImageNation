from fastapi.testclient import TestClient
from main import app
from models import ImageModel, GPS
from datetime import datetime
import base64
import io
import os
import json
import tempfile
import shutil
import time
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from imagededup.methods import PHash
from imagededup.utils import plot_duplicates
import numpy as np
from typing import List, Dict, Optional, Tuple, Union
from fastapi import Body, FastAPI, File, Request, UploadFile, HTTPException, status
from fastapi.encoders import jsonable_encoder
from starlette.middleware.base import BaseHTTPMiddleware


client = TestClient(app=app)

fakeDB = {
    "image1.jpg": {
        "name": "image1.jpg",
        "phash": "abc123",
        "gps": {
            "latitude": 37.7749,
            "longitude": -122.4194,
            "altitude": 0.0
        },
        "date": "2022-05-05 12:00:00"
    },
    "image2.jpg": {
        "name": "image2.jpg",
        "phash": "def456",
        "gps": None,
        "date": "2022-05-05 12:00:00"
    },
    "image3.jpg": {
        "name": "image2.jpg",
        "phash": "abc123",
        "gps": {
            "latitude": 10.0,
            "longitude": 20.0,
            "altitude": 30.0
        },
        "date": "2022-05-02 12:00:00",
        "image": None
    }
}

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to ImagePlotter"}

def test_upload_and_calculate_phash():
    test_images_dir = "/home/royga/eass/finalproject/myImages/test_images/"
    test_images = ["IMG_1.jpeg", "IMG_2.jpeg", "IMG_3.jpeg","IMG_4(copy).jpeg"]
    files = [("files", (open(os.path.join(test_images_dir, image_name), "rb"))) for image_name in test_images]
    response = client.post("/images/", files=files)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["status"] == "success"
    assert response.json()["message"] == f"{len(test_images)} images uploaded"