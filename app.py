import streamlit as st
import pandas as pd

st.set_page_config(page_title="Steve's World", page_icon="⛏️", layout="wide")
df = pd.read_csv("minecraft_players.csv")
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

elif page == "Player Data":

    st.title("Minecraft Player Data")
    st.write("Explore and analyse the sample Minecraft player dataset.")

    st.subheader("Filter Player Data")

    selected_world = st.selectbox(
        "Select World:",
        ["All"] + list(df["World"].unique())
    )

    selected_modes = st.multiselect(
        "Select Game Modes:",
        options=list(df["Game Mode"].unique())
    )

    filtered_df = df.copy()

    if selected_world != "All":
        filtered_df = filtered_df[
            filtered_df["World"] == selected_world
        ]

    if selected_modes:
        filtered_df = filtered_df[
            filtered_df["Game Mode"].isin(selected_modes)
        ]

    st.subheader("Player Records")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )
    st.write("Total Records:", len(filtered_df))
   