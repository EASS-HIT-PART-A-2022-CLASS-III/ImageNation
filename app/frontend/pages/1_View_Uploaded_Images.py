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

st.set_page_config(page_title="IMAGE WATCH", page_icon="🖼️")
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

st.markdown(
    "<h1 style='text-align: center; color: blue;'>View Uploade Image</h1>",
    unsafe_allow_html=True,
)
imageView_radioButton = st.sidebar.radio(
    "View images",
    options=["Show details Table", "Show small images", "Show images on map"],
    index=0,
)


def get_images():
    response = requests.get("http://localhost:8000/images")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to retrieve images.")
        return []


def create_db_df(images_data):
    df = pd.json_normalize(images_data)
    df = df.drop(columns="gps")
    df.columns = [col.replace("gps.", "") for col in df.columns]
    return df


def view_images_content(df):
    with st.spinner('Loading Data Frame please wait...'):
        st.write("This is the details table content.")
        df = df.drop(columns="content")
        column_options = [col for col in df.columns if col != "name"]
        imageDetails_multiSelect = st.multiselect(
            ":red[Select which details to show]",
            options=column_options,
            default=column_options,
        )
        selected_columns = ["name"] + [
            col.replace("gps.", "") for col in imageDetails_multiSelect
        ]
        df.columns = [col.replace("gps.", "") for col in df.columns]
        temp_df = df[selected_columns]
        st.dataframe(temp_df)
    st.success('Data Frame loaded!')


def decode_base64(encoded_str: str) -> bytes:
    if encoded_str is not None:
        return base64.b64decode(encoded_str.encode("ascii"))
    return b""


def display_small_images(images_data):
    instractions_placeholder = st.empty()
    with st.spinner('Loading Images...'):
        warnings = []
        images_per_row = 3
        num_images = len(images_data)
        num_rows = (num_images + images_per_row - 1) // images_per_row
        for row in range(num_rows):
            cols = st.columns(images_per_row)
            for col_index, col in enumerate(cols):
                image_index = row * images_per_row + col_index
                if image_index < num_images:
                    image_data = images_data[image_index]
                    encoded_content = image_data["content"]
                    image_bytes = decode_base64(encoded_content)
                    if image_bytes:
                        try:
                            image = Image.open(io.BytesIO(image_bytes))
                            col.image(
                                image, caption=image_data["name"], use_column_width=True
                            )
                        except:
                            warnings.append(f"Failed to display image: {image_data['name']}")
                            #col.error(f"Failed to display image: {image_data['name']}")
                    else:
                        warnings.append(f"Failed to decode image content: {image_data['name']}")
                        #col.error(f"Failed to decode image content: {image_data['name']}")
        st.success('Images loaded!')
        instractions_placeholder.write(":green[press on the arrows on the top right corner to see the images in full size]")
        if warnings:
            for warning in warnings:
                st.warning(warning)


def calculate_center(df):
    average_latitude = df["latitude"].mean()
    average_longitude = df["longitude"].mean()
    return [average_latitude, average_longitude]

import folium
from folium.plugins import PolyLineTextPath

def process_image(row):
    name = row["name"]
    date = row["date"]
    encoded_content = row.get("content")
    if pd.isnull(encoded_content):
        return f"Skipping image '{name}' due to missing content."
    image_bytes = decode_base64(encoded_content)
    if image_bytes is None:
        return f"Failed to decode image content for '{name}'."
    latitude = row.get("latitude")
    longitude = row.get("longitude")
    if pd.isnull(latitude) or pd.isnull(longitude):
        return f"Skipping image '{name}' due to missing GPS coordinates."

    try:
        img = Image.open(io.BytesIO(image_bytes))
    except:
        return f"Failed to open image '{name}'."

    size = (40, 40)  # Increase the size of the mask
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    img.thumbnail(size, Image.ANTIALIAS)
    img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    img.putalpha(mask)
    
    output = io.BytesIO()
    img.save(output, format="PNG")
    icon_data = base64.b64encode(output.getvalue()).decode()
    icon_url = f"data:image/png;base64,{icon_data}"
    
    # Use the desired icon size
    icon = folium.CustomIcon(icon_url, icon_size=(40, 40))


    marker = folium.Marker(
        location=[latitude, longitude],
        icon=icon,
    )

    popup_html = f'<p style="text-align:center;"><b>{name,date}</b><br><img src="data:image/jpeg;base64,{encoded_content}" style="max-height:200px; max-width:200px;"></p>'

    folium.Popup(popup_html, max_width=300).add_to(marker)

    return marker, name

def plot_images_on_map(df):
    with st.spinner('Loading Map please wait...'):
        warnings = []
        center = calculate_center(df)
        if center is None:
            st.error("No GPS data available in images.")
            return
        m = folium.Map(
            location=center,
            zoom_start=3,
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri",
        )
        marker_cluster = MarkerCluster().add_to(m)
        results = df.apply(process_image, axis=1)
        for result in results:
            if isinstance(result, str):
                warnings.append(result)
            else:
                marker, name = result
                marker.add_to(marker_cluster)
        folium_static(m)
    st.success('Map loaded!')
    if warnings:
            for warning in warnings:
                st.warning(warning)
    



images_data = get_images()
df = create_db_df(images_data)
if imageView_radioButton == "Show details Table":
    view_images_content(df)
elif imageView_radioButton == "Show small images":
    display_small_images(images_data)
elif imageView_radioButton == "Show images on map":
    plot_images_on_map(df)
    
