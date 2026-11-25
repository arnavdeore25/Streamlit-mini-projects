from typing import Dict
from pathlib import Path

import pandas as pd
import streamlit as st

from config import DATA_FILES

@st.cache_data(ttl=300, show_spinner="Loading campus data...")
def load_data(data_dir: Path) -> Dict[str, pd.DataFrame]:
    """Load all required CSV files and normalize selected columns."""
    missing_files = [
        filename for filename in DATA_FILES.values()
        if not (data_dir / filename).is_file()
    ]
    if missing_files:
        missing_list = "\\n".join(f"• {name}" for name in missing_files)
        raise FileNotFoundError(
            f"Missing required CSV file(s) in '{data_dir}':\\n{missing_list}"
        )

    data = {
        key: pd.read_csv(data_dir / filename)
        for key, filename in DATA_FILES.items()
    }

    for dataset_name in ("operations", "student_reviews"):
        frame = data[dataset_name]
        frame.columns = (
            frame.columns.astype(str)
            .str.replace("\\ufeff", "", regex=False)
            .str.strip()
            .str.lower()
        )

    reviews = data["student_reviews"]
    if "value_for_money" not in reviews.columns and "value_for_money_rating" in reviews.columns:
        data["student_reviews"] = reviews.rename(
            columns={"value_for_money_rating": "value_for_money"}
        )

    if "date" in data["operations"].columns:
        data["operations"]["date"] = pd.to_datetime(
            data["operations"]["date"], errors="coerce"
        )

    return data
