import base64
import json
import requests
import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import folium
from streamlit_folium import folium_static
import streamlit as st
import numpy as np
from geopy import Point
from geopy.geocoders import Nominatim
import base64
from PIL import Image
import io
import sys
from app.models import GPS, ImageModel
from app.utils import get_images, create_db_df, decode_base64, get_country_name


st.set_page_config(page_title="IMAGE EDIT'S", page_icon="🛠️")

################removing streamlit buttom-logo
st.markdown(
    """
    <style>
    .css-cio0dv.egzxvld1
    {
        visibility: hidden;
    }
    </style>

    <h1 style='text-align: center; color: red;'>Edit Image Data</h1>
    """,
    unsafe_allow_html=True,
)


images_data = get_images()
df = create_db_df(images_data)


###################################################################################
def edit_image_data(df):
    image_names = df["name"].unique()
    image_names = np.insert(image_names, 0, "Please select an image")
    selected_image_name = st.selectbox("Select Image", image_names)
    edit_placeholder = st.empty()

    if selected_image_name and selected_image_name != "Please select an image":
        edit_placeholder.subheader(f"Editing {selected_image_name}")
        selected_image_data = df[df["name"] == selected_image_name].iloc[0]

        encoded_content = selected_image_data["content"]

        image_bytes = decode_base64(encoded_content)
        if image_bytes:
            try:
                image = Image.open(io.BytesIO(image_bytes))
                caption = f"{selected_image_data['name']} - Image Location: {selected_image_data['country']}"
                col1, col2, col3 = st.columns(3)
                col2.image(image, caption=caption, use_column_width=True)
            except:
                pass

        image_name_input = st.text_input("Image Name", selected_image_data["name"])
        col1, col2 = st.columns(2)
        if selected_image_data["date"]:
            selected_datetime = datetime.strptime(
                selected_image_data["date"], "%Y-%m-%dT%H:%M:%S"
            )
            selected_date = selected_datetime.date()
            selected_time = selected_datetime.time()
        else:
            selected_date = date(2000, 1, 1)
            selected_time = time(12, 0, 0)
        new_date = col1.date_input("Image Date", selected_date)
        new_time = col2.time_input("Image Time", selected_time)
        if selected_image_data["latitude"] and selected_image_data["longitude"]:
            new_latitude = col1.number_input(
                "Image Latitude", value=selected_image_data["latitude"]
            )
            new_longitude = col2.number_input(
                "Image Longitude", value=selected_image_data["longitude"]
            )
        else:
            new_latitude = col1.number_input("Image Latitude", value=0.0)
            new_longitude = col2.number_input("Image Longitude", value=0.0)
        zoom_level = 13

        lat = float(np.nan_to_num(new_latitude, nan=0))
        lon = float(np.nan_to_num(new_longitude, nan=0))
        m = folium.Map(
            location=[lat, lon],
            zoom_start=zoom_level,
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri",
        )
        marker = folium.Marker(
            location=[lat, lon],
            draggable=False,
            icon=folium.Icon(icon="camera", color="red"),
        ).add_to(m)
        folium_static(m)

        # Update the latitude and longitude inputs with the new values when the form is submitted
        with st.form("Edit Image Data", clear_on_submit=True):
            st.write(image_name_input)
            st.write(new_date)
            st.write(new_time)
            st.write(marker.location[0])
            st.write(marker.location[1])

            form_state = st.form_submit_button("Submit")

            if form_state:
                if (
                    image_name_input == selected_image_data["name"]
                    and new_date == selected_date
                    and new_time == selected_time
                    and marker.location[0] == selected_image_data["latitude"]
                    and marker.location[1] == selected_image_data["longitude"]
                ):
                    st.warning("No changes were made to the image data.")
                else:
                    new_datetime = datetime.combine(new_date, new_time)
                    if (
                        marker.location[0] != selected_image_data["latitude"]
                        or marker.location[1] != selected_image_data["longitude"]
                    ):
                        new_gps = GPS(
                            latitude=marker.location[0],
                            longitude=marker.location[1],
                            altitude=selected_image_data["altitude"],
                            country=get_country_name(
                                marker.location[0], marker.location[1]
                            ),
                        )
                    else:
                        new_gps = None
                    new_image_data = ImageModel(
                        name=image_name_input,
                        date=new_datetime,
                        gps=new_gps,
                    )
                    response = requests.patch(
                        f"http://localhost:8000/patchImage/{selected_image_data['name']}",
                        data=new_image_data.json(),
                    )
                    if response.status_code == 202:
                        st.success("Successfully edited image data.")
                    else:
                        st.error("Failed to edit image data.")


edit_image_data(df)
