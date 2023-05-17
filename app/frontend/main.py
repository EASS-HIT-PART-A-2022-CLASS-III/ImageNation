import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import io
from PIL import Image
import base64
import hashlib
import sys
sys.path.append('..')
from models import ImageModel


st.title("Upload Images")

uploaded_files = st.file_uploader("Choose images...", type=["jpg", "png"], accept_multiple_files=True)
if uploaded_files:
    files_dict = []
    for uploaded_file in uploaded_files:
        file_bytes = io.BytesIO(uploaded_file.read())
        files_dict.append(("images", (uploaded_file.name, file_bytes, uploaded_file.type)))
    response = requests.post(
        "http://localhost:8000/images/",
        files=files_dict,
    )
    if response.status_code == 201:
        st.success("Successfully uploaded images.")
    else:
        st.error("Failed to upload images.")

# def get_images():
#     response = requests.get("http://localhost:8000/images")
#     if response.status_code == 200:
#         return response.json()
#     else:
#         st.error("Failed to retrieve images.")
#         return []


# def plot_images_on_map(images):
#     # Create a folium map
#     m = folium.Map(
#         location=[45.523, -122.675],
#         zoom_start=13,
#         tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
#         attr='Esri'
#     )

#     # Add marker cluster
#     marker_cluster = MarkerCluster().add_to(m)

#     # Iterate over images and plot them on the map
#     for image in images:
#         name = image["name"]
#         latitude = image["gps"]["latitude"]
#         longitude = image["gps"]["longitude"]
#         popup_text = f"Image: {name}"

#         # Get the image content from the server
#         response = requests.get(f"http://localhost:8000/images/{name}")
#         if response.status_code == 200:
#             image_data = response.json()["image"]["content"]

#             # Decode and resize the image
#             image_bytes = io.BytesIO(base64.b64decode(image_data))
#             img = Image.open(image_bytes)
#             img.thumbnail((100, 100))  # Resize the image to a smaller size

#             # Add the image as an HTML element in the popup
#             popup_html = f'<img src="data:image/jpeg;base64,{base64.b64encode(img.tobytes()).decode("ascii")}">'
#             folium.Marker(
#                 location=[latitude, longitude],
#                 popup=folium.Popup(popup_html, max_width=300),
#                 icon=folium.Icon(icon="cloud"),
#             ).add_to(marker_cluster)

#     # Display the map
#     folium_static(m)

# images = get_images()

# # Plot the images on the map
# plot_images_on_map(images)



# # # create a folium map
# # m = folium.Map(location=[45.523, -122.675], 
# #                zoom_start=13, 
# #                tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
# #                attr='Esri')

# # # add marker cluster
# # marker_cluster = MarkerCluster().add_to(m)

# # folium.Marker(
# #     location=[45.51, -122.68],
# #     popup="Add popup text here.",
# #     icon=folium.Icon(icon="cloud"),
# # ).add_to(marker_cluster)

# # folium.Marker(
# #     location=[45.513, -122.66],
# #     popup="Add popup text here.",
# #     icon=folium.Icon(color="green"),
# # ).add_to(marker_cluster)

# # folium.Marker(
# #     location=[45.512, -122.65],
# #     popup="Add popup text here.",
# #     icon=folium.Icon(color="red", icon="info-sign"),
# # ).add_to(marker_cluster)

# # # display map
# # folium_static(m)