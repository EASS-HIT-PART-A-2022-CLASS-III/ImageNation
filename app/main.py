from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List, Dict, Optional, Tuple, Union
from imagededup.methods import PHash
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import io
import os
from datetime import datetime
import base64
from models import ImageModel, GPS


app = FastAPI()

database = {}


async def read_image_data(file: UploadFile) -> bytes:
    return await file.read()

def extract_gps_and_date(image_data: bytes) -> Tuple[float, float, float, datetime]:
    try:
        with Image.open(io.BytesIO(image_data)) as img:
            exif_data = img._getexif()
        if exif_data:
          gps_data = {}
        datetime_original = None
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "GPSInfo":
                    for gps_tag in value:
                        sub_tag = GPSTAGS.get(gps_tag, gps_tag)
                        gps_data[sub_tag] = value[gps_tag]
                elif tag_name == "DateTimeOriginal":
                    datetime_original = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
        if gps_data:
            latitude = gps_data.get('GPSLatitude', None)
            longitude = gps_data.get('GPSLongitude', None)
            latitude_ref = gps_data.get('GPSLatitudeRef', None)
            longitude_ref = gps_data.get('GPSLongitudeRef', None)
            altitude = gps_data.get('GPSAltitude', None)
            altitude_ref = gps_data.get('GPSAltitudeRef', None)
            if latitude and longitude and latitude_ref and longitude_ref:
                lat = (latitude[0] + latitude[1] / 60 + latitude[2] / 3600) * (-1 if latitude_ref == 'S' else 1)
                lon = (longitude[0] + longitude[1] / 60 + longitude[2] / 3600) * (-1 if longitude_ref == 'W' else 1)
                altitude = altitude * (-1 if altitude_ref == 1 else 1)
                return lat, lon, altitude, datetime_original
        return None, None, None, datetime_original
    except Exception as e:
        print(e)
        return None, None, None, None

def calculate_phash_value(image_data: bytes) -> str:
    phasher = PHash()
    with Image.open(io.BytesIO(image_data)) as img:
         return phasher.encode_image(image_array=img)

async def process_image_file(file: UploadFile) -> Union[ImageModel, None]:
    image_data = await read_image_data(file)
    lat, lon, alt, date = extract_gps_and_date(image_data)
    gps_data = GPS(latitude=lat, longitude=lon, altitude=alt)
    #phash_value = calculate_phash_value(image_data)
    image_obj = ImageModel(
        name=file.filename,
        #phash=phash_value,
        gps=gps_data.dict(),
        date=date,
        image=image_data
    )
    return image_obj

@app.post("/upload_image_and_calculate_phash/")
async def upload_and_calculate_phash(files: List[UploadFile] = File(...)):
    for file in files:
        image_obj = await process_image_file(file)
        if image_obj:
            database[image_obj.name] = image_obj.dict()
    return {"status": "success", "message": f"{len(files)} images uploaded"}

@app.get("/images/{image_name}")
async def get_image(image_name: str):
    if image_name not in database:
        raise HTTPException(status_code=404, detail=f"Image {image_name} not found")
    image_obj = ImageModel(**database[image_name])
    return image_obj

@app.delete("/delete_image/{image_name}")
async def delete_image(image_name: str):
    if image_name not in database:
        raise HTTPException(status_code=404, detail=f"Image {image_name} not found")
    del database[image_name]
    return {"status": "success", "message": f"{image_name} deleted"}



















""" @app.get("/find_duplicates")
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
    return {"duplicates": duplicates} """