import streamlit as st
from utils import get_duplicates, delete_image


st.set_page_config(page_title="Find Duplicates", page_icon="👯‍♀️")

st.markdown(
    """
    <style>
    .css-cio0dv.egzxvld1
    {
        visibility: hidden;
    }
    </style>

    <h1 style='text-align: center; color: blue;'>Find Duplicates</h1>
    """,
    unsafe_allow_html=True,
)
st.markdown("---")


get_duplicates_button = st.button("Press to find Duplicates")
if get_duplicates_button:
    with st.spinner("Getting duplicates Images..."):
        st.session_state.duplicates_images = get_duplicates()
        show_duplicates_list = True
else:
    show_duplicates_list = False

if "duplicates_images" in st.session_state:
    if not st.session_state.duplicates_images:
        st.warning("No duplicate images found.")
    else:
        if show_duplicates_list:
            st.markdown("### This is the list of duplicate images in the Data Base:")
        checkbox_status = {}
        for group in st.session_state.duplicates_images.values():
            for image in group:
                checkbox_status[image] = st.checkbox(f"Select {image}", value=True)
        selected_images = [
            image for image, is_selected in checkbox_status.items() if is_selected
        ]
        if selected_images:
            delete_button = st.button("Delete selected images")
            if delete_button:
                for image in selected_images:
                    delete_result = delete_image(image)
                    if delete_result is not None:
                        st.success(delete_result["message"])
                for image in selected_images:
                    checkbox_status[image] = False
                st.session_state.duplicates_images = [
                    image
                    for image in st.session_state.duplicates_images
                    if checkbox_status.get(image, False)
                ]
        else:
            st.warning("No images")
