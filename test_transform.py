# test_transform.py

import pandas as pd
from transform import (
    transform_state_temperature,
    transform_noaa_events,
    merge_state_panel
)

def test_transform_state_temperature():
    df = pd.DataFrame({
        "STATE": ["Texas", "Texas", "California"],
        "DATE": ["202201", "202202", "202201"],
        "TEMPERATURE": [60.0, 70.0, 55.0]
    })
    result = transform_state_temperature(df)
    assert result.shape[0] == 2
    assert "AVG_TEMP" in result.columns
    assert round(result[result["STATE"] == "TEXAS"]["AVG_TEMP"].values[0], 1) == 65.0

def test_transform_noaa_events():
    df = pd.DataFrame({
        "YEAR": [2022, 2022, 2022],
        "STATE": ["TEXAS", "TEXAS", "CALIFORNIA"],
        "EVENT_TYPE": ["Flood", "Storm", "Fire"],
        "TOTAL_EVENTS": [5, 3, 10]
    })
    result = transform_noaa_events(df)
    assert result.shape[0] == 2
    assert result[result["STATE"] == "TEXAS"]["EVENT_COUNT"].values[0] == 8

def test_merge_state_panel():
    temp_df = pd.DataFrame({
        "YEAR": [2022, 2022],
        "STATE": ["TEXAS", "CALIFORNIA"],
        "AVG_TEMP": [65.0, 55.0]
    })
    event_df = pd.DataFrame({
        "YEAR": [2022],
        "STATE": ["TEXAS"],
        "EVENT_COUNT": [8]
    })
    result = merge_state_panel(temp_df, event_df)
    assert result.shape[0] == 1
    assert result.iloc[0]["STATE"] == "TEXAS"
