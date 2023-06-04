import streamlit as st
from utils import upload_images_async


st.set_page_config(page_title="Image Uploadung", page_icon="📮", layout="wide", layout="wide")
st.markdown(
    """
    <style>
    .css-cio0dv.egzxvld1
    {
        visibility: hidden;
    }
    </style>

    <h1 style='text-align: center; color: blue;'>Image Uploader</h1>
    """,
    unsafe_allow_html=True,
)
st.markdown("---")
st.header("Upload images to the Database")

col1, col2 = st.columns([3, 1])

uploaded_files = col1.file_uploader(
    "Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)

upload_button = col2.button("Upload Images")

if upload_button:
    try:
        if not uploaded_files:
            st.warning("Please upload at least one image.")
        else:
            response = upload_images_async(uploaded_files)
            if response.status_code == 201:
                col2.image("boratGreat.gif", use_column_width=True)
                col1.success(
                    f"Successfully uploaded {len(uploaded_files)} images, see below the uploaded images."
                )
                cols = st.columns(3)
                for i, file in enumerate(uploaded_files):
                    cols[i % 3].image(file, width=150, caption=file.name)
            else:
                st.error("Failed to upload images.")
    except Exception as e:
        st.error(f"Failed to upload images. Error: {e}")
