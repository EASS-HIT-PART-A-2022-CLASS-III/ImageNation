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

st.set_page_config(page_title="Image Uploadung", page_icon="📮")
st.markdown(
    """
    <style>
    .css-cio0dv.egzxvld1
    {
        visibility: hidden;
    }
    </style>

    <h1 style='text-align: center; color: blue;'>Image Uploader</h1>
    """,
    unsafe_allow_html=True,
)

################Welcome To App
################Upload images
st.header("Upload images to the Database")
st.markdown("---")

col1, col2 = st.columns(2)
uploaded_files = col1.file_uploader(
    "Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)



upload_button = col1.button("Upload Images")

if upload_button:
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
                col2.image('great_succes.gif', use_column_width=True)
                st.success(f"Successfully uploaded {len(uploaded_files)} images")
                cols = st.columns(len(uploaded_files))
                for i, file in enumerate(uploaded_files):
                    cols[i].image(file, width=150)
                
            else:
                st.error("Failed to upload images.")