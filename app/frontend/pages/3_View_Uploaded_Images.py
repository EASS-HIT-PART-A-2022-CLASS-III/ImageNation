import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import io
from PIL import Image
from app.frontend.utils import get_images, create_db_df, decode_base64
import folium
from PIL import Image
import io


st.set_page_config(page_title="IMAGE WATCH", page_icon="🖼️")
st.markdown(
    """
    <style>
    .css-cio0dv.egzxvld1
    {
        visibility: hidden;
    }
    </style>

    <h1 style='text-align: center; color: blue;'>View Uploade Image 📽️</h1>
    """,
    unsafe_allow_html=True,
)

imageView_radioButton = st.sidebar.radio(
    "View images",
    options=["Show details Table", "Show small images", "Show images on map"],
    index=0,
)


def view_images_content(df):
    with st.spinner("Loading Data Frame please wait..."):
        st.write("This is the details table content.")
        df = df.drop(columns=["content", "smallRoundContent"])
        column_options = [col for col in df.columns if col != "name"]
        imageDetails_multiSelect = st.multiselect(
            ":red[Select which details to show]",
            options=column_options,
            default=column_options,
        )
        st.write("press artibute name to sort by it.")
        selected_columns = ["name"] + [
            col.replace("gps.", "") for col in imageDetails_multiSelect
        ]
        df.columns = [col.replace("gps.", "") for col in df.columns]
        temp_df = df[selected_columns]
        st.dataframe(temp_df)
    st.success("Data Frame loaded!")


def display_small_images(images_data):
    instractions_placeholder = st.empty()
    with st.spinner("Loading Images..."):
        warnings = []
        cols = st.columns(3)
        for i, image_data in enumerate(images_data):
            encoded_content = image_data["content"]
            image_bytes = decode_base64(encoded_content)
            if image_bytes:
                try:
                    image = Image.open(io.BytesIO(image_bytes))
                    cols[i % 3].image(
                        image, caption=image_data["name"], use_column_width=True
                    )
                except:
                    warnings.append(f"Failed to display image: {image_data['name']}")
            else:
                warnings.append(f"Failed to decode image content: {image_data['name']}")
        st.success("Images loaded!")
        instractions_placeholder.write(
            ":green[press on the arrows on the top right corner to see the images in full size]"
        )
        if warnings:
            for warning in warnings:
                st.warning(warning)


def calculate_center(df):
    average_latitude = df["latitude"].mean()
    average_longitude = df["longitude"].mean()
    return [average_latitude, average_longitude]


def process_image(row):
    name = row["name"]
    date = row["date"]
    encoded_small_content = row.get("smallRoundContent")
    if pd.isnull(encoded_small_content):
        return f"Skipping image '{name}' due to missing small content."
    encoded_content = row.get("content")
    if pd.isnull(encoded_content):
        return f"Skipping image '{name}' due to missing content."
    latitude = row.get("latitude")
    longitude = row.get("longitude")
    if pd.isnull(latitude) or pd.isnull(longitude):
        return f"Skipping image '{name}' due to missing GPS coordinates."
    icon_url = f"data:image/png;base64,{encoded_small_content}"
    icon = folium.CustomIcon(icon_url, icon_size=(40, 40))
    popup_html = f'<p style="text-align:center;"><b>{name}, {date}</b><br><img src="data:image/jpeg;base64,{encoded_content}" style="max-height:200px; max-width:200px;"></p>'
    marker = folium.Marker(
        location=[latitude, longitude],
        icon=icon,
        popup=folium.Popup(popup_html, max_width=300),
    )

    return marker, name


def plot_images_on_map(df):
    with st.spinner("Loading Map please wait..."):
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
        folium_static(m, width=900, height=600)
    st.success("Map loaded!")
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
