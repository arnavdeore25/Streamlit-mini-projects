# Christ MenuMind

Christ MenuMind is an interactive campus food analytics dashboard built with Python and Streamlit. It helps users explore food outlets, menu items, prices, ratings, sales, student feedback, and operational metrics across multiple campus blocks.

> **Demo data notice:** All menu details, outlet information, prices, sales, reviews, footfall, and operating metrics in this project are synthetic. They are not verified records for real campus outlets and should not be presented as real-world results.

## Features

- Filter by campus block, outlet, and food preference
- Switch between dark and light dashboard themes
- View a KPI-only campus overview
- Explore menu, pricing, sales, feedback, and operations
- Compare outlets and analyse category distributions
- Search and sort menu items by outlet, name, price, or rating
- Reset filters directly from the sidebar
- Load data safely with clear errors for missing or invalid CSV files


## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib

## Project Structure

```text
Christ MenuMind/
├── data/
│   ├── blocks.csv
│   ├── outlets.csv
│   ├── menu_items.csv
│   ├── sales_data.csv
│   ├── student_preferences.csv
│   ├── student_reviews.csv
│   ├── price_history.csv
│   ├── outlet_daily_operations.csv
│   └── README.md
├── .streamlit/
│   └── config.toml
├── analytics.py
├── config.py
├── dashboard_header.py
├── data_loader.py
├── footer.py
├── kpis.py
├── main.py
├── menu_explorer.py
├── sidebar.py
├── style.css
├── style_light.css
└── README.md
```

## Data Files

| File | Purpose |
| --- | --- |
| `blocks.csv` | Campus blocks |
| `outlets.csv` | Outlet names and block mappings |
| `menu_items.csv` | Menu items, prices, categories, ratings, calories, and preparation details |
| `sales_data.csv` | Simulated daily item-level sales |
| `student_reviews.csv` | Synthetic student feedback |
| `student_preferences.csv` | Synthetic profiles for recommender testing |
| `price_history.csv` | Illustrative historical price snapshots |
| `outlet_daily_operations.csv` | Simulated footfall, waiting time, stockouts, and waste |

The data currently covers 60 simulated days ending 17 November 2026.

## Food Data Rules

- Non-vegetarian entries are limited to chicken-only items.
- The project does not include fish, seafood, mutton, beef, or pork.
- Menu labels do not guarantee real outlet recipes or allergen-free preparation.
- Vegetarian status and egg-free status should be confirmed with an actual outlet before use.
- The Chicken Caesar salad entry is explicitly bacon-free.

## Notes

- The app reads the CSV files from `data/` using `config.py`.
- Missing or unreadable data files produce an error message in the dashboard.
- Dashboard styling is controlled by `style.css` and `style_light.css`.
