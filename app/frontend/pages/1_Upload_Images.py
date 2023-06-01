import time
import streamlit as st
from app.frontend.utils import upload_images


st.set_page_config(page_title="Image Uploadung", page_icon="📮")
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

# borat_container = st.container()


col1, col2 = st.columns([3, 1])

uploaded_files = col1.file_uploader(
    "Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)


upload_button = col2.button("Upload Images")

# progress_bar = col2.progress(0)
# for percent_complete in range(100):
#     time.sleep(0.1)
#     progress_bar.progress(percent_complete + 1)

if upload_button:
    with st.spinner("Uploading Images..."):
        if uploaded_files:
            response = upload_images(uploaded_files)
            if response.status_code == 201:
                # borat_container.image("boratGreat.gif")
                col2.image("boratGreat.gif", use_column_width=True)
                # col3.image("boratGreat.gif", use_column_width=True)
                col1.success(
                    f"Successfully uploaded {len(uploaded_files)} images, see below the uploaded images."
                )
                cols = st.columns(3)
                for i, file in enumerate(uploaded_files):
                    cols[i % 3].image(file, width=150, caption=file.name)
            else:
                st.error("Failed to upload images.")
