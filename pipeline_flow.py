from prefect import flow, task
import pandas as pd
import os
from dotenv import load_dotenv
import sqlite3  

# Load environment variables
load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")

# === Import Extract modules ===
from extract_state_temperatures import extract_state_temperatures
from extract_noaa_summary import extract_noaa_summary
from city_api import fetch_multiple_cities

# === Import Transform modules ===
from transform import (
    transform_state_temperature,
    transform_noaa_events,
    merge_state_panel
)

# === Import Validation modules ===
from validate import (
    validate_state_temp,
    validate_noaa,
    validate_state_panel
)

# === Import Load module ===
from load import save_state_panel


# === Prefect Tasks ===

@task
def task_extract_state_temperatures(data_dir: str) -> pd.DataFrame:
    return extract_state_temperatures(data_dir)

@task
def task_extract_noaa_summary(data_dir: str) -> pd.DataFrame:
    return extract_noaa_summary(data_dir)

@task
def task_fetch_city_weather(api_key: str) -> pd.DataFrame:
    cities = [
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
        "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"
    ]
    return fetch_multiple_cities(api_key, cities)

@task
def task_validate_state_temp(df: pd.DataFrame) -> pd.DataFrame:
    return validate_state_temp(df)

@task
def task_validate_noaa(df: pd.DataFrame) -> pd.DataFrame:
    return validate_noaa(df)

@task
def task_transform_state_temperature(df: pd.DataFrame) -> pd.DataFrame:
    return transform_state_temperature(df)

@task
def task_transform_noaa_events(df: pd.DataFrame) -> pd.DataFrame:
    return transform_noaa_events(df)

@task
def task_merge_state_panel(temp_df: pd.DataFrame, event_df: pd.DataFrame) -> pd.DataFrame:
    return merge_state_panel(temp_df, event_df)

@task
def task_validate_panel(df: pd.DataFrame) -> pd.DataFrame:
    return validate_state_panel(df)

@task
def task_save_panel(df: pd.DataFrame, path: str):
    save_state_panel(df, path)

@task
def task_save_city_weather(df: pd.DataFrame, path: str = "extracted_data/city_weather.csv"):
    df.to_csv(path, index=False)
    print(f"Saved city weather data to {path}")

@task
def task_save_city_to_sql(df: pd.DataFrame, db_path: str = "extracted_data/weather.db"):
    # Clean column names to ensure SQLite compatibility
    def clean_col(col, index):
        if not col or str(col).strip() == "":
            return f"col_{index}"
        cleaned = (
            str(col).strip()
            .replace(" ", "_")
            .replace("-", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("/", "_")
            .replace(".", "")
            .replace("[", "")
            .replace("]", "")
        )
        # Ensure column doesn't start with a digit
        if cleaned[0].isdigit():
            cleaned = f"col_{index}_{cleaned}"
        return cleaned

    df.columns = [clean_col(col, i) for i, col in enumerate(df.columns)]

    conn = sqlite3.connect(db_path)
    df.to_sql("city_weather", conn, if_exists="replace", index=False)
    conn.close()

    print(f"Saved city weather data to {db_path} (table: city_weather)")
    print("Columns:", df.columns.tolist())
    print(df.head())

# === Main Flow ===

@flow(name="weather_etl_pipeline")
def main_pipeline(
    data_dir: str = "data/",
    output_path: str = "extracted_data/state_panel.csv",
    api_key: str = ""
):
    # Extract
    temp_raw = task_extract_state_temperatures(data_dir)
    noaa_raw = task_extract_noaa_summary(data_dir)
    city_weather = task_fetch_city_weather(api_key)

    # Validate raw
    temp_validated = task_validate_state_temp(temp_raw)
    noaa_validated = task_validate_noaa(noaa_raw)

    # Transform
    temp_transformed = task_transform_state_temperature(temp_validated)
    noaa_transformed = task_transform_noaa_events(noaa_validated)

    # Merge + Validate panel
    panel = task_merge_state_panel(temp_transformed, noaa_transformed)
    validated_panel = task_validate_panel(panel)

    # Save to CSV
    task_save_panel(validated_panel, output_path)
    task_save_city_weather(city_weather)

    # Save to SQLite
    task_save_city_to_sql(city_weather)


if __name__ == "__main__":
    # For local test only
    main_pipeline()

