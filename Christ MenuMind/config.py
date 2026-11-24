
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

DATA_FILES = {
    "blocks": "blocks.csv",
    "outlets": "outlets.csv",
    "menu": "menu_items.csv",
    "sales": "sales_data.csv",
    "student_reviews": "student_reviews.csv",
    "operations": "outlet_daily_operations.csv",
}


def read_stylesheet(path: Path) -> str:
    """Read an optional CSS file without failing when it is absent."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""
