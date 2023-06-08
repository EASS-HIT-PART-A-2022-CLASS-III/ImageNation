import streamlit as st
import io
import pandas as pd
import base64
import httpx
from streamlit_extras.switch_page_button import switch_page
import asyncio
from st_pages import Page

API_URL = "http://localhost:8000"


def get_all_pages():
    all_pages = [
        Page("Home.py", "Home"),
        Page("pages/1_Upload_Images.py", "Uplaod Images"),
        Page("pages/2_Edit_Images.py", "Edit Images"),
        Page("pages/3_View_Uploaded_Images.py", "View Uploaded Images"),
        Page("pages/4_Find_Duplicates.py", "Find Duplicates"),
    ]
    return all_pages


def load_data_for_df():
    with st.spinner("Loading Data..."):
        images_data = asyncio.run(get_images_data("images/data/"))
        if images_data:
            df = create_db_df(images_data)
            return df
        else:
            return None


def load_data_for_plot():
    with st.spinner("Loading Data..."):
        images_data = asyncio.run(get_images_data("images/plot/"))
        return images_data


def load_data_for_map():
    with st.spinner("Loading Data..."):
        images_data = asyncio.run(get_images_data("images/map/"))
        df = create_db_df(images_data)
        return df


def get_duplicates_async():
    with st.spinner("Loading Data..."):
        dup_images = asyncio.run(get_images_data("images/find_duplicates/"))
        return dup_images


def get_images_names():
    with st.spinner("Loading Data..."):
        image_names = asyncio.run(get_images_data("images/names/"))
        return image_names


def get_image_for_edit(image_name: str):
    with st.spinner("Loading Data..."):
        image = asyncio.run(get_images_data(f"images/edit/{image_name}/"))
        return image


async def get_images_data(endpoint: str):
    headers = {"Authorization": f"Bearer {st.session_state['user']['access_token']}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/{endpoint}", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to retrieve images.")
            return []


def create_db_df(images_data: list):
    df = pd.DataFrame(images_data)
    return df


def decode_base64(encoded_str: str) -> bytes:
    if encoded_str is not None:
        return base64.b64decode(encoded_str.encode("ascii"))
    return b""


def encode_base64(byte_array: bytes) -> str:
    return base64.b64encode(byte_array).decode("ascii")


def delete_image_async(image_name: str):
    with st.spinner("Deleting Images..."):
        res = asyncio.run(delete_image(image_name))
        return res


async def delete_image(image_name: str):
    headers = {"Authorization": f"Bearer {st.session_state['user']['access_token']}"}
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{API_URL}/images/name/{image_name}/", headers=headers
        )
        if response.status_code == 204:
            return {"message": f"image with the name: {image_name} deleted"}
        else:
            st.error(f"Failed to delete image: {image_name}")
            return None


def update_image_async(image_id: int, image: dict):
    with st.spinner("Updating Images..."):
        res = asyncio.run(update_image(image_id, image))
        return res


async def update_image(image_id: int, image: dict):
    headers = {"Authorization": f"Bearer {st.session_state['user']['access_token']}"}
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{API_URL}/images/{image_id}/", headers=headers, json=image
        )
        if response.status_code == 202:
            return {"message": f"image with the id: {image_id} updated"}
        else:
            st.error(f"Failed to update id: {image_id}")
            return None


def upload_images_async(uploaded_files: list):
    with st.spinner("Loading Data..."):
        res = asyncio.run(upload_images(uploaded_files))
        return res


async def upload_images(uploaded_files: list):
    files_dict = []
    for uploaded_file in uploaded_files:
        file_bytes = io.BytesIO(uploaded_file.read())
        files_dict.append(
            ("upload_images", (uploaded_file.name, file_bytes, uploaded_file.type))
        )
    headers = {"Authorization": f"Bearer {st.session_state['user']['access_token']}"}
    timeout = 30.0
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            f"{API_URL}/images/", files=files_dict, headers=headers
        )
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
            st.error("Login failed. Please try again.")
    else:
        st.session_state["user"]["logged_in"] = False
        st.session_state["user"][
            "action_status"
        ] = "Login failed. Please check your credentials."
        st.error("Login failed. Please try again.")


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


def calculate_center(df: pd.DataFrame):
    average_latitude = df["latitude"].mean()
    average_longitude = df["longitude"].mean()
    return [average_latitude, average_longitude]


def add_bg_from_local(image_file: str):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: 100% 100%;  
        background-position: fixed;
    }}

    .css-cio0dv.egzxvld1
        {{
            visibility: hidden;
        }}
    </style>


<h1 style='text-align: center;font-size:85px; pointer-events: none; font-weight:bold; color: #2b2a2a; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); background-color: #yourColor;'>
   IMAGE-NATION
</h1>
<p style='text-align: center; font-size:45px; font-weight:bold; pointer-events: none; color: #fba362; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); background-color: #yourColor;'>
    Are You Ready To Re-Explore THE WORLD
</p>




    
    """,
        unsafe_allow_html=True,
    )
