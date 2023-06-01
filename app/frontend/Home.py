import streamlit as st
import base64
import httpx
import asyncio

API_URL = "http://localhost:8000"


st.set_page_config(page_title="Welcome to IMAGE-NATION", page_icon="🌍")


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
if "user" not in st.session_state:
    st.session_state["user"] = {"name": None, "logged_in": False, "action_status": None}


async def login(email: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/login/", data={"username": email, "password": password}
        )
        data = response.json()

    if response.status_code == 200:
        st.session_state["user"]["name"] = data["user_name"]
        st.session_state["user"]["logged_in"] = True
        st.session_state["user"]["action_status"] = "Login Successful"
    else:
        st.session_state["user"]["logged_in"] = False
        st.session_state["user"]["action_status"] = "Login Failed"


async def signup(name: str, email: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/users/",
            json={"name": name, "email": email, "password": password},
        )
    if response.status_code == 201:
        st.session_state.logged_in = True
        if email and password:
            await login(email, password)
            st.session_state["user"]["action_status"] = "Signup Successful"
    else:
        st.session_state.logged_in = False
        st.session_state["user"]["action_status"] = "Signup Failed"


def logout():
    st.session_state["user"] = {
        "name": None,
        "logged_in": False,
        "action_status": "Logout Successful",
    }


if st.session_state["user"]["logged_in"]:
    # User is logged in, display your main app
    st.sidebar.title(f"Logged in as: {st.session_state['user']['name']}")
    st.write(f"Hello, {st.session_state['user']['name']}!")
    if st.button("Log Out"):
        logout()


else:
    # User is not logged in, display login and sign-up forms
    form_type = st.radio("Choose Form Type", ["Login", "Sign Up"], horizontal=True)

    with st.form(key="my_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if form_type == "Login":
            submit_button = st.form_submit_button(label="Log In")
            if submit_button:
                asyncio.run(login(email, password))
        elif form_type == "Sign Up":
            name = st.text_input("Name")
            submit_button = st.form_submit_button(label="Sign Up")
            if submit_button:
                asyncio.run(signup(name, email, password))

    # Action status message
    if st.session_state["user"]["action_status"]:
        st.write(st.session_state["user"]["action_status"])
