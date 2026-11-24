import pandas as pd
import streamlit as st

from config import DATA_DIR
from data_loader import load_data
from sidebar import render_sidebar
from dashboard_header import render_dashboard_header
from kpis import render_kpis
from analytics import render_analytics
from menu_explorer import render_menu_explorer
from footer import render_footer


def main():
    """Load data and assemble the dashboard from feature modules."""
    st.set_page_config(
        page_title="Christ MenuMind",
        page_icon="🍽️",
        layout="wide",
    )

    try:
        data = load_data(DATA_DIR)
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as error:
        st.error("Christ MenuMind could not load its data files.")
        st.code(str(error))
        st.info(
            "Verify that all required CSV files are inside the `data/` folder "
            "and contain valid CSV data."
        )
        st.stop()

    filters = render_sidebar(
        data["blocks"],
        data["outlets"],
        data["menu"],
        data["sales"],
        data["student_reviews"],
        data["operations"],
    )

    render_dashboard_header(
        filters["selected_block"],
        filters["selected_outlet"],
        filters["food_preference"],
        filters["light_theme"],
    )

    if filters["show_kpis_only"]:
        render_kpis(
            data["blocks"],
            filters["filtered_outlets"],
            filters["filtered_menu"],
        )
    else:
        render_analytics(
            selected_outlet=filters["selected_outlet"],
            filtered_menu=filters["filtered_menu"],
            filtered_sales=filters["filtered_sales"],
            filtered_reviews=filters["filtered_reviews"],
            filtered_operations=filters["filtered_operations"],
            menu=data["menu"],
            light_theme=filters["light_theme"],
            chart_bg_color=filters["chart_bg_color"],
            chart_text_color=filters["chart_text_color"],
            chart_grid_color=filters["chart_grid_color"],
            chart_edge_color=filters["chart_edge_color"],
        )

    render_menu_explorer(filters["filtered_menu"], filters["light_theme"])
    render_footer()

if __name__ == "__main__":
    main()
