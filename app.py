import streamlit as st

st.set_page_config(page_title="Steve's World", page_icon="⛏️", layout="wide")
st.sidebar.title("⛏️ Steve's World")
page = st.sidebar.radio("Navigate", ["Home", "Steve's Story", "Player Profile", "Player Data", "Join the World"])
