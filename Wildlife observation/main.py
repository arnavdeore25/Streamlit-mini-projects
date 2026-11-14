import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(page_title="Wildlife Monitoring and Animal Behaviour Dashboard", layout="wide")

st.title("Wildlife Monitoring and Animal Behaviour Dashboard")
st.write("This dashboard helps researchers explore animal observations collected from different zones of the forest reserve. Use the filters in the sidebar to study species, movement patterns and physical characteristics.")

data = pd.read_csv("wildlife_observations.csv")
data["Observation_Date"] = pd.to_datetime(data["Observation_Date"])

st.subheader("First 10 Observations")
st.dataframe(data.head(10))

st.sidebar.header("Filters")

zones = ["All Zones"] + sorted(data["Forest_Zone"].unique().tolist())
selected_zone = st.sidebar.selectbox("Select Forest Zone", zones)

animals = sorted(data["Animal"].unique().tolist())
selected_animals = st.sidebar.multiselect("Select Animal Species", animals, default=animals)

if selected_zone == "All Zones":
    filtered = data.copy()
else:
    filtered = data[data["Forest_Zone"] == selected_zone]

if len(selected_animals) > 0:
    filtered = filtered[filtered["Animal"].isin(selected_animals)]
else:
    filtered = filtered.iloc[0:0]

st.subheader("Summary")
c1, c2, c3 = st.columns(3)
c1.metric("Total Observations", len(filtered))
c2.metric("Unique Species", filtered["Animal"].nunique())
if len(filtered) > 0:
    c3.metric("Average Group Size", round(filtered["Group_Size"].mean(), 2))
else:
    c3.metric("Average Group Size", 0)

if len(filtered) == 0:
    st.warning("No observations match the selected filters. Please select at least one species.")
    st.stop()

colours = plt.cm.tab10(np.linspace(0, 1, len(animals)))
colour_map = {}
for i in range(len(animals)):
    colour_map[animals[i]] = colours[i]

tab1, tab2, tab3, tab4 = st.tabs(["Animal Population", "Animal Characteristics", "Observation Trends", "3D Wildlife Analysis"])

with tab1:
    st.subheader("Animal Sightings")
    counts = filtered["Animal"].value_counts().sort_index()

    left, right = st.columns(2)

    with left:
        fig1, ax1 = plt.subplots()
        ax1.bar(counts.index, counts.values, color=[colour_map[a] for a in counts.index])
        ax1.set_title("Number of Observations per Animal Species")
        ax1.set_xlabel("Animal Species")
        ax1.set_ylabel("Number of Observations")
        plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")
        st.pyplot(fig1)

    with right:
        table = counts.reset_index()
        table.columns = ["Animal Species", "Observations"]
        st.dataframe(table)

    with st.container():
        st.subheader("Animal Category Distribution")
        category = filtered["Category"].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(category.values, labels=category.index, autopct="%1.1f%%", startangle=90)
        ax2.set_title("Mammals vs Birds")
        ax2.axis("equal")
        st.pyplot(fig2)

with tab2:
    st.subheader("Animal Weight Distribution")
    bins = st.slider("Number of bins", 5, 50, 20)
    fig3, ax3 = plt.subplots()
    ax3.hist(filtered["Weight_kg"], bins=bins, color="seagreen", edgecolor="black")
    ax3.set_title("Distribution of Animal Weights")
    ax3.set_xlabel("Weight (kg)")
    ax3.set_ylabel("Number of Animals")
    st.pyplot(fig3)

    st.subheader("Age vs Movement Speed")
    fig4, ax4 = plt.subplots()
    for animal in sorted(filtered["Animal"].unique()):
        subset = filtered[filtered["Animal"] == animal]
        ax4.scatter(subset["Age_Years"], subset["Speed_kmph"], label=animal, color=colour_map[animal], s=40)
    ax4.set_title("Relationship between Age and Movement Speed")
    ax4.set_xlabel("Age (years)")
    ax4.set_ylabel("Speed (km/h)")
    ax4.legend(title="Species")
    st.pyplot(fig4)

with tab3:
    st.subheader("Wildlife Observation Trends")
    monthly = filtered.groupby(filtered["Observation_Date"].dt.to_period("M")).size()
    monthly.index = monthly.index.astype(str)

    fig5, ax5 = plt.subplots()
    ax5.plot(monthly.index, monthly.values, marker="o", linestyle="-", color="darkorange")
    ax5.set_title("Monthly Animal Sightings")
    ax5.set_xlabel("Month")
    ax5.set_ylabel("Number of Sightings")
    ax5.grid(True, linestyle="--", alpha=0.5)
    plt.setp(ax5.get_xticklabels(), rotation=45, ha="right")
    st.pyplot(fig5)

with tab4:
    st.subheader("3D Wildlife Analysis")
    view = st.slider("Rotate view angle", 0, 360, 45)

    col1, col2 = st.columns(2)

    with col1:
        st.write("Animal Physical Characteristics")
        fig6 = plt.figure()
        ax6 = fig6.add_subplot(111, projection="3d")
        for animal in sorted(filtered["Animal"].unique()):
            subset = filtered[filtered["Animal"] == animal]
            ax6.scatter(subset["Age_Years"], subset["Weight_kg"], subset["Speed_kmph"], label=animal, color=colour_map[animal], s=30)
        ax6.set_xlabel("Age (years)")
        ax6.set_ylabel("Weight (kg)")
        ax6.set_zlabel("Speed (km/h)")
        ax6.set_title("Age, Weight and Speed of Animals")
        ax6.legend(fontsize=7)
        ax6.view_init(elev=20, azim=view)
        st.pyplot(fig6)

    with col2:
        st.write("Animal Sightings Across Forest Zones")
        grouped = filtered.groupby(["Forest_Zone", "Animal"]).size().reset_index(name="Count")
        zone_list = sorted(filtered["Forest_Zone"].unique().tolist())
        animal_list = sorted(filtered["Animal"].unique().tolist())

        xpos = []
        ypos = []
        dz = []
        bar_colours = []
        for i in range(len(zone_list)):
            for j in range(len(animal_list)):
                row = grouped[(grouped["Forest_Zone"] == zone_list[i]) & (grouped["Animal"] == animal_list[j])]
                if len(row) > 0:
                    value = int(row["Count"].values[0])
                else:
                    value = 0
                xpos.append(i)
                ypos.append(j)
                dz.append(value)
                bar_colours.append(colour_map[animal_list[j]])

        zpos = np.zeros(len(dz))

        fig7 = plt.figure()
        ax7 = fig7.add_subplot(111, projection="3d")
        ax7.bar3d(xpos, ypos, zpos, 0.5, 0.5, dz, color=bar_colours, shade=True)
        ax7.set_xticks(range(len(zone_list)))
        ax7.set_xticklabels(zone_list, rotation=20, fontsize=7)
        ax7.set_yticks(range(len(animal_list)))
        ax7.set_yticklabels(animal_list, fontsize=7)
        ax7.set_xlabel("Forest Zone")
        ax7.set_ylabel("Animal Species")
        ax7.set_zlabel("Number of Observations")
        ax7.set_title("Observations across Forest Zones")
        ax7.view_init(elev=25, azim=view)
        st.pyplot(fig7)

    with st.expander("View Filtered Dataset"):
        st.dataframe(filtered)
        st.write("Total rows after filtering:", len(filtered))
