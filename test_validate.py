import pandas as pd
import pytest
from validate import (
    validate_state_temp,
    validate_noaa,
    validate_state_panel,
    state_temp_schema,
    noaa_schema,
    state_panel_schema
)
from pandera.errors import SchemaError


# === Test 1: Valid state temperature data ===
def test_validate_state_temp_valid():
    df = pd.DataFrame({
        "STATE": ["Texas"],
        "DATE": ["202201"],
        "TEMPERATURE": [68.0]
    })
    result = validate_state_temp(df)
    assert isinstance(result, pd.DataFrame)


# === Test 2: Invalid type for DATE (int instead of str) ===
def test_validate_state_temp_invalid_type():
    df = pd.DataFrame({
        "STATE": ["Texas"],
        "DATE": [202201],  # int, not str
        "TEMPERATURE": [68.0]
    })
    with pytest.raises(SchemaError):
        state_temp_schema.validate(df)  # Directly test the schema


# === Test 3: Valid NOAA summary data ===
def test_validate_noaa_valid():
    df = pd.DataFrame({
        "YEAR": [2021],
        "STATE": ["California"],
        "EVENT_TYPE": ["Tornado"],
        "TOTAL_EVENTS": [5]
    })
    result = validate_noaa(df)
    assert isinstance(result, pd.DataFrame)


# === Test 4: Invalid NOAA year ===
def test_validate_noaa_invalid_year():
    df = pd.DataFrame({
        "YEAR": [2010],  # Out of valid range
        "STATE": ["California"],
        "EVENT_TYPE": ["Tornado"],
        "TOTAL_EVENTS": [5]
    })
    with pytest.raises(SchemaError):
        noaa_schema.validate(df)


# === Test 5: Valid merged panel data ===
def test_validate_state_panel_valid():
    df = pd.DataFrame({
        "YEAR": [2022],
        "STATE": ["New York"],
        "AVG_TEMP": [52.0],
        "EVENT_COUNT": [10]
    })
    result = validate_state_panel(df)
    assert isinstance(result, pd.DataFrame)


# === Test 6: Invalid merged panel (negative event count) ===
def test_validate_state_panel_invalid_event_count():
    df = pd.DataFrame({
        "YEAR": [2022],
        "STATE": ["New York"],
        "AVG_TEMP": [52.0],
        "EVENT_COUNT": [-5]  # Invalid
    })
    with pytest.raises(SchemaError):
        state_panel_schema.validate(df)
