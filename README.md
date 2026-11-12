# Steve's World

A beginner-friendly Streamlit dashboard themed around Minecraft and the iconic character Steve. The app presents a simple interactive experience for browsing Steve's story, reviewing player profiles, exploring sample player data, and registering interest in joining the world.

## Features

- Home page with an introduction and themed interface
- Story section covering Steve's background and interesting facts
- Player profile area with category-based details and selectable game modes
- Data exploration page with filtering on world and game mode
- Registration form using multiple Streamlit widgets such as text inputs, radio buttons, selects, multiselects, sliders, and checkboxes
- Pixel-art asset included for a custom Minecraft-inspired design

## Project Structure

```text
Streamlit-mini-projects/
├── app.py                  # Main Streamlit application
├── minecraft_players.csv   # Sample dataset used in the dashboard
├── requirements.txt        # Python dependencies
├── assets/
│   └── steve_pixel.png     # Steve avatar image
├── README.md               # Project documentation
└── .gitattributes
```

## Tech Stack

- Python
- Streamlit
- Pandas


## Notes

- Keep `app.py` and `minecraft_players.csv` in the same folder when running the app.
- Keep the `assets` folder alongside `app.py` so the Steve image loads correctly.
- The app is intentionally simple and educational, making it a great example for learning Streamlit UI components and data display.

## License

This project is provided for educational and personal use.
