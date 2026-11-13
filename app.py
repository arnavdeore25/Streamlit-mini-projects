
import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Steve's World",
    page_icon="⛏️",
    layout="wide"
)

df = pd.read_csv("minecraft_players.csv")

st.sidebar.title("⛏️ Steve's World")

page = st.sidebar.radio(
    "Navigate",
    ["Home", "Steve's Story", "Player Profile", "Player Data", "Join the World"]
)

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

elif page == "Steve's Story":

    st.title("The Story of Steve")

    image_path = "assets/steve_pixel.png"
    st.image(image_path, width=200)

    st.subheader("Who is Steve?")

    st.write("""
    Steve is one of the default player characters in Minecraft.

    He is known for his blue shirt, blue pants, and block-shaped
    appearance.

    Players control Steve to explore worlds, collect resources,
    build structures, and survive against different creatures.
    """)

    st.subheader("A Little History")

    st.write("""
    - Steve appeared in the early development versions of Minecraft.
    - He became one of the most recognizable characters in gaming.
    - Alex was later introduced as another default character.
    - Players can customize their character's appearance using skins.
    """)

    st.subheader("Interesting Facts")

    st.write("1. Steve does not have official spoken dialogue.")
    st.write("2. Steve can explore, mine, craft, and build.")
    st.write("3. His default appearance has a blue shirt and blue pants.")
    st.write("4. Minecraft does not officially specify Steve's weight.")

elif page == "Player Profile":

    st.title("Steve's Player Profile")

    image_path = "assets/steve_pixel.png"
    st.image(image_path, width=150)

    st.subheader("Select Profile Information")

    profile_option = st.radio(
        "Choose a category:",
        ["Basic Details", "Appearance", "Game Details"]
    )

    if profile_option == "Basic Details":

        st.write("**Character Name:** *Steve*")
        st.write("**Character Type:** *Default Minecraft Avatar*")
        st.write("**Origin:** *Minecraft*")
        st.write("**Height:** *Approximately 1.8 blocks*")

    elif profile_option == "Appearance":

        st.write("**Hair:** *Dark Brown*")
        st.write("**Shirt:** *Blue*")
        st.write("**Pants:** *Blue*")
        st.write("**Shoes:** *Dark Grey*")

    elif profile_option == "Game Details":

        st.write("**Game:** *Minecraft*")
        st.write("**Developer:** *Mojang Studios*")
        st.write("**Main Activities:** *Mining, Crafting, Building*")

    st.divider()

    st.subheader("Select Game Mode")

    game_mode = st.radio(
        "Choose a game mode:",
        ["Survival", "Creative", "Adventure", "Spectator", "Hardcore"]
    )

    st.write("Selected Game Mode:", game_mode)

    if game_mode == "Survival":
        st.warning("Collect resources and survive in the Minecraft world.")

    elif game_mode == "Creative":
        st.success("Build anything using unlimited resources.")

    elif game_mode == "Adventure":
        st.success("Explore maps and complete challenges.")

    elif game_mode == "Spectator":
        st.success("Explore the world without interacting with it.")

    elif game_mode == "Hardcore":
        st.error("Survive on Hard difficulty with only one life.")

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

elif page == "Join the World":

    st.title("Join the Minecraft World!")
    st.write("Fill out this form to register as a Minecraft player.")

    with st.form("player_registration"):

        player_name = st.text_input("Enter your name")
        email = st.text_input("Enter your email")
        age = st.number_input(
            "Enter your age",
            min_value=10,
            max_value=100,
            value=18
        )

        gender = st.radio(
            "Select your gender:",
            ["Male", "Female", "Other"]
        )

        country = st.selectbox(
            "Select your country:",
            ["India", "USA", "UK", "Canada", "Australia", "Other"]
        )

        favourite_modes = st.multiselect(
            "Select your favourite game modes:",
            ["Survival", "Creative", "Adventure", "Spectator", "Hardcore"]
        )

        experience = st.select_slider(
            "How experienced are you?",
            options=["Beginner", "Intermediate", "Advanced", "Expert"]
        )

        favourite_activity = st.selectbox(
            "Favourite Minecraft Activity:",
            ["Mining", "Building", "Exploring", "Fighting"]
        )

        agreement = st.checkbox("I agree to the registration terms")

        submitted = st.form_submit_button("Join the World")

    # Process the submitted form (VALIDATION)
    if submitted:
        if player_name == "" or email == "":
            st.error("Please enter your name and email.")

        elif "@" not in email or "." not in email:
            st.error("Please enter a valid email address.")

        elif not agreement:
            st.warning("Please accept the registration terms.")

        else:
            st.success("Congratulations! You have joined Steve's World.")

            st.subheader("Your Registration Details")

            st.write("**Name:**", player_name)
            st.write("**Email:**", email)
            st.write("**Age:**", age)
            st.write("**Gender:**", gender)
            st.write("**Country:**", country)
            st.write("**Favourite Modes:**", favourite_modes)
            st.write("**Experience:**", experience)
            st.write("**Favourite Activity:**", favourite_activity)

            # Display celebration animation
            st.balloons()
