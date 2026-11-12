import streamlit as st

st.set_page_config(page_title="Steve's World", page_icon="⛏️", layout="wide")
st.sidebar.title("⛏️ Steve's World")
page = st.sidebar.radio("Navigate", ["Home", "Steve's Story", "Player Profile", "Player Data", "Join the World"])

if page == "Home":
    st.title("Welcome to Steve's World!")
    image_path = "assets/steve_pixel.png"
    st.image(image_path, width=200)
    st.write("""
    Welcome to Steve's World!

    This dashboard is dedicated to Steve, one of the most
    famous characters from Minecraft.

    Explore his story, view his profile, analyse player data,
    and join the Minecraft world.
    """)
    st.subheader("Explore the Dashboard")
    st.write("Use the sidebar to explore different sections.")

