import streamlit as st
import pandas as pd

################removing streamlit buttom-logo
st.markdown("""
<style>
.css-cio0dv.egzxvld1
{
    visibility: hidden;
}
</style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: red;'>Edit Image Data</h1>", unsafe_allow_html=True)
with st.form("Edit Image Data", clear_on_submit=True):
    image_name = st.text_input("Image Name")
    col1, col2 = st.columns(2)
    col1.date_input("Image Date")
    col2.time_input("Image Time")
    form_state = st.form_submit_button("Submit")
    if form_state:
        if image_name == "" and col1.value is None and col2.value is None:
            st.warning("No changes were made to the image data.")
        else:
            st.success("Successfully edited image data.")



###process image date
# edited_date = image_date.strftime("%Y-%m-%d")
# st.header("Edited Image Time")
# image_time = st.time_input("Image Time")
# edited_time = image_time.strftime("%H:%M:%S")
# edited_date_time = edited_date + " " + edited_time

###edit image gps by choosing location on map
st.header("Edit Image GPS")
st.subheader("Choose location on map")
st.map()

