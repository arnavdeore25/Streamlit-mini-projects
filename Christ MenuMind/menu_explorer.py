
import pandas as pd
import streamlit as st

def render_menu_explorer(filtered_menu, light_theme):
    st.divider()
    st.subheader("🍴 Explore Menu")
    st.caption("Search food items and sort the results using the available options.")

    if not filtered_menu.empty:
        menu_search_col, menu_sort_col, menu_order_col = st.columns([2, 1.3, 1.2])

        with menu_search_col:
            menu_search = st.text_input(
                "Search food",
                placeholder="Search by item or outlet name...",
                key="menu_search_input"
            )

        with menu_sort_col:
            menu_sort_by = st.selectbox(
                "Sort by",
                ["Default", "Price", "Rating", "Food Name", "Outlet"],
                key="menu_sort_by"
            )

        with menu_order_col:
            menu_sort_order = st.selectbox(
                "Order",
                ["Ascending", "Descending"],
                key="menu_sort_order"
            )

        menu_display = filtered_menu.copy()

        if menu_search.strip():
            search_text = menu_search.strip()
            searchable_columns = ["item_name", "outlet_name", "category", "food_type"]
            search_mask = pd.Series(False, index=menu_display.index)

            for column in searchable_columns:
                if column in menu_display.columns:
                    search_mask |= menu_display[column].astype(str).str.contains(
                        search_text, case=False, na=False
                    )

            menu_display = menu_display[search_mask]

        sort_columns = {
            "Price": "price_inr",
            "Rating": "average_rating",
            "Food Name": "item_name",
            "Outlet": "outlet_name"
        }

        if menu_sort_by in sort_columns:
            sort_column = sort_columns[menu_sort_by]
            if sort_column in menu_display.columns:
                menu_display = menu_display.sort_values(
                    by=sort_column,
                    ascending=(menu_sort_order == "Ascending"),
                    na_position="last"
                )

        st.caption(f"Showing **{len(menu_display):,}** of **{len(filtered_menu):,}** food items.")

        display_columns = [
            column for column in [
                "outlet_name",
                "item_name",
                "category",
                "food_type",
                "price_inr",
                "average_rating"
            ]
            if column in menu_display.columns
        ]

        if menu_display.empty:
            st.warning("No food items match your search.")
        else:
            st.dataframe(
                menu_display[display_columns],
                use_container_width=True,
                hide_index=True
            )
    else:
        st.warning("No food items found for the selected filters.")

