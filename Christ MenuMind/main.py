
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
student_reviews = pd.read_csv("data/student_reviews.csv")
operations = pd.read_csv("data/outlet_daily_operations.csv")

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

chart_choice = st.radio(
    "Select Analysis",
    chart_options[analysis_group],
    horizontal=True
)

st.divider()
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
            color="white"
        )

        ax.set_xlabel("Number of Food Items")
        ax.set_ylabel("Category")

        for bar in bars:
            ax.text(
                bar.get_width() + 1,
                bar.get_y() + bar.get_height() / 2,
                int(bar.get_width()),
                va="center",
                color="white"
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
                "edgecolor": "#0e1117",
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
            color="white"
        )

        ax.set_title(
            "Vegetarian vs Chicken Distribution",
            fontsize=16,
            fontweight="bold",
            color="white",
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

        legend.get_title().set_color("white")

        for text in legend.get_texts():
            text.set_color("white")

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
            color="white",
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
                color="white",
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
            color="white",
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

        legend.get_title().set_color("white")

        for text in legend.get_texts():
            text.set_color("white")

    # Common chart styling
    if fig is not None:

        fig.patch.set_facecolor("#0e1117")
        ax.set_facecolor("#0e1117")

        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")

        if chart_choice != "Vegetarian vs Chicken":
            ax.grid(axis="y", linestyle="--", alpha=0.2)
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
                color="white",
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
                    color="white",
                    fontsize=9
                )

        # Food price distribution
        elif chart_choice == "Food Price Distribution":

            fig, ax = plt.subplots(figsize=(11, 6))

            ax.hist(
                price_data["price_inr"],
                bins=15,
                color="#66C2A5",
                edgecolor="#0e1117",
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
                color="white",
                pad=20
            )

            ax.set_xlabel("Food Price (₹)")
            ax.set_ylabel("Number of Food Items")

            ax.legend(
                facecolor="#0e1117",
                edgecolor="none",
                labelcolor="white"
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
                color="white",
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
                color="white",
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
                    color="white",
                    fontsize=9
                )

        # Pricing chart styling
        if fig is not None:

            fig.patch.set_facecolor("#0e1117")
            ax.set_facecolor("#0e1117")

            ax.tick_params(colors="white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")

            ax.grid(
                axis="y",
                linestyle="--",
                alpha=0.2
            )

            if chart_choice == "Outlet-wise Average Pricing":
                ax.grid(axis="x", linestyle="--", alpha=0.2)
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
                color="white",
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
                color="white",
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
                    color="white",
                    fontsize=9
                )

        # Sales chart styling
        fig.patch.set_facecolor("#0e1117")
        ax.set_facecolor("#0e1117")

        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")

        if chart_choice == "Revenue Trend":
            ax.grid(axis="y", linestyle="--", alpha=0.2)
            ax.grid(axis="x", visible=False)
            ax.yaxis.set_major_formatter(
                plt.FuncFormatter(lambda value, _: f"₹{value:,.0f}")
            )
        else:
            ax.grid(axis="x", linestyle="--", alpha=0.2)
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
        fig.patch.set_facecolor("#0e1117")
        ax.set_facecolor("#0e1117")

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
                ax.set_title("Student Food Rating Distribution", color="white", fontsize=16, fontweight="bold", pad=20)
                ax.set_xlabel("Star Rating")
                ax.set_ylabel("Number of Reviews")
                for bar in bars:
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                            f"{int(bar.get_height())}", ha="center", color="white")
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
                ax.set_title("Average Student Satisfaction by Outlet", color="white", fontsize=16, fontweight="bold", pad=20)
                ax.set_xlabel("Average Rating")
                ax.set_ylabel("Outlet")
                ax.set_xlim(0, 5.5)
                for bar in bars:
                    ax.text(bar.get_width()+0.05, bar.get_y()+bar.get_height()/2,
                            f"{bar.get_width():.2f}", va="center", color="white")
                    
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
                    wedgeprops={"width": 0.42, "edgecolor": "#0e1117", "linewidth": 2},
                    textprops={"color": "white"}
                )
                for text in autotexts:
                    text.set_color("white")
                ax.text(0, 0, f"{counts.sum()}\nResponses", ha="center", va="center", color="white", fontsize=15, fontweight="bold")
                ax.set_title("Would Students Recommend This Food?", color="white", fontsize=16, fontweight="bold", pad=20)

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
                ax.set_title("Average Student Rating Over Time", color="white", fontsize=16, fontweight="bold", pad=20)
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
                ax.set_title("Top 10 Most Reviewed Food Items", color="white", fontsize=16, fontweight="bold", pad=20)
                ax.set_xlabel("Number of Reviews")
                ax.set_ylabel("Food Item")
                for bar in bars:
                    ax.text(bar.get_width()+0.1, bar.get_y()+bar.get_height()/2,
                            f"{int(bar.get_width())}", va="center", color="white")

        # Common feedback chart styling
        if fig.axes and ax.has_data():
            ax.tick_params(colors="white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            if chart_choice not in ["Student Recommendation Analysis", "Outlet Rating Heatmap"]:
                ax.grid(axis="y", linestyle="--", alpha=0.2)
                if chart_choice in ["Outlet Satisfaction", "Most Reviewed Food Items"]:
                    ax.grid(axis="x", linestyle="--", alpha=0.2)
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
        fig.patch.set_facecolor("#0e1117")
        ax.set_facecolor("#0e1117")

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
                    color="white", fontsize=16, fontweight="bold", pad=20
                )
                ax.set_xlabel("Date")
                ax.set_ylabel("Estimated Student Footfall")
                fig.autofmt_xdate()
                st.metric("Total Recorded Footfall", f"{int(chart_data.sum()):,}")

        # Outlet-wise footfall comparison


        # Common operational chart styling
        if ax.has_data():
            ax.tick_params(colors="white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            if chart_choice == "Outlet-wise Footfall Comparison":
                ax.grid(axis="x", linestyle="--", alpha=0.2)
            elif chart_choice == "Outlet-wise Average Waiting Time":
                ax.grid(axis="x", linestyle="--", alpha=0.2)
            elif chart_choice != "Day-wise Footfall Heatmap":
                ax.grid(axis="y", linestyle="--", alpha=0.2)
            for spine in ax.spines.values():
                spine.set_visible(False)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)

        plt.close(fig)
        st.caption(
            "Operational metrics are based on simulated demonstration data. "
            "Footfall values represent estimated daily student visits."
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
