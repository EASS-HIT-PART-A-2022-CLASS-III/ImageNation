import streamlit as st
from datetime import datetime, date, time
import folium
from streamlit_folium import folium_static
import numpy as np
from PIL import Image
import io
from utils import (
    get_images_names,
    decode_base64,
    get_image_for_edit,
    update_image_async,
)
from streamlit_extras.no_default_selectbox import selectbox


st.set_page_config(page_title="IMAGE EDIT'S", page_icon="🛠️", layout="wide")

st.markdown(
    """
    <style>
    .css-cio0dv.egzxvld1
    {
        visibility: hidden;
    }
    </style>
    <h1 style='text-align: center;font-size:50px; color: white;'>Edit Image Data</h1>
    """,
    unsafe_allow_html=True,
)

st.write("---")


def edit_image_data(images_names):
    col1, col2, _ = st.columns([1, 1, 2])
    select_placeholder = col1.empty()
    select_placeholder.write(":red[please select image from the list]")
    with col2:
        result = selectbox(
            "Select Image",
            images_names,
            no_selection_label="<None>",
            label_visibility="collapsed",
        )
    st.write("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    edit_placeholder = col1.empty()
    image_name_placeholder = col2.empty()
    image_placeholder = col3.empty()
    col2.subheader("")
    col2.write("")
    col2.write("")
    col2.write("")
    col2.write("")
    if result:
        select_placeholder.write(":green[Image selected]")
        edit_placeholder.subheader(f"Editing:")
        image_name_placeholder.subheader(f"{result}")
        image_for_edit = get_image_for_edit(result)
        image_bytes = decode_base64(image_for_edit["content"])
        if image_bytes:
            try:
                image = Image.open(io.BytesIO(image_bytes))
                caption = f"{image_for_edit['name']}"
                image_placeholder.image(image, caption=caption, width=300)
            except:
                pass
        edit_name = col1.text_input("Image Name", image_for_edit["name"])
        if image_for_edit["date"]:
            selected_datetime = datetime.strptime(
                image_for_edit["date"], "%Y-%m-%dT%H:%M:%S"
            )
            selected_date = selected_datetime.date()
            selected_time = selected_datetime.time()
        else:
            selected_date = date(2000, 1, 1)
            selected_time = time(12, 0, 0)
        new_date = col1.date_input("Image Date", selected_date)
        new_time = col2.time_input("Image Time", selected_time)
        if image_for_edit["latitude"] and image_for_edit["longitude"]:
            new_latitude = col1.number_input(
                "Image Latitude", value=image_for_edit["latitude"]
            )
            new_longitude = col2.number_input(
                "Image Longitude", value=image_for_edit["longitude"]
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
            max_zoom=18,
            min_zoom=2,
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri",
        )
        marker = folium.Marker(
            location=[lat, lon],
            draggable=False,
            icon=folium.Icon(icon="camera", color="red"),
        ).add_to(m)
        folium_static(m)
        with st.form("Edit Image Data", clear_on_submit=True):
            st.write(edit_name)
            st.write(new_date)
            st.write(new_time)
            st.write(marker.location[0])
            st.write(marker.location[1])

            form_state = st.form_submit_button("Submit")
            if form_state:
                if (
                    edit_name == image_for_edit["name"]
                    and new_date == selected_date
                    and new_time == selected_time
                    and marker.location[0] == image_for_edit["latitude"]
                    and marker.location[1] == image_for_edit["longitude"]
                ):
                    st.warning("No changes were made to the image data.")
                else:
                    new_datetime = datetime.combine(new_date, new_time).isoformat()
                    new_gps = None
                    if (
                        marker.location[0] != image_for_edit["latitude"]
                        or marker.location[1] != image_for_edit["longitude"]
                    ):
                        new_gps = {
                            "latitude": marker.location[0],
                            "longitude": marker.location[1],
                            "altitude": image_for_edit["altitude"],
                            "direction": image_for_edit["direction"],
                        }
                    new_image_data = {
                        "name": edit_name,
                        "date": new_datetime,
                        "gps": new_gps,
                    }
                    id = image_for_edit["id"]
                    print(id)
                    res = update_image_async(id, new_image_data)
                    if res:
                        st.success("Image data updated successfully.")
                    else:
                        st.error("Error updating image data.")


images_names = get_images_names()
edit_image_data(images_names)
