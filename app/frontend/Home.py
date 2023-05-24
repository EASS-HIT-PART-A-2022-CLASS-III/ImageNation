import streamlit as st
import base64

st.set_page_config(page_title="Welcome to IMAGE-NATION", page_icon="🌍")
st.sidebar.title("IMAGE-NATION")


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: 100% 100%;  
        background-position: center;
    }}

    .css-cio0dv.egzxvld1
        {{
            visibility: hidden;
        }}
    </style>

    <h1 style='text-align: center; pointer-events: none;'>
    <span style='color: black;'>Welcome To </span></span><span style='color: green;'>I</span><span style='color: yellow;'>M</span><span style='color: orange;'>A</span><span style='color: red;'>G</span><span style='color: violet;'>E</span><span>-</span><span style='color: indigo;'>N</span><span style='color: blue;'>A</span><span style='color: green;'>T</span><span style='color: yellow;'>I</span><span style='color: orange;'>O</span><span style='color: red;'>N</span><span> 🌍</span>
    </h1>
    <h2 style='text-align: center; pointer-events: none;'>
    <span style='color: black;'>Are you ready to re-explore the world? 🛺</span>
    </h2>
    
    """,
        unsafe_allow_html=True,
    )


add_bg_from_local("backgrond_Image.jpg")

st.markdown("---")
st.write("Welcome to my app!")
st.write("Please navigate to the desired section using the sidebar.")
st.write("Enjoy!")
