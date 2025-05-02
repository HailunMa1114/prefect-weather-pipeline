import os
import pandas as pd
import sqlite3
from load import save_state_panel

def test_save_state_panel(tmp_path):
    df = pd.DataFrame({
        "YEAR": [2020],
        "STATE": ["Texas"],
        "AVG_TEMP": [70.5],
        "EVENT_COUNT": [12]
    })
    file_path = tmp_path / "state_panel_test.csv"
    save_state_panel(df, str(file_path))
    assert file_path.exists()
    df_loaded = pd.read_csv(file_path)
    pd.testing.assert_frame_equal(df_loaded, df)
