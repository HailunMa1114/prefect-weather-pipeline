import pandas as pd
import os

def extract_noaa_summary(data_dir: str = "data/") -> pd.DataFrame:
    """
    Extract and aggregate NOAA storm event data from yearly CSV files into a summary table.
    
    Returns:
        pd.DataFrame: Aggregated summary with columns [YEAR, STATE, EVENT_TYPE, TOTAL_EVENTS]
    """
    all_years = []

    for year in range(2020, 2025):
        file_path = os.path.join(data_dir, f"{year}.csv")
        try:
            df = pd.read_csv(file_path, usecols=["YEAR", "STATE", "EVENT_TYPE"])
            print(f"Loaded {year}.csv with {len(df)} records.")
            all_years.append(df)
        except FileNotFoundError:
            print(f"File not found: {file_path}. Skipping.")
        except ValueError as e:
            print(f"Error reading {file_path}: {e}")

    if not all_years:
        raise ValueError("No valid NOAA data files found in the given directory.")

    df_all = pd.concat(all_years, ignore_index=True)

    summary = (
        df_all
        .groupby(["YEAR", "STATE", "EVENT_TYPE"])
        .size()
        .reset_index(name="TOTAL_EVENTS")
        .sort_values(by=["YEAR", "STATE", "EVENT_TYPE"])
    )

    return summary
