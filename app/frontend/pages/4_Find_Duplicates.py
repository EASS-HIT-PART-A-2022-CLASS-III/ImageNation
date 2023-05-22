import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from folium.features import CustomIcon
import io
from PIL import Image, ImageOps, ImageDraw
import base64
import hashlib
import sys
sys.path.append("..")
from models import ImageModel
from PIL import UnidentifiedImageError
from concurrent.futures import ThreadPoolExecutor
import folium
from folium.plugins import PolyLineTextPath
from PIL import Image
import io



st.set_page_config(page_title="Find Duplicates", page_icon="👯‍♀️")
################removing streamlit buttom-logo
st.markdown(
    """
    <style>
    .css-cio0dv.egzxvld1
    {
        visibility: hidden;
    }
    </style>

    <h1 style='text-align: center; color: blue;'>Find Duplicates</h1>
    """,
    unsafe_allow_html=True,
)

def get_images():
    response = requests.get("http://localhost:8000/images")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to retrieve images.")
        return []
    
def get_duplicates():
    response = requests.get("http://localhost:8000/findDuplicateImages")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to retrieve images.")
        return []