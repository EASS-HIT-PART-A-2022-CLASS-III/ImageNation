import streamlit as st
import io
import pandas as pd
import base64
import httpx
from streamlit_extras.switch_page_button import switch_page
import asyncio

API_URL = "http://localhost:8000"


def load_data():
    with st.spinner("Loading Data..."):
        images_data = asyncio.run(get_images_data())
        df = create_db_df(images_data)
        st.success("Data Loaded!")
        return df


async def get_images_data():
    headers = {"Authorization": f"Bearer {st.session_state['user']['access_token']}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/images/data/", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to retrieve images.")
            return []


def create_db_df(images_data):
    df = pd.DataFrame(images_data)
    return df


def decode_base64(encoded_str: str) -> bytes:
    if encoded_str is not None:
        return base64.b64decode(encoded_str.encode("ascii"))
    return b""


def encode_base64(byte_array: bytes) -> str:
    return base64.b64encode(byte_array).decode("ascii")


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
            ("upload_images", (uploaded_file.name, file_bytes, uploaded_file.type))
        )
    headers = {"Authorization": f"Bearer {st.session_state['user']['access_token']}"}
    with httpx.Client() as client:
        response = client.post(f"{API_URL}/images/", files=files_dict, headers=headers)
    return response


async def login(email: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/login/", data={"username": email, "password": password}
        )

    if response.status_code == 200:
        data = response.json()
        token = data["access_token"]
        if token is not None:
            st.session_state["user"]["access_token"] = token
            st.session_state["user"]["name"] = data["user_name"]
            st.session_state["user"]["logged_in"] = True
            switch_page("Home")
        else:
            st.session_state["user"][
                "action_status"
            ] = "Login failed. Please try again."

    else:
        st.session_state["user"]["logged_in"] = False
        st.session_state["user"][
            "action_status"
        ] = "Login failed. Please check your credentials."


async def signup(name: str, email: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/users/",
            json={"name": name, "email": email, "password": password},
        )
    if response.status_code == 201:
        st.session_state["user"]["action_status"] = "Sign up Successful"
        st.session_state["user"]["logged_in"] = True
        if email and password:
            await login(email, password)
    else:
        st.session_state["user"]["logged_in"] = False
        st.session_state["user"]["action_status"] = "Sign up Failed"


def logout():
    st.session_state["user"] = {
        "name": None,
        "logged_in": False,
        "access_token": None,
        "action_status": "Logout Successful",
    }
    switch_page("Home")


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: 100% 100%;  
        background-position: center;
    }}

    .css-cio0dv.egzxvld1
        {{
            visibility: hidden;
        }}
    </style>

    <h1 style='text-align: center; pointer-events: none;'>
    <span style='color: black;'>Welcome To </span></span><span style='color: green;'>I</span><span style='color: yellow;'>M</span><span style='color: orange;'>A</span><span style='color: red;'>G</span><span style='color: violet;'>E</span><span>-</span><span style='color: indigo;'>N</span><span style='color: blue;'>A</span><span style='color: green;'>T</span><span style='color: yellow;'>I</span><span style='color: orange;'>O</span><span style='color: red;'>N</span><span> 🌍</span>
    </h1>
    <h2 style='text-align: center; pointer-events: none;'>
    <span style='color: black;'>Are you ready to re-explore the world? 🛺</span>
    </h2>
    
    """,
        unsafe_allow_html=True,
    )
