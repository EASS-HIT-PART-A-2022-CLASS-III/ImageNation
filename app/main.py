import shutil
import time
from fastapi import Body, FastAPI, File, Request, UploadFile, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List, Dict, Optional, Tuple, Union
from imagededup.methods import PHash
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import io
import os
from datetime import datetime
import base64
from models import ImageModel, GPS
import tempfile
from starlette.middleware.base import BaseHTTPMiddleware


app = FastAPI(title="ImagePlotter", version="0.1.0")

class ProccessingTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    
app.add_middleware(ProccessingTimeMiddleware)



image1 = ImageModel(
    name="image1.jpg",
    phash="aabbccddeeff0011",
    gps=GPS(latitude=12.34, longitude=56.78, altitude=90.0),
    date=datetime(2022, 1, 1, 12, 0, 0),
    image="fdsfdgfddsgfd",
)

image2 = ImageModel(
    name="image2.jpg",
    phash="1122334455667788",
    gps=GPS(latitude=-12.34, longitude=-56.78, altitude=100.0),
    date=datetime(2022, 2, 2, 12, 0, 0),
    image="sffdsgvcvee",
)

image3 = ImageModel(
    name="image3.jpg",
    phash="1122334455667788",
    gps=None,
    date=datetime(2022, 3, 3, 12, 0, 0),
    image="ddsfvfdgfdgfd",
)

database = {
    image1.name: image1,
    image2.name: image2,
    image3.name: image3,
}

async def extract_gps_data_and_convert_to_decimal(gps_data: dict) -> Tuple[float, float, float]:
    latitude = gps_data.get('GPSLatitude', None)
    longitude = gps_data.get('GPSLongitude', None)
    latitude_ref = gps_data.get('GPSLatitudeRef', None)
    longitude_ref = gps_data.get('GPSLongitudeRef', None)
    altitude = gps_data.get('GPSAltitude', None)
    altitude_ref = gps_data.get('GPSAltitudeRef', None)
    if latitude and longitude and latitude_ref and longitude_ref:
        lat = (latitude[0] + latitude[1] / 60 + latitude[2] / 3600) * (-1 if latitude_ref == 'S' else 1)
        lon = (longitude[0] + longitude[1] / 60 + longitude[2] / 3600) * (-1 if longitude_ref == 'W' else 1)
        alt = altitude * (-1 if altitude_ref == 1 else 1)
        return lat, lon, alt
    else:
        return None, None, None
        
def encode_base64(byte_array: bytes) ->str:
    return base64.b64encode(byte_array).decode('ascii')

def decode_base64(encoded_str: str) -> bytes:
    return base64.b64decode(encoded_str.encode('ascii'))

async def read_image_data(file: UploadFile) -> bytes:
    return await file.read()

async def parse_gps_and_date(image_data: bytes) -> Tuple[float, float, float, datetime]:
    try:
        with Image.open(io.BytesIO(image_data)) as img:
            exif_data = img._getexif()
        if exif_data:
            gps_data = {}
            datetime_original = None
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "GPSInfo":
                    for gps_tag in value:
                        sub_tag = GPSTAGS.get(gps_tag, gps_tag)
                        gps_data[sub_tag] = value[gps_tag]
                elif tag_name == "DateTimeOriginal":
                    datetime_original = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
        if gps_data:
            lat, lon, altitude = await extract_gps_data_and_convert_to_decimal(gps_data)
            return lat, lon, altitude, datetime_original
        else:
             return None, None, None, datetime_original
    except Exception as e:
        print({f"error": str(e)})
        return None, None, None, None

async def calculate_phash_value(image_data: bytes) -> str:
    phasher = PHash()
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        try:
            tmp_file.write(image_data)
            path = tmp_file.name
            result = phasher.encode_image(path)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            shutil.os.remove(path)
    return result

async def process_image_file(file: UploadFile) -> Union[ImageModel, None]:
    image_data = await read_image_data(file)
    lat, lon, alt, date = await parse_gps_and_date(image_data)
    gps_data = GPS(latitude=lat, longitude=lon, altitude=alt)
    phash_value = await calculate_phash_value(image_data)
    image_encoded = encode_base64(image_data)
    image_obj = ImageModel(
        name=file.filename,
        phash=phash_value,
        gps=gps_data.dict(),
        date=date,
        image=image_encoded
    )
    return image_obj

@app.get("/", status_code=status.HTTP_200_OK)
async def home():
    return {"message": "Welcome to ImagePlotter"}


@app.post("/images/", response_description="The created images", status_code=status.HTTP_201_CREATED)
async def upload_and_calculate_phash(files: List[UploadFile] = File(...)):
    for file in files:
        image_obj = await process_image_file(file)
        if image_obj:
            database[image_obj.name] = image_obj
    return {"status": "success", "message": f"{len(files)} images uploaded",}


# @app.get("/images/{image_name}", response_model=ImageModel, response_description="The image", status_code=status.HTTP_200_OK)
# async def get_image(image_name: str):
#     if image_name not in database:
#         raise HTTPException(status_code=404, detail=f"Image {image_name} not found")
#     image_obj = ImageModel(**database[image_name])
#     return {"image": image_obj}

@app.get("/images/{image_name}", response_model=ImageModel, response_description="The image", status_code=status.HTTP_200_OK)
async def get_image(image_name: str):
    if image_name not in database:
        raise HTTPException(status_code=404, detail=f"Image {image_name} not found")
    return database[image_name]

@app.get("/images", response_model=List[ImageModel], response_description="The list of images", status_code=status.HTTP_200_OK)
async def get_images():
    if database:
        return list(database.values())
    else:
        raise HTTPException(status_code=404, detail=f"No images found")


@app.delete("/deleteImage/{image_name}", response_description="The deleted image")
async def delete_image(image_name: str):
    if image_name not in database:
        raise HTTPException(status_code=404, detail=f"Image {image_name} not found")
    del database[image_name]
    return {"status": "success", "message": f"{image_name} deleted"}

@app.put("/updateImage/{image_name}", response_model=ImageModel, response_description="The updated image",status_code=status.HTTP_202_ACCEPTED)
async def update_image(image_name: str, image: ImageModel):
    if image_name not in database:
        raise HTTPException(status_code=404, detail=f"Image {image_name} not found")
    update_image_encoded = jsonable_encoder(image)
    database[image_name] = update_image_encoded
    return {"image": update_image_encoded}

@app.patch("/patchImage/{image_name}", response_model=ImageModel, response_description="The updated image", status_code=status.HTTP_202_ACCEPTED)
async def patch_image(image_name: str, image: ImageModel):
    if image_name not in database:
        raise HTTPException(status_code=404, detail=f"Image {image_name} not found")
    stored_image_data = database.get(image_name)
    if stored_image_data is not None:
        stored_image_model = ImageModel(**stored_image_data)    
        update_data = image.dict(exclude_unset=True)
        update_image = stored_image_model.copy(update=update_data)
        update_image_encoded = jsonable_encoder(update_image)
        database[image_name] = update_image_encoded
        return {"image": update_image_encoded}
    else:
        database[image_name] = image
    return {"status": "success", "message": f"{image_name} updated"}

async def find_duplicate_images(images: Dict[str, ImageModel]) -> List[str]:
    phasher = PHash()
    encoding_images = {}
    for image_name, image_model in images.items():
        if image_model.phash:
            encoding_images[image_name] = image_model.phash
        elif image_model.image:
            encoding_images[image_name] = await calculate_phash_value(image_model.image)
    duplicates = phasher.find_duplicates_to_remove(encoding_map=encoding_images, max_distance_threshold=12)
    return duplicates

@app.get("/findDuplicateImages",tags=["Dup"], response_description="The duplicate images", status_code=status.HTTP_200_OK)
async def find_duplicate(): 
    if database:
        duplicates = await find_duplicate_images(database)
        return {"duplicates": duplicates}
    else:
        raise HTTPException(status_code=404, detail=f"No images found")