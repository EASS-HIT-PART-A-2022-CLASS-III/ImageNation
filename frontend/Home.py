import streamlit as st
import asyncio
from utils import logout, login, signup, add_bg_from_local, get_all_pages
from st_pages import Page, show_pages


st.set_page_config(page_title="Welcome to IMAGE-NATION", page_icon="🌍", layout="wide")
add_bg_from_local("bg_new.jpg")


home_page = Page("Home.py", "Home")
all_pages = get_all_pages()

# st.markdown("---")
# st.write("Welcome to my app!")


if "user" not in st.session_state:
    st.session_state["user"] = {
        "name": None,
        "logged_in": False,
        "access_token": None,
        "action_status": None,
    }
    st.sidebar.title(f"Please log in or sign up")
    show_pages([home_page])


if st.session_state["user"]["logged_in"]:
    st.sidebar.title(f"Logged in as: {st.session_state['user']['name']}")
    # st.write(f"Hello, {st.session_state['user']['name']}!")
    show_pages(all_pages)
    if st.sidebar.button("Log Out"):
        show_pages([home_page])
        logout()


else:
    form_type = st.sidebar.radio(
        "Choose Form Type", ["Login", "Sign Up"], horizontal=True
    )

    with st.sidebar.form(key="my_form"):
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

    if st.session_state["user"]["action_status"]:
        st.write(st.session_state["user"]["action_status"])
