# test_city_api.py

import pytest
import pandas as pd
from city_api import fetch_city_weather

def test_fetch_city_weather_mock(monkeypatch):
    def mock_get(url, params):
        class MockResponse:
            def json(self):
                if "forecast" in url:
                    return {"list": []}
                else:
                    return {
                        "main": {"temp": 20, "feels_like": 18, "humidity": 50},
                        "wind": {"speed": 3},
                        "weather": [{"main": "Clear"}]
                    }
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    df = fetch_city_weather("fake-key", "TestCity")
    assert not df.empty
    assert "temperature" in df.columns
    assert df.iloc[0]["city"] == "TestCity"
