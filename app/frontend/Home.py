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

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover;
        background-position: center;
    }}

    .css-cio0dv.egzxvld1
        {{
            visibility: hidden;
        }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('backgrond_Image.jpg')    


################Welcome To App
st.title("Welcom To :blue[IMAGE-NATION] 🌍")
st.subheader("Are you ready to re-explore the world? 🛺")
st.markdown("---")
st.write("Welcome to my app!")
st.write("This is the landing page.")
st.write("Please navigate to the desired section using the sidebar.")
st.write("Enjoy!")
#st.image('backgrond_Image.jpg')



