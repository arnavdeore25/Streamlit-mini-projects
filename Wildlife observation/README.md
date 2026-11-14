# Wildlife Observation Dashboard

This project is a small Streamlit dashboard for exploring wildlife monitoring data from a forest reserve. It lets users filter by forest zone and animal species, then view summary metrics and charts about sightings, behavior, and animal characteristics.

## Features

- Filter observations by forest zone and species
- View summary statistics for the selected dataset
- Explore counts by species and category
- Analyze weight distribution and age-speed relationships
- Review monthly sighting trends
- Inspect a 3D visualization of wildlife metrics

## Files

- `main.py` – Streamlit app
- `wildlife_observations.csv` – sample wildlife observation dataset

## Run locally

1. Open a terminal in this folder.
2. Install the required packages:
   ```bash
   pip install streamlit pandas numpy matplotlib
   ```
3. Start the app:
   ```bash
   streamlit run main.py or python -m streamlit run main.py
   ```
4. Open the local URL shown in the terminal in your browser.

## Notes

The dashboard reads the CSV file from the same directory as the app, so keep `wildlife_observations.csv` in the project folder when running it.
