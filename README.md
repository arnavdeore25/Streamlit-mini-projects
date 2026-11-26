# Streamlit Mini Projects

A collection of interactive Python and Streamlit mini-projects focused on dashboards, data exploration, and beginner-friendly web applications.

## Projects

| Project | Description |
| --- | --- |
| [Christ MenuMind](./Christ%20MenuMind) | A campus food intelligence dashboard for exploring outlets, menus, pricing, sales, feedback, and operations using synthetic data. |
| [Steve's World](./SuperHero) | A Minecraft-inspired dashboard with character stories, player profiles, game modes, filtered player data, and a registration form. |
| [Wildlife Observation Dashboard](./Wildlife%20observation) | A forest reserve dashboard for analysing sightings, species, animal characteristics, monthly trends, and 3D visualizations. |

## Features

### Christ MenuMind

- Campus block and outlet filters
- Vegetarian and non-vegetarian filters
- Dark and light themes
- Menu, pricing, sales, feedback, and operational analytics
- Searchable and sortable menu explorer
- Matplotlib visualizations and KPI dashboards

### Steve's World

- Minecraft-themed home page
- Steve's story and profile
- Game mode information
- Player data filtering
- Interactive player registration form

### Wildlife Observation Dashboard

- Forest-zone and species filters
- Observation and average group-size metrics
- Species, category, weight, age, and speed charts
- Monthly sighting trends
- Interactive 3D visualizations

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/arnavdeore25/Streamlit-mini-projects.git
cd Streamlit-mini-projects
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run an app

#### Christ MenuMind

```bash
cd "Christ MenuMind"
streamlit run main.py
```

#### Steve's World

```bash
cd SuperHero
streamlit run app.py
```

#### Wildlife Observation Dashboard

```bash
cd "Wildlife observation"
streamlit run main.py
```

After the app starts, open the local URL displayed in the terminal, usually `http://localhost:8501`.

## Repository Structure

```text
Streamlit-mini-projects/
├── Christ MenuMind/
│   ├── data/                 # Synthetic campus and menu datasets
│   ├── main.py               # Streamlit entry point
│   ├── analytics.py
│   ├── menu_explorer.py
│   └── style.css
├── SuperHero/
│   ├── app.py                # Steve's World Streamlit app
│   ├── assets/
│   ├── minecraft_players.csv
│   └── requirements.txt
├── Wildlife observation/
│   ├── main.py               # Wildlife dashboard entry point
│   ├── wildlife_observations.csv
│   └── requirements.txt
├── requirements.txt
└── README.md
```

## Data Note

The Christ MenuMind datasets are entirely synthetic or simulated. Menu details, outlet performance, sales, ratings, footfall, and operational metrics are demo data and must not be presented as verified real-world campus records.

## License

This repository is intended for educational and personal use.
