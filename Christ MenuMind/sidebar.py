from pathlib import Path
import streamlit as st
from config import BASE_DIR, read_stylesheet

def render_sidebar(blocks, outlets, menu, sales, student_reviews, operations):
    """Render sidebar controls and return filters, filtered data, and theme settings."""
    # Sidebar
    st.sidebar.title("🍽️ Christ MenuMind")
    st.sidebar.caption("Campus Food Intelligence")

    # Theme switch: OFF = Dark, ON = Light
    light_theme = st.sidebar.toggle(
        "Light Theme",
        value=False,
        key="light_theme_toggle",
        help="Switch between the dark and light dashboard appearance."
    )
    theme_name = "Light" if light_theme else "Dark"

    # Chart colours follow the selected theme.
    chart_bg_color = "#FFFFFF" if light_theme else "#0e1117"
    chart_text_color = "#263238" if light_theme else "#FFFFFF"
    chart_grid_color = "#D9E0E7" if light_theme else "#64748B"
    chart_edge_color = "#FFFFFF" if light_theme else "#0e1117"

    css = read_stylesheet(BASE_DIR / "style.css")

    light_theme_css = ""
    if light_theme:
        light_theme_css = read_stylesheet(BASE_DIR / "style_light.css")


    st.markdown(
        f"<style>{css}\n{light_theme_css}</style>",
        unsafe_allow_html=True
    )

    st.sidebar.divider()

    # Filter controls
    def reset_filters():
        st.session_state["selected_block_filter"] = "All Blocks"
        st.session_state["selected_outlet_filter"] = "All Outlets"
        st.session_state["food_preference_filter"] = "All"


    def reset_outlet_on_block_change():
        st.session_state["selected_outlet_filter"] = "All Outlets"


    selected_block = st.sidebar.selectbox(
        "Select Campus Block",
        ["All Blocks"] + blocks["block_name"].tolist(),
        key="selected_block_filter",
        on_change=reset_outlet_on_block_change
    )

    # Filter outlet options based on the selected block
    if selected_block == "All Blocks":
        available_outlets = outlets["outlet_name"].tolist()
    else:
        available_outlets = outlets[
            outlets["block_name"] == selected_block
        ]["outlet_name"].tolist()

    selected_outlet = st.sidebar.selectbox(
        "Select Outlet",
        ["All Outlets"] + available_outlets,
        key="selected_outlet_filter"
    )

    food_preference = st.sidebar.radio(
        "Food Preference",
        ["All", "Veg", "Non-Veg"],
        horizontal=True,
        key="food_preference_filter"
    )

    st.sidebar.divider()
    st.sidebar.button(
        "↺ Reset Filters",
        use_container_width=True,
        on_click=reset_filters
    )

    st.sidebar.divider()
    show_kpis_only = st.sidebar.toggle(
        "Show KPIs only",
        value=False,
        help="Turn on to view KPI cards instead of analytics graphs."
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

    # Filter student reviews
    if selected_block == "All Blocks":
        filtered_reviews = student_reviews.copy()
    else:
        filtered_reviews = student_reviews[
            student_reviews["block_name"] == selected_block
        ]

    if selected_outlet != "All Outlets":
        filtered_reviews = filtered_reviews[
            filtered_reviews["outlet_name"] == selected_outlet
        ]

    # Filter operational data
    if selected_block == "All Blocks":
        filtered_operations = operations.copy()
    else:
        filtered_operations = operations[
            operations["block_name"] == selected_block
        ].copy()

    if selected_outlet != "All Outlets":
        filtered_operations = filtered_operations[
            filtered_operations["outlet_name"] == selected_outlet
        ]

    # Apply Veg / Non-Veg preference consistently across menu, sales and feedback.
    if food_preference == "Veg":
        filtered_menu = filtered_menu[
            filtered_menu["food_type"].astype(str).str.strip().str.lower() == "vegetarian"
        ]
    elif food_preference == "Non-Veg":
        filtered_menu = filtered_menu[
            filtered_menu["food_type"].astype(str).str.strip().str.lower().str.startswith("non-vegetarian")
        ]

    if food_preference != "All":
        matching_item_ids = filtered_menu["item_id"].unique()
        if "item_id" in filtered_sales.columns:
            filtered_sales = filtered_sales[
                filtered_sales["item_id"].isin(matching_item_ids)
            ]
        if "item_id" in filtered_reviews.columns:
            filtered_reviews = filtered_reviews[
                filtered_reviews["item_id"].isin(matching_item_ids)
            ]

    return {
        "selected_block": selected_block,
        "selected_outlet": selected_outlet,
        "food_preference": food_preference,
        "show_kpis_only": show_kpis_only,
        "filtered_outlets": filtered_outlets,
        "filtered_menu": filtered_menu,
        "filtered_sales": filtered_sales,
        "filtered_reviews": filtered_reviews,
        "filtered_operations": filtered_operations,
        "light_theme": light_theme,
        "chart_bg_color": chart_bg_color,
        "chart_text_color": chart_text_color,
        "chart_grid_color": chart_grid_color,
        "chart_edge_color": chart_edge_color,
    }
