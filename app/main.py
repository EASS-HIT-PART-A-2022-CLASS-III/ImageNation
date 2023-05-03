from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List, Dict
from imagededup.methods import PHash
from PIL import Image, UnidentifiedImageError
import io
import os

app = FastAPI()


database = {}

async def read_image_data(file: UploadFile) -> bytes:
    return await file.read()

def extract_gps_coordinates(image_data: bytes) -> tuple:
    try:
        with Image.open(io.BytesIO(image_data)) as img:
            exif_data = img.getexif()
            lat, lon = exif_data[34853][:2] 
    except (IOError, AttributeError, KeyError):
        lat, lon = None, None
    return lat, lon

def calculate_phash_value(image_data: bytes) -> str:
    phasher = PHash()
    with Image.open(io.BytesIO(image_data)) as img:
        return phasher.encode_image(image_array=img)

async def process_image_file(file: UploadFile) -> dict:
    image_data = await read_image_data(file)
    lat, lon = extract_gps_coordinates(image_data)
    if lat is None or lon is None:
        return None
    phash_value = calculate_phash_value(image_data)
    return {'phash': phash_value, 'lat': lat, 'lon': lon}

@app.post("/upload_and_calculate_phash/")
async def upload_and_calculate_phash(files: List[UploadFile] = File(...)):
    for file in files:
        image_data = await process_image_file(file)
        if image_data is not None:
            database[file.filename] = image_data

    return {"status": "success"}




@app.get("/find_duplicates")
async def find_duplicates():
    # Create a list to hold the image paths
    image_paths = []

    # Loop through the image data in the database
    for filename, data in database.items():
        # Get the image path and PHash value
        image_path = os.path.join(images_dir, filename)
        phash_value = data['phash']

        # Add the image path to the list
        image_paths.append(image_path)

    # Use ImageDedup to find duplicate images
    duplicates = phasher.find_duplicates(image_dir=images_dir, image_list=image_paths)

    # Return the duplicate images as a dictionary
    return {"duplicates": duplicates}