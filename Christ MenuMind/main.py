
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Christ MenuMind",
    page_icon="🍽️",
    layout="wide"
)

# Load data
blocks = pd.read_csv("data/blocks.csv")
outlets = pd.read_csv("data/outlets.csv")
menu = pd.read_csv("data/menu_items.csv")
sales = pd.read_csv("data/sales_data.csv")

# Sidebar
st.sidebar.title("🍽️ Christ MenuMind")
st.sidebar.caption("Campus Food Intelligence")
st.sidebar.divider()

selected_block = st.sidebar.selectbox(
    "Select Campus Block",
    ["All Blocks"] + blocks["block_name"].tolist()
)

# Filter outlet options
if selected_block == "All Blocks":
    available_outlets = outlets["outlet_name"].tolist()
else:
    available_outlets = outlets[
        outlets["block_name"] == selected_block
    ]["outlet_name"].tolist()

selected_outlet = st.sidebar.selectbox(
    "Select Outlet",
    ["All Outlets"] + available_outlets
)

# Apply filters
if selected_block == "All Blocks":
    filtered_outlets = outlets.copy()
    filtered_menu = menu.copy()
    filtered_sales = sales.copy()
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

# Main dashboard
st.title("🍽️ Christ MenuMind")
st.subheader("Eat Smart. Explore Better. Decide with Data.")

st.write(
    "An intelligent campus food analytics platform "
    "for exploring food menus, prices, sales and student preferences."
)

st.divider()

# KPI cards
st.subheader("📌 Campus Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Campus Blocks", blocks.shape[0])
col2.metric("Total Outlets", filtered_outlets.shape[0])
col3.metric("Total Food Items", filtered_menu.shape[0])

if not filtered_menu.empty:
    average_price = filtered_menu["price_inr"].mean()
    col4.metric("Average Food Price", f"₹{average_price:.0f}")
else:
    col4.metric("Average Food Price", "N/A")

st.divider()

# Analysis options
st.subheader("📊 Explore Food Analytics")

analysis_group = st.radio(
    "Choose Analysis Category",
    [
        "Menu Analytics",
        "Pricing Analytics",
        "Sales Analytics",
        "Student Feedback",
        "Operational Analytics"
    ],
    horizontal=True
)

chart_options = {
    "Menu Analytics": [
        "Category Distribution",
        "Vegetarian vs Chicken",
        "Menu Availability by Outlet",
        "Category Distribution by Outlet"
    ],

    "Pricing Analytics": [
        "Average Price by Category",
        "Food Price Distribution",
        "Price Comparison by Category",
        "Outlet-wise Average Pricing"
    ],

    "Sales Analytics": [
        "Revenue Trend",
        "Top 10 Best-Selling Items",
        "Revenue by Outlet",
        "Category-wise Sales Contribution",
        "Sales Activity"
    ],

    "Student Feedback": [
        "Rating Distribution",
        "Outlet Satisfaction",
        "Feedback Dimension Analysis"
    ],

    "Operational Analytics": [
        "Daily Footfall",
        "Average Waiting Time",
        "Food Wastage"
    ]
}

chart_choice = st.radio(
    "Select Analysis",
    chart_options[analysis_group],
    horizontal=True
)

# Menu overview
st.divider()
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
    st.warning("No food items found.")

# Footer
st.divider()

st.caption(
    "Christ MenuMind | Campus Food Intelligence Dashboard"
)
