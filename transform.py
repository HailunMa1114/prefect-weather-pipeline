import pandas as pd

def transform_state_temperature(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate monthly temperatures into annual average per state.

    Parameters:
        df (pd.DataFrame): Input with columns [STATE, DATE, TEMPERATURE]

    Returns:
        pd.DataFrame: Output with [YEAR, STATE, AVG_TEMP]
    """
    df["YEAR"] = df["DATE"].astype(str).str[:4].astype(int)
    df["STATE"] = df["STATE"].str.upper().str.strip()  
    result = (
        df.groupby(["YEAR", "STATE"], as_index=False)
          .agg(AVG_TEMP=("TEMPERATURE", "mean"))
    )
    return result


def transform_noaa_events(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate total storm events per state per year.

    Parameters:
        df (pd.DataFrame): Input with columns [YEAR, STATE, EVENT_TYPE, TOTAL_EVENTS]

    Returns:
        pd.DataFrame: Output with [YEAR, STATE, EVENT_COUNT]
    """
    df["STATE"] = df["STATE"].str.upper().str.strip() 
    result = (
        df.groupby(["YEAR", "STATE"], as_index=False)
          .agg(EVENT_COUNT=("TOTAL_EVENTS", "sum"))
    )
    return result


def merge_state_panel(temp_df: pd.DataFrame, event_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge annual temperature and event count per state.

    Parameters:
        temp_df (pd.DataFrame): Output from transform_state_temperature
        event_df (pd.DataFrame): Output from transform_noaa_events

    Returns:
        pd.DataFrame: Merged panel with [YEAR, STATE, AVG_TEMP, EVENT_COUNT]
    """
    return pd.merge(temp_df, event_df, on=["YEAR", "STATE"], how="inner")
