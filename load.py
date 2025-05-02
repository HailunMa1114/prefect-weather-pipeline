import pandas as pd
import sqlite3

def save_state_panel(panel_df: pd.DataFrame, output_path: str = "extracted_data/state_panel.csv"):
    """
    Save the final merged panel data to CSV.

    Parameters:
        panel_df (pd.DataFrame): DataFrame with columns [YEAR, STATE, AVG_TEMP, EVENT_COUNT]
        output_path (str): Path to save the CSV
    """
    panel_df.to_csv(output_path, index=False)
    print(f"State panel saved to {output_path}")

def save_city_weather_to_sql(df, db_path="extracted_data/weather.db", table_name="city_weather"):
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
