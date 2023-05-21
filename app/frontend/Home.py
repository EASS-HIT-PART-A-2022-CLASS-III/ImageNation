import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import io
from PIL import Image
import base64
import hashlib
import sys

sys.path.append("..")
from models import ImageModel

st.set_page_config(page_title="Welcome to IMAGE-NATION", page_icon="🌍")
################removing streamlit buttom-logo
st.markdown(
    """
<style>
.css-cio0dv.egzxvld1
{
    visibility: hidden;
}
</style>
    """,
    unsafe_allow_html=True,
)
################Welcome To App
st.title("ImagePlotter")
st.header("Upload images to plot them on a map.")
st.markdown("---")


################Upload images


uploaded_files = st.file_uploader(
    "Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)
with st.spinner("Uploading Images..."):
    if uploaded_files:
        files_dict = []
        for uploaded_file in uploaded_files:
            file_bytes = io.BytesIO(uploaded_file.read())
            files_dict.append(
                ("images", (uploaded_file.name, file_bytes, uploaded_file.type))
            )
        response = requests.post(
            "http://localhost:8000/images/",
            files=files_dict,
        )
        if response.status_code == 201:
            st.success("Successfully uploaded images.")
        else:
            st.error("Failed to upload images.")