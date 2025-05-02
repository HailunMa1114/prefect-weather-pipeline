import os
import pandas as pd
import sqlite3
from load import save_state_panel, save_city_weather_to_sql

def test_save_state_panel(tmp_path):
    # Create sample DataFrame
    df = pd.DataFrame({
        "YEAR": [2020],
        "STATE": ["Texas"],
        "AVG_TEMP": [70.5],
        "EVENT_COUNT": [12]
    })

    # Save to a temporary file
    file_path = tmp_path / "state_panel_test.csv"
    save_state_panel(df, str(file_path))

    # Check if file exists
    assert file_path.exists()

    # Check content
    df_loaded = pd.read_csv(file_path)
    pd.testing.assert_frame_equal(df_loaded, df)

def test_save_city_weather_to_sql(tmp_path):
    # Create sample city weather DataFrame
    df = pd.DataFrame({
        "city": ["New York"],
        "date": ["2025-05-01"],
        "temperature": [20.0],
        "feels_like": [19.5],
        "humidity": [80],
        "wind_speed": [3.2],
        "weather": ["Rain"],
        "source": ["forecast"]
    })

    db_path = tmp_path / "weather_test.db"
    save_city_weather_to_sql(df, str(db_path))

    # Connect to DB and check contents
    conn = sqlite3.connect(str(db_path))
    result_df = pd.read_sql("SELECT * FROM city_weather", conn)
    conn.close()

    # Should match original DataFrame
    pd.testing.assert_frame_equal(result_df, df)
