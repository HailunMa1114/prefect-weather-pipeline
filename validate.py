import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema, Check


# 1. Schema for raw state-level temperature data
state_temp_schema = DataFrameSchema({
    "STATE": Column(pa.String, nullable=False),
    "DATE": Column(pa.String, checks=Check.str_length(6), nullable=False),
    "TEMPERATURE": Column(pa.Float, checks=Check.in_range(-50, 130), nullable=False),
})


# 2. Schema for NOAA summarized storm events
noaa_schema = DataFrameSchema({
    "YEAR": Column(pa.Int, checks=Check.in_range(2020, 2024)),
    "STATE": Column(pa.String, nullable=False),
    "EVENT_TYPE": Column(pa.String, nullable=False),
    "TOTAL_EVENTS": Column(pa.Int, checks=Check.ge(0), nullable=False),
})


# 3. Schema for merged state-level panel data
state_panel_schema = DataFrameSchema({
    "YEAR": Column(pa.Int, checks=Check.in_range(2020, 2024)),
    "STATE": Column(pa.String, nullable=False),
    "AVG_TEMP": Column(pa.Float, checks=Check.in_range(-50, 130)),
    "EVENT_COUNT": Column(pa.Int, checks=Check.ge(0)),
})


# === Validation functions ===

def validate_state_temp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate state-level temperature data using Pandera schema.
    """
    df["DATE"] = df["DATE"].astype(str) 
    return state_temp_schema.validate(df)


def validate_noaa(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate NOAA summary data using Pandera schema.
    """
    return noaa_schema.validate(df)


def validate_state_panel(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate final merged panel data using Pandera schema.
    """
    return state_panel_schema.validate(df)
