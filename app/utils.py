import requests
import streamlit as st
import pandas as pd
import base64
from geopy import Point
from geopy.geocoders import Nominatim


def get_images():
    response = requests.get("http://localhost:8000/images")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to retrieve images.")
        return []


def create_db_df(images_data):
    df = pd.json_normalize(images_data)
    if "gps" in df.columns:
        df = df.drop(columns="gps")
    df.columns = [col.replace("gps.", "") for col in df.columns]
    return df


def decode_base64(encoded_str: str) -> bytes:
    if encoded_str is not None:
        return base64.b64decode(encoded_str.encode("ascii"))
    return b""


def encode_base64(byte_array: bytes) -> str:
    return base64.b64encode(byte_array).decode("ascii")


def get_country_name(latitude: float, longitude: float) -> str:
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        point = Point(latitude, longitude)
        location = geolocator.reverse(point, exactly_one=True, language="en")
        address = location.raw.get("address")
        if address and "country" in address:
            return address["country"]
    except:
        pass

    return None


def get_duplicates():
    response = requests.get("http://localhost:8000/findDuplicateImages")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to retrieve images.")
        return []


def delete_image(image_name):
    response = requests.delete(f"http://localhost:8000/deleteImage/{image_name}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to delete image: {image_name}")
        return None
