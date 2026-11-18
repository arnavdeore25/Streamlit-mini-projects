
import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Christ MenuMind",
    page_icon="🍽️",
    layout="wide"
)

# Load datasets
blocks = pd.read_csv("data/blocks.csv")
outlets = pd.read_csv("data/outlets.csv")
menu = pd.read_csv("data/menu_items.csv")
sales = pd.read_csv("data/sales_data.csv")

# Sidebar
st.sidebar.title("🍽️ Christ MenuMind")
st.sidebar.markdown("Campus Food Intelligence")

# Block selection
selected_block = st.sidebar.selectbox(
    "Select Campus Block",
    ["All Blocks"] + blocks["block_name"].tolist()
)

# Filter outlets based on selected block
if selected_block == "All Blocks":
    available_outlets = outlets
else:
    available_outlets = outlets[
        outlets["block_name"] == selected_block
    ]

# Outlet selection
selected_outlet = st.sidebar.selectbox(
    "Select Outlet",
    ["All Outlets"] + available_outlets["outlet_name"].tolist()
)

# Main heading
st.title("🍽️ Christ MenuMind")
st.subheader("Eat Smart. Explore Better. Decide with Data.")

st.write(
    "An intelligent campus food analytics platform "
    "for exploring food menus, prices, sales and student preferences."
)

st.divider()

# Apply filters
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

# Apply outlet filter
if selected_outlet != "All Outlets":
    filtered_outlets = filtered_outlets[
        filtered_outlets["outlet_name"] == selected_outlet
    ]

    filtered_menu = filtered_menu[
        filtered_menu["outlet_name"] == selected_outlet
    ]

    filtered_sales = filtered_sales[
        filtered_sales["outlet_name"] == selected_outlet
    ]

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Blocks", blocks.shape[0])
col2.metric("Total Outlets", filtered_outlets.shape[0])
col3.metric("Total Food Items", filtered_menu.shape[0])

col4.metric(
    "Average Food Price",
    f"₹{filtered_menu['price_inr'].mean():.0f}"
    if not filtered_menu.empty else "₹0"
)

st.divider()

# Menu Overview
st.subheader("🍴 Menu Overview")

if not filtered_menu.empty:
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
else:
    st.warning("No food items found for this selection.")

st.divider()
st.caption("Christ MenuMind | Campus Food Intelligence Dashboard")
