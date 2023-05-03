import streamlit as st
import requests
import folium
from folium.plugins import MarkerCluster
from io import BytesIO
from PIL import Image

# Define the URL for the FastAPI backend
BACKEND_URL = 'http://localhost:8000'

@st.cache(allow_output_mutation=True)
def get_map():
    # Create a folium map object centered on a specific location
    m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)
    return m

# Get the folium map object
m = get_map()

# Create a marker cluster layer to group the markers together
marker_cluster = MarkerCluster().add_to(m)

# Define a function to process uploaded images and add markers to the map
def process_uploaded_images(images):
    for image in images:
        # Read the image data from the uploaded file
        image_data = BytesIO(image.read())
        img = Image.open(image_data)

        # Extract the GPS coordinates from the image metadata
        lat, lon = img.getexif()[34853][:2]

        # Resize the image to a smaller size for use as a marker icon
        size = (64, 64)
        img.thumbnail(size)

        # Convert the image to a data URL for use as the marker icon
        img_data = BytesIO()
        img.save(img_data, format='PNG')
        img_data.seek(0)
        data_url = 'data:image/png;base64,' + img_data.read().encode('base64').replace('\n', '')

        # Create a folium marker for the image location, using the image as the icon
        marker = folium.Marker(location=[lat, lon], icon=folium.features.CustomIcon(data_url, icon_size=(64, 64)))

        # Add the marker to the marker cluster layer on the map
        marker.add_to(marker_cluster)

# Define the Streamlit app UI
st.title('Image Map')
uploaded_images = st.file_uploader('Upload images', accept_multiple_files=True)

# If images have been uploaded, process them and add markers to the map
if uploaded_images:
    process_uploaded_images(uploaded_images)

    # Send the uploaded images to the FastAPI backend
    files = {'file': [image for image in uploaded_images]}
    response = requests.post(f'{BACKEND_URL}/find_duplicates', files=files)

    # Display the response from the FastAPI backend
    st.write(response.json())

# Display the folium map object
st.markdown('<h2>Map</h2>', unsafe_allow_html=True)
st.markdown('<div id="map"></div>', unsafe_allow_html=True)
folium_static(m)