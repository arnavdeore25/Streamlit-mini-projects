
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="MenuIQ",
    page_icon="🍽️",
    layout="wide"
)

blocks = pd.read_csv("data/blocks.csv")
outlets = pd.read_csv("data/outlets.csv")
menu = pd.read_csv("data/menu_items.csv")
sales = pd.read_csv("data/sales_data.csv")

st.sidebar.title("🍽️ MenuIQ")
st.sidebar.markdown("Campus Food Intelligence")

selected_block = st.sidebar.selectbox(
    "Select Campus Block",
    ["All Blocks"] + blocks["block_name"].tolist()
)

st.title("🍽️ MenuIQ")
st.subheader("Eat Smart. Explore Better. Decide with Data.")

st.write(
    "An intelligent campus food analytics platform "
    "for exploring food menus, prices, sales and student preferences."
)

st.divider()

if selected_block == "All Blocks":
    filtered_outlets = outlets
    filtered_menu = menu
    filtered_sales = sales
else:
    filtered_outlets = outlets[
        outlets["block_name"] == selected_block
    ]

    filtered_menu = menu[
        menu["block_name"] == selected_block
    ]

    filtered_sales = sales[
        sales["block_name"] == selected_block
    ]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Blocks", blocks.shape[0])
col2.metric("Total Outlets", filtered_outlets.shape[0])
col3.metric("Total Food Items", filtered_menu.shape[0])
col4.metric(
    "Average Food Price",
    f"₹{filtered_menu['price_inr'].mean():.0f}"
)

st.divider()

st.subheader("🍴 Menu Overview")

st.dataframe(
    filtered_menu[
        [
            "outlet_name",
            "item_name",
            "category",
            "food_type",
            "price_inr",
            "average_rating"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()
st.caption("MenuIQ | Campus Food Intelligence Dashboard")
