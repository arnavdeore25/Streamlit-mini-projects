import streamlit as st


def render_kpis(blocks, filtered_outlets, filtered_menu):
    # KPI-only view: shown when the sidebar toggle is enabled.
        st.subheader("📌 Campus Overview")
        st.caption("Key indicators based on your current block, outlet and food preference filters.")

        total_items = len(filtered_menu)
        total_veg = (
            filtered_menu["food_type"].astype(str).str.strip().str.lower()
            .eq("vegetarian").sum()
        )
        total_chicken = (
            filtered_menu["food_type"].astype(str).str.strip().str.lower()
            .str.startswith("non-vegetarian").sum()
        )
        average_price = filtered_menu["price_inr"].mean() if total_items else 0
        average_rating = (
            filtered_menu["average_rating"].mean()
            if total_items and "average_rating" in filtered_menu.columns
            else 0
        )

        kpi_style = """
        <style>
        div[data-testid="stMetric"] {
            background: rgba(30, 41, 59, 0.48);
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 12px;
            padding: 16px 18px;
            min-height: 112px;
        }
        div[data-testid="stMetricLabel"] {
            min-height: 2.2rem;
            align-items: center;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.65rem;
            font-weight: 700;
        }
        </style>
        """
        st.markdown(kpi_style, unsafe_allow_html=True)

        kpi_row1 = st.columns(3)
        kpi_row1[0].metric("🏢 Campus Blocks", f"{blocks.shape[0]:,}")
        kpi_row1[1].metric("🏪 Selected Outlets", f"{filtered_outlets.shape[0]:,}")
        kpi_row1[2].metric("🍽️ Food Items", f"{total_items:,}")

        kpi_row2 = st.columns(4)
        kpi_row2[0].metric("💰 Average Price", f"₹{average_price:.0f}" if total_items else "N/A")
        kpi_row2[1].metric("⭐ Average Rating", f"{average_rating:.1f}/5" if total_items else "N/A")
        kpi_row2[2].metric("🥗 Vegetarian Items", f"{total_veg:,}")
        kpi_row2[3].metric("🍗 Chicken Items", f"{total_chicken:,}")

        st.info("Turn off **Show KPIs only** in the sidebar to return to analytics graphs.")
