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
st.markdown("---")
st.write("Welcome to my app!")
st.write("This is the landing page.")
st.write("Please navigate to the desired section using the sidebar.")
st.write("Enjoy!")
