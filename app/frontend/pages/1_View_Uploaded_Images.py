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


################removing streamlit buttom-logo
st.markdown("""
<style>
.css-cio0dv.egzxvld1
{
    visibility: hidden;
}
</style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: blue;'>View Uploade Image</h1>", unsafe_allow_html=True)

def get_images():
    response = requests.get("http://localhost:8000/images")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to retrieve images.")
        return []

# Get images data from the back end
images_data = get_images()
df = pd.json_normalize(images_data)
df = df.drop(columns=['content', 'gps'])
column_options = [col.replace('gps.', '') for col in df.columns if col != 'name']
imageDetails_multiSelect = st.multiselect("Select which details to show", options=column_options, default=column_options)
selected_columns = ['name'] + [col.replace('gps.', '') for col in imageDetails_multiSelect]
df.columns = [col.replace('gps.', '') for col in df.columns]
df = df[selected_columns]
st.dataframe(df)

################radio button to see uploaded images
imageView_radioButton = st.sidebar.radio("View images",options=["Show details Table", "Show small images", "Show images on map"] , on_change=None, index=0)


