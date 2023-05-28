import base64
from fastapi import FastAPI, Request, UploadFile, HTTPException, status, File
import shutil
from fastapi.encoders import jsonable_encoder
from typing import List, Dict, Tuple, Union
from imagededup.methods import PHash
from PIL import Image, ImageDraw, ImageOps, ImagePath
from PIL.ExifTags import TAGS, GPSTAGS
import io
from datetime import datetime
from models import ImageModel, GPS, Location
import tempfile
from geopy import Point
from geopy.geocoders import Nominatim


# image5 = ImageModel(
#     name="image5.jpg",
#     phash="aabbccddeeff0011",
#     gps=GPS(latitude=12.34, longitude=56.78, altitude=90.0),
#     date=datetime(2022, 1, 1, 12, 0, 0),
#     image="fdsfdgfddsgfd",
# )

# image6 = ImageModel(
#     name="image6.jpg",
#     phash="1122334455667788",
#     gps=GPS(latitude=-12.34, longitude=-56.78, altitude=100.0),
#     date=datetime(2022, 2, 2, 12, 0, 0),
#     image="sffdsgvcvee",
# )

# image7 = ImageModel(
#     name="image7.jpg",
#     phash="1122334455667788",
#     gps=None,
#     location=Location(country="Israel", data={"state": "israel"}),
#     date=datetime(2022, 3, 3, 12, 0, 0),
#     image="ddsfvfdgfdgfd",
# )

# database = {
#     image5.name: image5,
#     image6.name: image6,
#     image7.name: image7,
# }


async def extract_gps_data_and_convert_to_decimal(
    gps_data: dict,
) -> Tuple[float, float, float, float]:
    latitude = gps_data.get("GPSLatitude", None)
    longitude = gps_data.get("GPSLongitude", None)
    latitude_ref = gps_data.get("GPSLatitudeRef", None)
    longitude_ref = gps_data.get("GPSLongitudeRef", None)
    altitude = gps_data.get("GPSAltitude", None)
    altitude_ref = gps_data.get("GPSAltitudeRef", b"\x00")
    direction = gps_data.get("GPSImgDirection", None)
    if latitude and longitude and latitude_ref and longitude_ref:
        lat = (latitude[0] + latitude[1] / 60 + latitude[2] / 3600) * (
            -1 if latitude_ref == "S" else 1
        )
        lon = (longitude[0] + longitude[1] / 60 + longitude[2] / 3600) * (
            -1 if longitude_ref == "W" else 1
        )
        if altitude is not None:
            alt = altitude * (-1 if altitude_ref == b"\x01" else 1)
        else:
            alt = None
        dir = direction

        return lat, lon, alt, dir
    else:
        return None, None, None, None


def decode_base64(encoded_str: str) -> bytes:
    if encoded_str is not None:
        return base64.b64decode(encoded_str.encode("ascii"))
    return b""


def encode_base64(byte_array: bytes) -> str:
    return base64.b64encode(byte_array).decode("ascii")


# def get_country_name(latitude: float, longitude: float) -> str:
#     try:
#         geolocator = Nominatim(user_agent="geoapiExercises")
#         point = Point(latitude, longitude)
#         location = geolocator.reverse(point, exactly_one=True, language="en")
#         address = location.raw.get("address")
#         print(address)
#         if address and "country" in address:
#             return address["country"]
#     except Exception as e:
#         raise HTTPException(
#             status.HTTP_503_SERVICE_UNAVAILABLE,
#             detail="error when getting country name",
#         )
#     return None


def get_country_name(location_details: dict) -> str:
    return location_details.get("country")


def get_location_details(latitude: float, longitude: float) -> dict:
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        point = Point(latitude, longitude)
        location = geolocator.reverse(point, exactly_one=True, language="en")
        address = location.raw.get("address")

        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No location details found",
            )

        return address
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error when getting location details",
        )


async def read_image_data(file: UploadFile) -> bytes:
    return await file.read()


async def delete_exif_data(img: Image) -> Image:
    data = list(img.getdata())
    img_without_exif = Image.new(img.mode, img.size)
    img_without_exif.putdata(data)
    return img_without_exif


async def parse_gps_and_date(
    image_data: bytes,
) -> Tuple[float, float, float, float, datetime]:
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
                    datetime_original = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
        if gps_data:
            (
                lat,
                lon,
                altitude,
                dir,
            ) = await extract_gps_data_and_convert_to_decimal(gps_data)
            return lat, lon, altitude, dir, datetime_original
        else:
            return None, None, None, None, datetime_original
    except Exception as e:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="error when parsing gps and date",
        )


async def calculate_phash_value(image_data: bytes) -> str:
    phasher = PHash()
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        try:
            tmp_file.write(image_data)
            path = tmp_file.name
            result = phasher.encode_image(path)
        except Exception as e:
            raise HTTPException(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="error when calculating phash",
            )
        finally:
            shutil.os.remove(path)
    return result


async def find_duplicate_images(images: Dict[str, ImageModel]) -> List[str]:
    phasher = PHash()
    encoding_images = {}
    for image_name, image_model in images.items():
        if image_model.phash:
            encoding_images[image_name] = image_model.phash
        elif image_model.image:
            encoding_images[image_name] = await calculate_phash_value(image_model.image)
    duplicates = phasher.find_duplicates_to_remove(
        encoding_map=encoding_images, max_distance_threshold=12
    )
    return duplicates


def make_round(
    image,
    size=(40, 40),
    border=5,
    fill_color="white",
    outer_color="black",
    outer_width=2,
):
    image = image.resize(size, Image.LANCZOS)
    result = Image.new(
        "RGBA",
        (
            size[0] + border * 2 + outer_width * 2,
            size[1] + border * 2 + outer_width * 2,
        ),
    )
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    result.paste(image, (border + outer_width, border + outer_width), mask=mask)
    draw = ImageDraw.Draw(result)
    draw.ellipse(
        (0, 0, result.size[0] - 1, result.size[1] - 1),
        outline=outer_color,
        width=outer_width,
    )
    draw.ellipse(
        (
            outer_width,
            outer_width,
            result.size[0] - outer_width - 1,
            result.size[1] - outer_width - 1,
        ),
        outline=fill_color,
        width=border,
    )

    return result


async def process_small_image_data(image_data: bytes) -> bytes:
    try:
        with Image.open(io.BytesIO(image_data)) as img:
            processed_img = make_round(img)
            byte_arr = io.BytesIO()
            processed_img.save(byte_arr, format="PNG")
            return byte_arr.getvalue()
    except Exception as e:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="error when processing small image",
        )


async def process_image_file(image: UploadFile) -> Union[ImageModel, None]:
    image_data = await read_image_data(image)
    phash_value = await calculate_phash_value(image_data)
    lat, lon, alt, dir, date = await parse_gps_and_date(image_data)
    gps_data = GPS(latitude=lat, longitude=lon, altitude=alt, direction=dir)
    file_size = float(len(image_data))
    image_encoded = encode_base64(image_data)
    small_image_data = await process_small_image_data(image_data)
    small_round_image = encode_base64(small_image_data)
    location_data = get_location_details(lat, lon)
    country = get_country_name(location_data)
    location = Location(country=country, data=location_data)
    image_obj = ImageModel(
        name=image.filename,
        phash=phash_value,
        size=file_size,
        gps=gps_data.dict(),
        location=location,
        date=date,
        content=image_encoded,
        smallRoundContent=small_round_image,
    )
    print(location)
    return image_obj
