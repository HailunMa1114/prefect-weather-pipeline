import pandas as pd
import os
from typing import List

def extract_state_temperatures(data_dir: str = "data/") -> pd.DataFrame:
    """
    Load and combine monthly average temperature data for all US states from individual CSV files.

    Parameters:
        data_dir (str): Path to the directory containing state temperature CSVs 

    Returns:
        pd.DataFrame: Combined table with columns ['STATE', 'DATE', 'TEMPERATURE']
    """
    all_states = []
    
    for filename in os.listdir(data_dir):
        if filename.endswith(".csv") and filename not in ["us_tem.csv"] and filename[0].isalpha():
            state = filename.replace(".csv", "").lower()
            file_path = os.path.join(data_dir, filename)
            try:
                df = pd.read_csv(file_path, usecols=["Date", "Value"])
                df["STATE"] = state
                df.rename(columns={"Date": "DATE", "Value": "TEMPERATURE"}, inplace=True)
                all_states.append(df)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    if not all_states:
        raise ValueError("No valid state temperature files found.")

    result = pd.concat(all_states, ignore_index=True)
    return result[["STATE", "DATE", "TEMPERATURE"]]
