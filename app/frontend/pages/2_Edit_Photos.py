import base64
import requests
import streamlit as st
import pandas as pd
import datetime
import folium
from streamlit_folium import folium_static
import datetime
import streamlit as st
import numpy as np
from geopy import Point
from geopy.geocoders import Nominatim
import base64
from PIL import Image
import io




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
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='text-align: center; color: red;'>Edit Image Data</h1>",
    unsafe_allow_html=True,
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

images_data = get_images()
df = create_db_df(images_data)

def decode_base64(encoded_str: str) -> bytes:
    if encoded_str is not None:
        return base64.b64decode(encoded_str.encode("ascii"))
    return b""


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
                caption = selected_image_data["name"] + " " + selected_image_data["country"]
                st.image(
                image, caption=caption , use_column_width=True
                  )
            except:
                pass

        image_name_input = st.text_input("Image Name", selected_image_data["name"])
        col1, col2 = st.columns(2)
        selected_date = datetime.datetime.strptime(selected_image_data["date"], "%Y-%m-%dT%H:%M:%S").date()
        selected_time = datetime.datetime.strptime(selected_image_data["date"], "%Y-%m-%dT%H:%M:%S").time()
        new_date = col1.date_input("Image Date", selected_date)
        new_time = col2.time_input("Image Time", selected_time)
        new_latitude = col1.number_input("Image Latitude", value=selected_image_data["latitude"])
        new_longitude = col2.number_input("Image Longitude", value=selected_image_data["longitude"])
        zoom_level = 13
        if new_latitude and new_longitude:
            lat = float(np.nan_to_num(new_latitude, nan=0))
            lon = float(np.nan_to_num(new_longitude, nan=0))
            m = folium.Map(location=[lat, lon],
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
                ):
                    st.warning("No changes were made to the image data.")
                else:
                    st.success("Successfully edited image data.")
        
edit_image_data(df)