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


def prepare_columns():
    col1, col2, col3 = st.columns([1, 1, 2])
    image_placeholder = col3.empty()
    return col1, col2, col3, image_placeholder


def prepare_input_values(image_for_edit):
    selected_datetime = (
        datetime.strptime(image_for_edit["date"], "%Y-%m-%dT%H:%M:%S")
        if image_for_edit["date"]
        else None
    )
    selected_date = selected_datetime.date() if selected_datetime else date(2000, 1, 1)
    selected_time = selected_datetime.time() if selected_datetime else time(12, 0, 0)
    image_latitude = image_for_edit["latitude"] if image_for_edit["latitude"] else 0.0
    image_longitude = (
        image_for_edit["longitude"] if image_for_edit["longitude"] else 0.0
    )
    return selected_date, selected_time, image_latitude, image_longitude


def setup_map(new_latitude, new_longitude, zoom_level=13):
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
    return m, marker


def update_image(image_for_edit, edit_name, new_date, new_time, marker):
    new_datetime = datetime.combine(new_date, new_time).isoformat()
    new_gps = (
        {
            "latitude": marker.location[0],
            "longitude": marker.location[1],
            "altitude": image_for_edit["altitude"],
            "direction": image_for_edit["direction"],
        }
        if (
            marker.location[0] != image_for_edit["latitude"]
            or marker.location[1] != image_for_edit["longitude"]
        )
        else None
    )
    new_image_data = {
        "name": edit_name,
        "date": new_datetime,
        "gps": new_gps,
    }
    id = image_for_edit["id"]
    res = update_image_async(id, new_image_data)
    return res


def edit_image_data(images_names):
    col11, col22, col3, _ = st.columns([1, 1, 1, 1])
    with col11:
        select_placeholder = col11.empty()
        select_placeholder.write(":red[Please select image]")
    with col22:
        result = selectbox(
            "Select Image",
            images_names,
            no_selection_label="<None>",
            label_visibility="collapsed",
        )

    if result:
        select_placeholder.write(":green[Image selected]")
        col1, col2, col3, image_placeholder = prepare_columns()
        # image_name_placeholder.subheader(f"{result}")
        image_for_edit = get_image_for_edit(result)
        image_bytes = decode_base64(image_for_edit["content"])
        if image_bytes:
            try:
                image = Image.open(io.BytesIO(image_bytes))
                caption = f"{image_for_edit['name']}"
                image_placeholder.image(image, caption=caption, width=250)
            except:
                pass

        # col1_1, col1_2 = col1.columns(2)
        with col1:
            edit_name = st.text_input("Image Name", image_for_edit["name"])
            (
                selected_date,
                selected_time,
                image_latitude,
                image_longitude,
            ) = prepare_input_values(image_for_edit)
            new_date = st.date_input("Image Date", selected_date)
            new_latitude = st.number_input("Image Latitude", value=image_latitude)

        with col2:
            new_time = st.time_input("Image Time", selected_time)
            new_longitude = st.number_input("Image Longitude", value=image_longitude)

        m, marker = setup_map(new_latitude, new_longitude)
        folium_static(m)

        with col1.form("Edit Image Data", clear_on_submit=True):
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
                    res = update_image(
                        image_for_edit, edit_name, new_date, new_time, marker
                    )
                    if res:
                        st.success("Image data updated successfully.")
                    else:
                        st.error("Error updating image data.")


images_names = get_images_names()
edit_image_data(images_names)
