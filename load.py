import pandas as pd

def save_state_panel(panel_df: pd.DataFrame, output_path: str = "extracted_data/state_panel.csv"):
    """
    Save the final merged panel data to CSV.

    Parameters:
    - panel_df (pd.DataFrame): DataFrame with columns [YEAR, STATE, AVG_TEMP, EVENT_COUNT]
    - output_path (str): File path to save the CSV
    """
    panel_df.to_csv(output_path, index=False)
    print(f"State panel saved to {output_path}")
