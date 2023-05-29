import streamlit as st
import io
import pandas as pd
import base64
import httpx

API_URL = "http://localhost:8000"


@st.cache_data
def load_data():
    with st.spinner("Loading Data..."):
        images_data = get_images()
        df = create_db_df(images_data)
        st.success("Data Loaded!")
        return df


@st.cache_data
def get_images():
    with httpx.Client() as client:
        response = client.get(f"{API_URL}/images")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to retrieve images.")
            return []


def create_db_df(images_data):
    df = pd.json_normalize(images_data, sep="_")
    if "gps" in df.columns:
        df = df.drop(columns="gps")
    if "location" in df.columns:
        df["location"] = df["location"].apply(
            lambda loc: loc["country"]
            if isinstance(loc, dict) and "country" in loc
            else None
        )
    df.columns = [
        col.replace("gps_", "").replace("location_", "") for col in df.columns
    ]
    return df


def decode_base64(encoded_str: str) -> bytes:
    if encoded_str is not None:
        return base64.b64decode(encoded_str.encode("ascii"))
    return b""


def encode_base64(byte_array: bytes) -> str:
    return base64.b64encode(byte_array).decode("ascii")


# TODO: Fix this to use backend route

# def get_country_name(latitude: float, longitude: float) -> str:
#     try:
#         geolocator = Nominatim(user_agent="geoapiExercises")
#         point = Point(latitude, longitude)
#         location = geolocator.reverse(point, exactly_one=True, language="en")
#         address = location.raw.get("address")
#         if address and "country" in address:
#             return address["country"]
#     except:
#         pass

#     return None


def get_duplicates():
    with httpx.Client() as client:
        response = client.get(f"{API_URL}/findDuplicateImages")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to retrieve images.")
            return []


def delete_image(image_name):
    with httpx.Client() as client:
        response = client.delete(f"{API_URL}/deleteImage/{image_name}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to delete image: {image_name}")
            return None


def upload_images(uploaded_files):
    files_dict = []
    for uploaded_file in uploaded_files:
        file_bytes = io.BytesIO(uploaded_file.read())
        files_dict.append(
            ("images", (uploaded_file.name, file_bytes, uploaded_file.type))
        )
    with httpx.Client() as client:
        response = client.post(f"{API_URL}/images/", files=files_dict)
    return response
