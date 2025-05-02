# test_extract.py

import pandas as pd
import pytest
from extract_state_temperatures import extract_state_temperatures
from extract_noaa_summary import extract_noaa_summary
import os

def test_extract_state_temperatures(tmp_path):
    # Create dummy file
    file = tmp_path / "texas.csv"
    file.write_text("Date,Value\n2020-01,10.5\n2020-02,12.1")

    df = extract_state_temperatures(str(tmp_path))
    assert not df.empty
    assert set(df.columns) == {"STATE", "DATE", "TEMPERATURE"}
    assert df.iloc[0]["STATE"] == "texas"

def test_extract_noaa_summary(tmp_path):
    # Create dummy NOAA file
    file = tmp_path / "2020.csv"
    file.write_text("YEAR,STATE,EVENT_TYPE\n2020,TEXAS,Storm\n2020,TEXAS,Flood")

    df = extract_noaa_summary(str(tmp_path))
    assert not df.empty
    assert set(df.columns) == {"YEAR", "STATE", "EVENT_TYPE", "TOTAL_EVENTS"}
    assert df["TOTAL_EVENTS"].sum() == 2
