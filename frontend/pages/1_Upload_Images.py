import streamlit as st
from utils import upload_images_async


st.set_page_config(page_title="Image Uploadung", page_icon="📮", layout="wide")
st.markdown(
    """
    <style>
    .css-cio0dv.egzxvld1
    {
        visibility: hidden;
    }
    </style>

    <h1 style='text-align: center;font-size:50px; color: white;'>Image Uploader</h1>

    """,
    unsafe_allow_html=True,
)
st.markdown("---")
st.header("Upload images to the Database")

col1, col2 = st.columns([3, 1])

uploaded_files = col1.file_uploader(
    "Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)
image_placeholder = col2.empty()
col1, col2, _ = st.columns([1, 2, 1])
upload_button = col1.button("Upload Images")


if upload_button:
    try:
        if not uploaded_files:
            st.warning("Please upload at least one image.")
        else:
            response = upload_images_async(uploaded_files)
            if response.status_code == 201:
                response_json = response.json()
                success_count = response_json.get("success", 0)
                error_messages = response_json.get("errors", [])
                successful_uploads = response_json.get("uploaded_images", [])
                if success_count != 0:
                    image_placeholder.image("boratGreat.gif", use_column_width=True)
                    col2.success(
                        f"{success_count} Images upload successfully, See below the uploaded images."
                    )
                else:
                    image_placeholder.image("boratNo.gif", use_column_width=True)
                    st.error("Failed to upload images.")
                if error_messages:
                    with col2.expander(
                        ":red[Expend to see unsuccessfull uploads images]"
                    ):
                        for error in error_messages:
                            st.warning(error)
                cols = st.columns(3)
                for i, file in enumerate(uploaded_files):
                    if file.name in successful_uploads:
                        cols[i % 3].image(file, width=150, caption=file.name)
            else:
                st.error("Failed to upload images.")
                image_placeholder.image("boratNo.gif", use_column_width=True)
    except Exception as e:
        st.error(f"Failed to upload images. Error: {e}")
