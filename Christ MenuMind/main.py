
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(
    page_title="Christ MenuMind",
    page_icon="🍽️",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
# Data directory
DATA_DIR = BASE_DIR / "data"

# Load data
blocks = pd.read_csv(DATA_DIR / "blocks.csv")
outlets = pd.read_csv(DATA_DIR/"data/outlets.csv")
menu = pd.read_csv(DATA_DIR/"data/menu_items.csv")
sales = pd.read_csv(DATA_DIR/"data/sales_data.csv")
student_reviews = pd.read_csv(DATA_DIR/"data/student_reviews.csv")
operations = pd.read_csv(DATA_DIR/"data/outlet_daily_operations.csv")

# Clean operational data column names
operations.columns = (
    operations.columns
    .str.replace("\ufeff", "", regex=False)
    .str.strip()
    .str.lower()
)
operations["date"] = pd.to_datetime(operations["date"], errors="coerce")

# Clean review column names
student_reviews.columns = (
    student_reviews.columns
    .str.replace("\ufeff", "", regex=False)
    .str.strip()
    .str.lower()
)

# Keep the feedback column name consistent with the chart logic.
if "value_for_money" not in student_reviews.columns and "value_for_money_rating" in student_reviews.columns:
    student_reviews = student_reviews.rename(
        columns={"value_for_money_rating": "value_for_money"}
    )

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

css = open(BASE_DIR /"style.css", encoding="utf-8").read()

light_theme_css = ""
if light_theme:
    with open(BASE_DIR /"style_light.css", encoding="utf-8") as light_css_file:
        light_theme_css = light_css_file.read()


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

# Live clock, date and greeting
clock_html = """
    <div id="menumind-header" style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
        padding: 16px 22px;
        margin: 4px 0 18px 0;
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 14px;
        background: __CLOCK_BG__;
        color: __CLOCK_TEXT__;
        font-family: Arial, sans-serif;
        box-sizing: border-box;
    ">
        <div>
            <div id="greeting" style="font-size: 21px; font-weight: 700; margin-bottom: 5px;">
                Welcome!
            </div>
            <div style="font-size: 13px; color: __CLOCK_MUTED__;">
                Here's your campus food overview for today.
            </div>
        </div>
        <div style="text-align: right; min-width: 150px;">
            <div id="live-clock" style="font-size: 27px; font-weight: 700; letter-spacing: 1px;">
                --:--:--
            </div>
            <div id="live-date" style="font-size: 13px; color: __CLOCK_MUTED__; margin-top: 3px;">
                Loading date...
            </div>
        </div>
    </div>

    <script>
        function updateMenuMindHeader() {
            const now = new Date();
            const hour = now.getHours();

            let greeting = "Good evening";
            if (hour >= 5 && hour < 12) {
                greeting = "Good morning";
            } else if (hour >= 12 && hour < 17) {
                greeting = "Good afternoon";
            }

            document.getElementById("greeting").textContent = greeting + "!";
            document.getElementById("live-clock").textContent =
                now.toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                    second: "2-digit"
                });
            document.getElementById("live-date").textContent =
                now.toLocaleDateString([], {
                    weekday: "long",
                    day: "numeric",
                    month: "long",
                    year: "numeric"
                });
        }

        updateMenuMindHeader();
        setInterval(updateMenuMindHeader, 1000);
    </script>
    """

clock_html = (
    clock_html
    .replace("__CLOCK_BG__", "linear-gradient(110deg, #FFFFFF, #EAF1F7)" if light_theme else "linear-gradient(110deg, rgba(30, 41, 59, 0.92), rgba(15, 23, 42, 0.88))")
    .replace("__CLOCK_TEXT__", "#263445" if light_theme else "#F8FAFC")
    .replace("__CLOCK_MUTED__", "#64748B" if light_theme else "#CBD5E1")
)
st.components.v1.html(clock_html, height=112, scrolling=False)


# Main dashboard
st.title("🍽️ Christ MenuMind")
st.subheader("Eat Smart. Explore Better. Decide with Data.")

st.write(
    "An intelligent campus food analytics platform "
    "for exploring food menus, prices, sales and student preferences."
)

# Active filter summary
active_block_label = selected_block
active_outlet_label = selected_outlet
active_food_label = {
    "All": "All Food Types",
    "Veg": "Vegetarian",
    "Non-Veg": "Non-Vegetarian (Chicken)"
}[food_preference]

st.markdown("### 🔎 Active Filters")
filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    st.markdown(
        f"""
        <div style="
            padding: 12px 16px;
            border: 1px solid rgba(148, 163, 184, 0.25);
            border-radius: 10px;
            background: rgba(30, 41, 59, 0.45);
        ">
            <div style="font-size: 12px; color: #94A3B8;">CAMPUS BLOCK</div>
            <div style="font-size: 16px; font-weight: 600; color: #F8FAFC;">
                {active_block_label}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with filter_col2:
    st.markdown(
        f"""
        <div style="
            padding: 12px 16px;
            border: 1px solid rgba(148, 163, 184, 0.25);
            border-radius: 10px;
            background: rgba(30, 41, 59, 0.45);
        ">
            <div style="font-size: 12px; color: #94A3B8;">OUTLET</div>
            <div style="font-size: 16px; font-weight: 600; color: #F8FAFC;">
                {active_outlet_label}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with filter_col3:
    st.markdown(
        f"""
        <div style="
            padding: 12px 16px;
            border: 1px solid rgba(148, 163, 184, 0.25);
            border-radius: 10px;
            background: rgba(30, 41, 59, 0.45);
        ">
            <div style="font-size: 12px; color: #94A3B8;">FOOD PREFERENCE</div>
            <div style="font-size: 16px; font-weight: 600; color: #F8FAFC;">
                {active_food_label}
            </div>
        </div>
        """,
        unsafe_allow_html=True  
    )

st.divider()

# KPI-only view: shown when the sidebar toggle is enabled.
if show_kpis_only:
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

else:
    # Keep horizontal radio groups aligned and prevent option text from overflowing.
    st.markdown(
        """
        <style>
        div[data-testid="stRadio"] div[role="radiogroup"] {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 0.65rem 1.25rem;
            width: 100%;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label {
            white-space: nowrap;
            margin: 0;
        }
        div[data-testid="stRadio"] {
            min-width: 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

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
            "Top 10 Best-Selling Items"
        ],

        "Student Feedback": [
            "Rating Distribution",
            "Outlet Satisfaction",
            "Student Recommendation Analysis",
            "Rating Trends Over Time",
            "Most Reviewed Food Items"
        ],

        "Operational Analytics": [
            "Daily Footfall Trend",
            "Outlet-wise Footfall Comparison",
            "Day-wise Footfall Heatmap",
            "Outlet-wise Average Waiting Time",
            "Waiting Time Trend",
            "Footfall vs Waiting Time"
        ]
    }

    # Hide outlet-comparison charts when a single outlet is selected.
    outlet_comparison_charts = {
        "Menu Availability by Outlet",
        "Category Distribution by Outlet",
        "Outlet-wise Average Pricing",
        "Outlet Satisfaction",
        "Outlet Rating Heatmap",
        "Outlet-wise Footfall Comparison",
        "Outlet-wise Average Waiting Time"
    }

    visible_chart_options = chart_options[analysis_group]

    if selected_outlet != "All Outlets":
        visible_chart_options = [
            chart for chart in visible_chart_options
            if chart not in outlet_comparison_charts
        ]

    st.divider()

    for chart_index, chart_choice in enumerate(visible_chart_options):
        if chart_index % 2 == 0:
            chart_columns = st.columns(2)

        with chart_columns[chart_index % 2]:
            with st.container(border=True):
                st.subheader(f"📈 {chart_choice}")

                # Display selected graph
                if analysis_group in ["Menu Analytics", "Pricing Analytics"] and filtered_menu.empty:
                    st.warning("No menu data available for the selected filters.")

                elif analysis_group == "Menu Analytics":

                    fig = None
                    ax = None

                    # Category distribution
                    if chart_choice == "Category Distribution":

                        chart_data = (
                            filtered_menu.groupby("category")
                            .size()
                            .reset_index(name="item_count")
                            .sort_values("item_count", ascending=True)
                        )

                        fig, ax = plt.subplots(figsize=(10, 7))

                        bars = ax.barh(
                            chart_data["category"],
                            chart_data["item_count"],
                            color=plt.cm.viridis(
                                np.linspace(0.25, 0.85, len(chart_data))
                            )
                        )

                        ax.set_title(
                            "Menu Distribution by Category",
                            fontsize=16,
                            fontweight="bold",
                            color=chart_text_color
                        )

                        ax.set_xlabel("Number of Food Items")
                        ax.set_ylabel("Category")

                        for bar in bars:
                            ax.text(
                                bar.get_width() + 1,
                                bar.get_y() + bar.get_height() / 2,
                                int(bar.get_width()),
                                va="center",
                                color=chart_text_color
                            )

                    # Vegetarian vs Chicken
                    elif chart_choice == "Vegetarian vs Chicken":

                        chart_data = (
                            filtered_menu.groupby("food_type")
                            .size()
                            .reset_index(name="item_count")
                        )

                        total_items = chart_data["item_count"].sum()

                        colors = ["#66C2A5", "#FC8D62"]

                        fig, ax = plt.subplots(figsize=(9, 5))

                        wedges, texts, autotexts = ax.pie(
                            chart_data["item_count"],
                            labels=None,
                            autopct="%1.1f%%",
                            startangle=90,
                            pctdistance=0.78,
                            colors=colors[:len(chart_data)],
                            wedgeprops={
                                "width": 0.38,
                                "edgecolor": chart_edge_color,
                                "linewidth": 3
                            },
                            textprops={
                                "color": "white",
                                "fontsize": 12,
                                "fontweight": "bold"
                            }
                        )

                        ax.text(
                            0, 0,
                            f"{total_items}\nItems",
                            ha="center",
                            va="center",
                            fontsize=20,
                            fontweight="bold",
                            color=chart_text_color
                        )

                        ax.set_title(
                            "Vegetarian vs Chicken Distribution",
                            fontsize=16,
                            fontweight="bold",
                            color=chart_text_color,
                            pad=20
                        )

                        legend_labels = [
                            f"{food_type} ({count})"
                            for food_type, count in zip(
                                chart_data["food_type"],
                                chart_data["item_count"]
                            )
                        ]

                        legend = ax.legend(
                            wedges,
                            legend_labels,
                            title="Food Type",
                            loc="center left",
                            bbox_to_anchor=(1, 0.5),
                            frameon=False,
                            fontsize=11
                        )

                        legend.get_title().set_color(chart_text_color)

                        for text in legend.get_texts():
                            text.set_color(chart_text_color)

                    # Menu availability by outlet
                    elif chart_choice == "Menu Availability by Outlet":

                        chart_data = (
                            filtered_menu.groupby("outlet_name")
                            .size()
                            .reset_index(name="item_count")
                            .sort_values("item_count", ascending=False)
                        )

                        fig, ax = plt.subplots(figsize=(12, 6))

                        bars = ax.bar(
                            chart_data["outlet_name"],
                            chart_data["item_count"],
                            color="#66C2A5",
                            width=0.65
                        )

                        ax.set_title(
                            "Menu Items Available per Outlet",
                            fontsize=16,
                            fontweight="bold",
                            color=chart_text_color,
                            pad=20
                        )

                        ax.set_xlabel("Outlet")
                        ax.set_ylabel("Number of Food Items")

                        ax.tick_params(axis="x", rotation=45)

                        for bar in bars:
                            ax.text(
                                bar.get_x() + bar.get_width() / 2,
                                bar.get_height() + 0.5,
                                int(bar.get_height()),
                                ha="center",
                                color=chart_text_color,
                                fontsize=9
                            )

                    # Category distribution by outlet
                    elif chart_choice == "Category Distribution by Outlet":

                        chart_data = (
                            filtered_menu.groupby(["outlet_name", "category"])
                            .size()
                            .reset_index(name="item_count")
                        )

                        pivot_data = chart_data.pivot(
                            index="outlet_name",
                            columns="category",
                            values="item_count"
                        ).fillna(0)

                        fig, ax = plt.subplots(figsize=(14, 7))

                        pivot_data.plot(
                            kind="bar",
                            stacked=False,
                            ax=ax,
                            width=0.8,
                            colormap="tab20"
                        )

                        ax.set_title(
                            "Category Distribution Across Outlets",
                            fontsize=16,
                            fontweight="bold",
                            color=chart_text_color,
                            pad=20
                        )

                        ax.set_xlabel("Outlet")
                        ax.set_ylabel("Number of Food Items")

                        ax.tick_params(axis="x", rotation=45)

                        legend = ax.legend(
                            title="Food Category",
                            bbox_to_anchor=(1.02, 1),
                            loc="upper left",
                            fontsize=8,
                            frameon=False
                        )

                        legend.get_title().set_color(chart_text_color)

                        for text in legend.get_texts():
                            text.set_color(chart_text_color)

                    # Common chart styling
                    if fig is not None:

                        fig.patch.set_facecolor(chart_bg_color)
                        ax.set_facecolor(chart_bg_color)

                        ax.tick_params(colors=chart_text_color)
                        ax.xaxis.label.set_color(chart_text_color)
                        ax.yaxis.label.set_color(chart_text_color)

                        if chart_choice != "Vegetarian vs Chicken":
                            ax.grid(axis="y", linestyle="--", alpha=0.35, color=chart_grid_color)
                            ax.grid(axis="x", visible=False)

                        for spine in ax.spines.values():
                            spine.set_visible(False)

                        plt.tight_layout()

                        st.pyplot(fig, use_container_width=True)

                        plt.close(fig)

                # Pricing analytics
                elif analysis_group == "Pricing Analytics":

                    price_data = filtered_menu.copy()

                    price_data["price_inr"] = pd.to_numeric(
                        price_data["price_inr"],
                        errors="coerce"
                    )

                    price_data = price_data.dropna(subset=["price_inr"])

                    if price_data.empty:
                        st.warning("No valid pricing data available.")

                    else:

                        fig = None
                        ax = None

                        # Average price by category
                        if chart_choice == "Average Price by Category":

                            chart_data = (
                                price_data.groupby("category")["price_inr"]
                                .mean()
                                .reset_index()
                                .sort_values("price_inr", ascending=True)
                            )

                            fig, ax = plt.subplots(figsize=(11, 7))

                            bars = ax.bar(
                                chart_data["category"],
                                chart_data["price_inr"],
                                color=plt.cm.viridis(
                                    np.linspace(0.25, 0.85, len(chart_data))
                                ),
                                width=0.65
                            )

                            ax.set_title(
                                "Average Price by Food Category",
                                fontsize=16,
                                fontweight="bold",
                                color=chart_text_color,
                                pad=20
                            )

                            ax.set_xlabel("Food Category")
                            ax.set_ylabel("Average Price (₹)")

                            ax.tick_params(axis="x", rotation=45)

                            for bar in bars:
                                ax.text(
                                    bar.get_x() + bar.get_width() / 2,
                                    bar.get_height() + 1,
                                    f"₹{bar.get_height():.0f}",
                                    ha="center",
                                    color=chart_text_color,
                                    fontsize=9
                                )

                        # Food price distribution
                        elif chart_choice == "Food Price Distribution":

                            fig, ax = plt.subplots(figsize=(11, 6))

                            ax.hist(
                                price_data["price_inr"],
                                bins=15,
                                color="#66C2A5",
                                edgecolor=chart_edge_color,
                                linewidth=1.5
                            )

                            median_price = price_data["price_inr"].median()

                            ax.axvline(
                                median_price,
                                color="#FC8D62",
                                linestyle="--",
                                linewidth=2,
                                label=f"Median: ₹{median_price:.0f}"
                            )

                            ax.set_title(
                                "Distribution of Food Prices",
                                fontsize=16,
                                fontweight="bold",
                                color=chart_text_color,
                                pad=20
                            )

                            ax.set_xlabel("Food Price (₹)")
                            ax.set_ylabel("Number of Food Items")

                            ax.legend(
                                facecolor=chart_bg_color,
                                edgecolor="none",
                                labelcolor=chart_text_color
                            )

                        # Price comparison by category
                        elif chart_choice == "Price Comparison by Category":

                            categories = sorted(price_data["category"].unique())

                            box_data = [
                                price_data.loc[
                                    price_data["category"] == category,
                                    "price_inr"
                                ].values
                                for category in categories
                            ]

                            fig, ax = plt.subplots(figsize=(12, 7))

                            boxplot = ax.boxplot(
                                box_data,
                                tick_labels=categories,
                                patch_artist=True,
                                medianprops={
                                    "color": "#FC8D62",
                                    "linewidth": 2
                                },
                                whiskerprops={
                                    "color": "white"
                                },
                                capprops={
                                    "color": "white"
                                },
                                flierprops={
                                    "marker": "o",
                                    "markerfacecolor": "#A78BFA",
                                    "markeredgecolor": "none",
                                    "markersize": 5
                                }
                            )

                            colors = plt.cm.viridis(
                                np.linspace(0.25, 0.85, len(categories))
                            )

                            for patch, color in zip(boxplot["boxes"], colors):
                                patch.set_facecolor(color)
                                patch.set_alpha(0.85)

                            ax.set_title(
                                "Food Price Comparison Across Categories",
                                fontsize=16,
                                fontweight="bold",
                                color=chart_text_color,
                                pad=20
                            )

                            ax.set_xlabel("Food Category")
                            ax.set_ylabel("Price (₹)")

                            ax.tick_params(axis="x", rotation=45)



                        # Outlet-wise average pricing
                        elif chart_choice == "Outlet-wise Average Pricing":

                            chart_data = (
                                price_data.groupby("outlet_name")["price_inr"]
                                .mean()
                                .reset_index()
                                .sort_values("price_inr", ascending=True)
                            )

                            fig, ax = plt.subplots(
                                figsize=(11, max(5, len(chart_data) * 0.4))
                            )

                            bars = ax.barh(
                                chart_data["outlet_name"],
                                chart_data["price_inr"],
                                color=plt.cm.viridis(
                                    np.linspace(0.25, 0.85, len(chart_data))
                                ),
                                height=0.65
                            )

                            ax.set_title(
                                "Average Food Price by Outlet",
                                fontsize=16,
                                fontweight="bold",
                                color=chart_text_color,
                                pad=20
                            )

                            ax.set_xlabel("Average Price (₹)")
                            ax.set_ylabel("Food Outlet")

                            for bar in bars:
                                ax.text(
                                    bar.get_width() + 1,
                                    bar.get_y() + bar.get_height() / 2,
                                    f"₹{bar.get_width():.0f}",
                                    va="center",
                                    color=chart_text_color,
                                    fontsize=9
                                )

                        # Pricing chart styling
                        if fig is not None:

                            fig.patch.set_facecolor(chart_bg_color)
                            ax.set_facecolor(chart_bg_color)

                            ax.tick_params(colors=chart_text_color)
                            ax.xaxis.label.set_color(chart_text_color)
                            ax.yaxis.label.set_color(chart_text_color)

                            ax.grid(
                                axis="y",
                                linestyle="--",
                                alpha=0.2
                            )

                            if chart_choice == "Outlet-wise Average Pricing":
                                ax.grid(axis="x", linestyle="--", alpha=0.35, color=chart_grid_color)
                                ax.grid(axis="y", visible=False)

                            for spine in ax.spines.values():
                                spine.set_visible(False)

                            plt.tight_layout()

                            st.pyplot(fig, use_container_width=True)

                            plt.close(fig)

                elif analysis_group == "Sales Analytics":

                    sales_data = filtered_sales.copy()

                    sales_data["sales_date"] = pd.to_datetime(
                        sales_data["sales_date"],
                        errors="coerce"
                    )

                    sales_data["net_sales_inr"] = pd.to_numeric(
                        sales_data["net_sales_inr"],
                        errors="coerce"
                    )

                    sales_data["quantity_sold"] = pd.to_numeric(
                        sales_data["quantity_sold"],
                        errors="coerce"
                    )

                    sales_data = sales_data.dropna(
                        subset=["sales_date", "net_sales_inr", "quantity_sold"]
                    )

                    if sales_data.empty:
                        st.warning("No sales data available for the selected filters.")

                    else:
                        fig, ax = plt.subplots(figsize=(12, 6))

                        # Revenue trend
                        if chart_choice == "Revenue Trend":

                            chart_data = (
                                sales_data.groupby("sales_date")["net_sales_inr"]
                                .sum()
                                .reset_index()
                                .sort_values("sales_date")
                            )

                            ax.plot(
                                chart_data["sales_date"],
                                chart_data["net_sales_inr"],
                                color="#66C2A5",
                                linewidth=2.5,
                                marker="o",
                                markersize=4
                            )

                            ax.fill_between(
                                chart_data["sales_date"],
                                chart_data["net_sales_inr"],
                                color="#66C2A5",
                                alpha=0.12
                            )

                            ax.set_title(
                                "Daily Campus Food Revenue Trend",
                                fontsize=16,
                                fontweight="bold",
                                color=chart_text_color,
                                pad=20
                            )

                            ax.set_xlabel("Sales Date")
                            ax.set_ylabel("Revenue (₹)")
                            fig.autofmt_xdate()

                        # Top 10 best-selling items
                        elif chart_choice == "Top 10 Best-Selling Items":

                            chart_data = (
                                sales_data.groupby("item_id")["quantity_sold"]
                                .sum()
                                .reset_index()
                                .sort_values("quantity_sold", ascending=False)
                                .head(10)
                                .merge(
                                    menu[["item_id", "item_name"]].drop_duplicates("item_id"),
                                    on="item_id",
                                    how="left"
                                )
                            )

                            chart_data["item_name"] = chart_data["item_name"].fillna(
                                chart_data["item_id"]
                            )
                            chart_data = chart_data.sort_values("quantity_sold", ascending=True)

                            fig.set_size_inches(12, 7)

                            bars = ax.barh(
                                chart_data["item_name"],
                                chart_data["quantity_sold"],
                                color=plt.cm.viridis(
                                    np.linspace(0.25, 0.85, len(chart_data))
                                ),
                                height=0.65
                            )

                            ax.set_title(
                                "Top 10 Most Purchased Food Items",
                                fontsize=16,
                                fontweight="bold",
                                color=chart_text_color,
                                pad=20
                            )

                            ax.set_xlabel("Total Quantity Sold")
                            ax.set_ylabel("Food Item")

                            for bar in bars:
                                ax.text(
                                    bar.get_width() + 1,
                                    bar.get_y() + bar.get_height() / 2,
                                    f"{int(bar.get_width()):,}",
                                    va="center",
                                    color=chart_text_color,
                                    fontsize=9
                                )

                        # Sales chart styling
                        fig.patch.set_facecolor(chart_bg_color)
                        ax.set_facecolor(chart_bg_color)

                        ax.tick_params(colors=chart_text_color)
                        ax.xaxis.label.set_color(chart_text_color)
                        ax.yaxis.label.set_color(chart_text_color)

                        if chart_choice == "Revenue Trend":
                            ax.grid(axis="y", linestyle="--", alpha=0.35, color=chart_grid_color)
                            ax.grid(axis="x", visible=False)
                            ax.yaxis.set_major_formatter(
                                plt.FuncFormatter(lambda value, _: f"₹{value:,.0f}")
                            )
                        else:
                            ax.grid(axis="x", linestyle="--", alpha=0.35, color=chart_grid_color)
                            ax.grid(axis="y", visible=False)

                        for spine in ax.spines.values():
                            spine.set_visible(False)

                        plt.tight_layout()
                        st.pyplot(fig, use_container_width=True)
                        plt.close(fig)

                        st.caption("Sales figures are based on simulated demonstration data.")

                elif analysis_group == "Student Feedback":

                    review_data = filtered_reviews.copy()

                    numeric_columns = [
                        "rating", "taste_rating", "portion_rating", "value_for_money"
                    ]
                    for column in numeric_columns:
                        if column in review_data.columns:
                            review_data[column] = pd.to_numeric(
                                review_data[column], errors="coerce"
                            )

                    required_columns = {
                        "Rating Distribution": ["rating"],
                        "Outlet Satisfaction": ["outlet_name", "rating"],
                        "Feedback Dimension Analysis": [
                            "taste_rating", "portion_rating", "value_for_money"
                        ],
                        "Student Recommendation Analysis": ["would_recommend"],
                        "Rating Trends Over Time": ["review_date", "rating"],
                        "Outlet Rating Heatmap": [
                            "outlet_name", "rating", "taste_rating",
                            "portion_rating", "value_for_money"
                        ],
                        "Taste vs Value for Money": ["taste_rating", "value_for_money"],
                        "Most Reviewed Food Items": ["item_id"]
                    }

                    missing = [
                        col for col in required_columns[chart_choice]
                        if col not in review_data.columns
                    ]

                    if missing:
                        st.error(
                            "Required column(s) missing from student_reviews.csv: "
                            + ", ".join(missing)
                        )
                    elif review_data.empty:
                        st.warning("No student reviews available for the selected filters.")
                    else:
                        fig, ax = plt.subplots(figsize=(12, 6))
                        fig.patch.set_facecolor(chart_bg_color)
                        ax.set_facecolor(chart_bg_color)

                        # Rating distribution
                        if chart_choice == "Rating Distribution":
                            data = review_data[review_data["rating"].between(1, 5)]
                            if data.empty:
                                st.warning("No valid ratings found.")
                            else:
                                counts = data["rating"].round().value_counts().reindex(
                                    [1, 2, 3, 4, 5], fill_value=0
                                )
                                bars = ax.bar(
                                    ["⭐ 1", "⭐ 2", "⭐ 3", "⭐ 4", "⭐ 5"],
                                    counts.values,
                                    color=["#FC8D62", "#FDCB6E", "#A8DADC", "#66C2A5", "#6C9BCF"]
                                )
                                ax.set_title("Student Food Rating Distribution", color=chart_text_color, fontsize=16, fontweight="bold", pad=20)
                                ax.set_xlabel("Star Rating")
                                ax.set_ylabel("Number of Reviews")
                                for bar in bars:
                                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                                            f"{int(bar.get_height())}", ha="center", color=chart_text_color)
                                st.metric("Total Reviews", len(data))
                                st.metric("Average Rating", f"{data['rating'].mean():.2f} / 5 ⭐")

                        # Outlet satisfaction
                        elif chart_choice == "Outlet Satisfaction":
                            data = review_data.dropna(subset=["outlet_name", "rating"])
                            chart_data = data.groupby("outlet_name")["rating"].mean().sort_values()
                            if chart_data.empty:
                                st.warning("No outlet rating data available.")
                            else:
                                bars = ax.barh(chart_data.index, chart_data.values,
                                               color=plt.cm.viridis(np.linspace(0.25, 0.85, len(chart_data))))
                                ax.set_title("Average Student Satisfaction by Outlet", color=chart_text_color, fontsize=16, fontweight="bold", pad=20)
                                ax.set_xlabel("Average Rating")
                                ax.set_ylabel("Outlet")
                                ax.set_xlim(0, 5.5)
                                for bar in bars:
                                    ax.text(bar.get_width()+0.05, bar.get_y()+bar.get_height()/2,
                                            f"{bar.get_width():.2f}", va="center", color=chart_text_color)

                        # Student recommendation analysis
                        elif chart_choice == "Student Recommendation Analysis":
                            values = review_data["would_recommend"].dropna().astype(str).str.strip().str.lower()
                            values = values.replace({"true": "yes", "1": "yes", "false": "no", "0": "no", "y": "yes", "n": "no"})
                            counts = values.value_counts()
                            if counts.empty:
                                st.warning("No recommendation responses available.")
                            else:
                                labels = [str(x).title() for x in counts.index]
                                wedges, texts, autotexts = ax.pie(
                                    counts.values, labels=labels, autopct="%1.1f%%", startangle=90,
                                    colors=["#66C2A5", "#FC8D62", "#A78BFA"],
                                    wedgeprops={"width": 0.42, "edgecolor": chart_edge_color, "linewidth": 2},
                                    textprops={"color": "white"}
                                )
                                for text in autotexts:
                                    text.set_color(chart_text_color)
                                ax.text(0, 0, f"{counts.sum()}\nResponses", ha="center", va="center", color=chart_text_color, fontsize=15, fontweight="bold")
                                ax.set_title("Would Students Recommend This Food?", color=chart_text_color, fontsize=16, fontweight="bold", pad=20)

                        # Rating trends over time
                        elif chart_choice == "Rating Trends Over Time":
                            data = review_data.copy()
                            data["review_date"] = pd.to_datetime(data["review_date"], errors="coerce")
                            data = data.dropna(subset=["review_date", "rating"])
                            chart_data = data.groupby(data["review_date"].dt.date)["rating"].mean()
                            if chart_data.empty:
                                st.warning("No valid dated ratings available.")
                            else:
                                ax.plot(pd.to_datetime(chart_data.index), chart_data.values,
                                        color="#66C2A5", marker="o", linewidth=2.5)
                                ax.fill_between(pd.to_datetime(chart_data.index), chart_data.values,
                                                color="#66C2A5", alpha=0.12)
                                ax.set_title("Average Student Rating Over Time", color=chart_text_color, fontsize=16, fontweight="bold", pad=20)
                                ax.set_xlabel("Review Date")
                                ax.set_ylabel("Average Rating")
                                ax.set_ylim(0, 5.5)
                                fig.autofmt_xdate()

                        # Most reviewed food items
                        elif chart_choice == "Most Reviewed Food Items":
                            chart_data = review_data.groupby("item_id").size().sort_values(ascending=False).head(10)
                            if chart_data.empty:
                                st.warning("No food item review data available.")
                            else:
                                names = menu[["item_id", "item_name"]].drop_duplicates("item_id")
                                chart_data = chart_data.rename("review_count").reset_index().merge(names, on="item_id", how="left")
                                chart_data["item_name"] = chart_data["item_name"].fillna(chart_data["item_id"].astype(str))
                                chart_data = chart_data.sort_values("review_count")
                                bars = ax.barh(chart_data["item_name"], chart_data["review_count"],
                                               color=plt.cm.viridis(np.linspace(0.25, 0.85, len(chart_data))))
                                ax.set_title("Top 10 Most Reviewed Food Items", color=chart_text_color, fontsize=16, fontweight="bold", pad=20)
                                ax.set_xlabel("Number of Reviews")
                                ax.set_ylabel("Food Item")
                                for bar in bars:
                                    ax.text(bar.get_width()+0.1, bar.get_y()+bar.get_height()/2,
                                            f"{int(bar.get_width())}", va="center", color=chart_text_color)

                        # Common feedback chart styling
                        if fig.axes and ax.has_data():
                            ax.tick_params(colors=chart_text_color)
                            ax.xaxis.label.set_color(chart_text_color)
                            ax.yaxis.label.set_color(chart_text_color)
                            if chart_choice not in ["Student Recommendation Analysis", "Outlet Rating Heatmap"]:
                                ax.grid(axis="y", linestyle="--", alpha=0.35, color=chart_grid_color)
                                if chart_choice in ["Outlet Satisfaction", "Most Reviewed Food Items"]:
                                    ax.grid(axis="x", linestyle="--", alpha=0.35, color=chart_grid_color)
                            for spine in ax.spines.values():
                                spine.set_visible(False)
                            plt.tight_layout()
                            st.pyplot(fig, use_container_width=True)

                        plt.close(fig)
                        st.caption("Student feedback is based on simulated demonstration data.")

                elif analysis_group == "Operational Analytics":

                    operation_data = filtered_operations.copy()

                    required_columns = {
                        "Daily Footfall Trend": ["date", "estimated_footfall"],
                        "Outlet-wise Footfall Comparison": ["outlet_name", "estimated_footfall"],
                        "Day-wise Footfall Heatmap": ["date", "outlet_name", "estimated_footfall"],
                        "Outlet-wise Average Waiting Time": ["outlet_name", "average_wait_time_min"],
                        "Waiting Time Trend": ["date", "average_wait_time_min"],
                        "Footfall vs Waiting Time": ["estimated_footfall", "average_wait_time_min"]
                    }

                    missing = [
                        column for column in required_columns[chart_choice]
                        if column not in operation_data.columns
                    ]

                    if missing:
                        st.error(
                            "Required column(s) missing from outlet_daily_operations.csv: "
                            + ", ".join(missing)
                        )
                    elif operation_data.empty:
                        st.warning("No operational data available for the selected filters.")
                    else:
                        operation_data["estimated_footfall"] = pd.to_numeric(
                            operation_data["estimated_footfall"], errors="coerce"
                        )
                        operation_data["average_wait_time_min"] = pd.to_numeric(
                            operation_data["average_wait_time_min"], errors="coerce"
                        )
                        operation_data["date"] = pd.to_datetime(
                            operation_data["date"], errors="coerce"
                        )

                        fig, ax = plt.subplots(figsize=(12, 6))
                        fig.patch.set_facecolor(chart_bg_color)
                        ax.set_facecolor(chart_bg_color)

                        # Daily footfall trend
                        if chart_choice == "Daily Footfall Trend":
                            data = operation_data.dropna(
                                subset=["date", "estimated_footfall"]
                            )
                            chart_data = data.groupby("date")["estimated_footfall"].sum().sort_index()

                            if chart_data.empty:
                                st.warning("No valid daily footfall records available.")
                            else:
                                ax.plot(
                                    chart_data.index,
                                    chart_data.values,
                                    color="#66C2A5",
                                    marker="o",
                                    linewidth=2.5,
                                    markersize=5
                                )
                                ax.fill_between(
                                    chart_data.index,
                                    chart_data.values,
                                    color="#66C2A5",
                                    alpha=0.12
                                )
                                ax.set_title(
                                    "Daily Campus Footfall Trend",
                                    color=chart_text_color, fontsize=16, fontweight="bold", pad=20
                                )
                                ax.set_xlabel("Date")
                                ax.set_ylabel("Estimated Student Footfall")
                                fig.autofmt_xdate()
                                st.metric("Total Recorded Footfall", f"{int(chart_data.sum()):,}")

                        # Outlet-wise footfall comparison
                        elif chart_choice == "Outlet-wise Footfall Comparison":
                            data = operation_data.dropna(
                                subset=["outlet_name", "estimated_footfall"]
                            )
                            chart_data = data.groupby("outlet_name")["estimated_footfall"].mean().sort_values()

                            if chart_data.empty:
                                st.warning("No outlet footfall records available.")
                            else:
                                bars = ax.barh(
                                    chart_data.index,
                                    chart_data.values,
                                    color=plt.cm.viridis(
                                        np.linspace(0.25, 0.85, len(chart_data))
                                    )
                                )
                                ax.set_title(
                                    "Average Daily Footfall by Outlet",
                                    color=chart_text_color, fontsize=16, fontweight="bold", pad=20
                                )
                                ax.set_xlabel("Average Daily Student Footfall")
                                ax.set_ylabel("Outlet")
                                for bar in bars:
                                    ax.text(
                                        bar.get_width() + 1,
                                        bar.get_y() + bar.get_height() / 2,
                                        f"{bar.get_width():.0f}",
                                        va="center", color=chart_text_color, fontsize=9
                                    )

                        # Day-wise footfall heatmap
                        elif chart_choice == "Day-wise Footfall Heatmap":
                            data = operation_data.dropna(
                                subset=["date", "outlet_name", "estimated_footfall"]
                            ).copy()
                            data["day"] = data["date"].dt.day_name()
                            day_order = [
                                "Monday", "Tuesday", "Wednesday", "Thursday",
                                "Friday", "Saturday", "Sunday"
                            ]
                            heat_data = data.pivot_table(
                                index="outlet_name",
                                columns="day",
                                values="estimated_footfall",
                                aggfunc="mean"
                            ).reindex(columns=day_order)
                            heat_data = heat_data.dropna(how="all")

                            if heat_data.empty:
                                st.warning("No weekday footfall records available.")
                            else:
                                matrix = heat_data.to_numpy(dtype=float)
                                image = ax.imshow(matrix, aspect="auto", cmap="YlGnBu")
                                ax.set_xticks(
                                    range(len(heat_data.columns)),
                                    heat_data.columns,
                                    rotation=25,
                                    ha="right"
                                )
                                ax.set_yticks(range(len(heat_data.index)), heat_data.index)
                                ax.set_title(
                                    "Average Footfall by Outlet and Day",
                                    color=chart_text_color, fontsize=16, fontweight="bold", pad=20
                                )
                                ax.set_xlabel("Day of Week")
                                ax.set_ylabel("Outlet")
                                for i in range(matrix.shape[0]):
                                    for j in range(matrix.shape[1]):
                                        if np.isfinite(matrix[i, j]):
                                            ax.text(
                                                j, i, f"{matrix[i, j]:.0f}",
                                                ha="center", va="center",
                                                color=chart_text_color if matrix[i, j] < np.nanmean(matrix) else "#0e1117",
                                                fontsize=8
                                            )
                                colorbar = fig.colorbar(image, ax=ax)
                                colorbar.set_label("Average Footfall", color=chart_text_color)
                                colorbar.ax.yaxis.set_tick_params(color=chart_text_color)
                                plt.setp(colorbar.ax.get_yticklabels(), color=chart_text_color)

                        # Outlet-wise average waiting time
                        elif chart_choice == "Outlet-wise Average Waiting Time":
                            data = operation_data.dropna(
                                subset=["outlet_name", "average_wait_time_min"]
                            )
                            chart_data = data.groupby("outlet_name")["average_wait_time_min"].mean().sort_values()

                            if chart_data.empty:
                                st.warning("No outlet waiting-time records available.")
                            else:
                                bars = ax.barh(
                                    chart_data.index,
                                    chart_data.values,
                                    color=plt.cm.plasma(
                                        np.linspace(0.25, 0.85, len(chart_data))
                                    )
                                )
                                ax.set_title(
                                    "Average Waiting Time by Outlet",
                                    color=chart_text_color, fontsize=16, fontweight="bold", pad=20
                                )
                                ax.set_xlabel("Average Waiting Time (Minutes)")
                                ax.set_ylabel("Outlet")
                                for bar in bars:
                                    ax.text(
                                        bar.get_width() + 0.1,
                                        bar.get_y() + bar.get_height() / 2,
                                        f"{bar.get_width():.1f} min",
                                        va="center", color=chart_text_color, fontsize=9
                                    )

                        # Waiting time trend
                        elif chart_choice == "Waiting Time Trend":
                            data = operation_data.dropna(
                                subset=["date", "average_wait_time_min"]
                            )
                            chart_data = data.groupby("date")["average_wait_time_min"].mean().sort_index()

                            if chart_data.empty:
                                st.warning("No dated waiting-time records available.")
                            else:
                                ax.plot(
                                    chart_data.index,
                                    chart_data.values,
                                    color="#FDCB6E",
                                    marker="o",
                                    linewidth=2.5,
                                    markersize=5
                                )
                                ax.fill_between(
                                    chart_data.index,
                                    chart_data.values,
                                    color="#FDCB6E",
                                    alpha=0.12
                                )
                                ax.set_title(
                                    "Average Waiting Time Trend",
                                    color=chart_text_color, fontsize=16, fontweight="bold", pad=20
                                )
                                ax.set_xlabel("Date")
                                ax.set_ylabel("Average Waiting Time (Minutes)")
                                ax.set_ylim(bottom=0)
                                fig.autofmt_xdate()

                        # Footfall versus waiting time
                        elif chart_choice == "Footfall vs Waiting Time":
                            data = operation_data.dropna(
                                subset=["estimated_footfall", "average_wait_time_min"]
                            )

                            if data.empty:
                                st.warning("No matching footfall and waiting-time records available.")
                            else:
                                ax.scatter(
                                    data["estimated_footfall"],
                                    data["average_wait_time_min"],
                                    color="#A78BFA",
                                    alpha=0.7,
                                    edgecolors=chart_text_color,
                                    linewidths=0.4,
                                    s=60
                                )
                                ax.set_title(
                                    "Student Footfall vs Average Waiting Time",
                                    color=chart_text_color, fontsize=16, fontweight="bold", pad=20
                                )
                                ax.set_xlabel("Estimated Student Footfall")
                                ax.set_ylabel("Average Waiting Time (Minutes)")
                                ax.set_ylim(bottom=0)

                        # Common operational chart styling
                        if ax.has_data():
                            ax.tick_params(colors=chart_text_color)
                            ax.xaxis.label.set_color(chart_text_color)
                            ax.yaxis.label.set_color(chart_text_color)
                            if chart_choice == "Outlet-wise Footfall Comparison":
                                ax.grid(axis="x", linestyle="--", alpha=0.35, color=chart_grid_color)
                            elif chart_choice == "Outlet-wise Average Waiting Time":
                                ax.grid(axis="x", linestyle="--", alpha=0.35, color=chart_grid_color)
                            elif chart_choice != "Day-wise Footfall Heatmap":
                                ax.grid(axis="y", linestyle="--", alpha=0.35, color=chart_grid_color)
                            for spine in ax.spines.values():
                                spine.set_visible(False)
                            plt.tight_layout()
                            st.pyplot(fig, use_container_width=True)

                        plt.close(fig)
                        st.caption(
                            "Operational metrics are based on simulated demonstration data. "
                            "Footfall values represent estimated daily student visits."
                        )

    # Menu overview with search and sorting
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

# Footer
st.divider()

st.caption(
    "Christ MenuMind | Campus Food Intelligence Dashboard"
)
