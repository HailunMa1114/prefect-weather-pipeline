import requests
import pandas as pd
import time

def fetch_city_weather(api_key: str, city: str) -> pd.DataFrame:
    """
    Fetch current and 5-day forecast weather for a single city.
    Keep only daily forecast at 12:00 and enrich with current weather.

    Parameters:
        api_key (str): OpenWeatherMap API key
        city (str): City name

    Returns:
        pd.DataFrame: Weather DataFrame with columns like
            ['city', 'date', 'temperature', 'feels_like', 'humidity', 'weather', ...]
    """
    base_params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    # Fetch current weather
    current_url = "https://api.openweathermap.org/data/2.5/weather"
    current = requests.get(current_url, params=base_params).json()

    current_record = {
        "city": city,
        "date": pd.to_datetime("today").normalize(),
        "temperature": current["main"]["temp"],
        "feels_like": current["main"]["feels_like"],
        "humidity": current["main"]["humidity"],
        "wind_speed": current["wind"]["speed"],
        "weather": current["weather"][0]["main"],
        "source": "current"
    }

    # Fetch 5-day forecast
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
    forecast = requests.get(forecast_url, params=base_params).json()

    forecast_records = []
    for entry in forecast.get("list", []):
        ts = pd.to_datetime(entry["dt_txt"])
        if ts.hour == 12:
            record = {
                "city": city,
                "date": ts.normalize(),
                "temperature": entry["main"]["temp"],
                "feels_like": entry["main"]["feels_like"],
                "humidity": entry["main"]["humidity"],
                "wind_speed": entry["wind"]["speed"],
                "weather": entry["weather"][0]["main"],
                "source": "forecast"
            }
            forecast_records.append(record)

    all_records = [current_record] + forecast_records
    df = pd.DataFrame(all_records)

    # Limit to today + 4 days ahead
    today = pd.to_datetime("today").normalize()
    df = df[df["date"] <= today + pd.Timedelta(days=4)]

    return df


def fetch_multiple_cities(api_key: str, cities: list) -> pd.DataFrame:
    """
    Fetch weather data for multiple cities.

    Parameters:
        api_key (str): OpenWeatherMap API key
        cities (list): List of city names

    Returns:
        pd.DataFrame: Combined weather data for all cities
    """
    all_dfs = []

    for city in cities:
        try:
            df = fetch_city_weather(api_key, city)
            all_dfs.append(df)
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching data for {city}: {e}")

    if not all_dfs:
        return pd.DataFrame()

    return pd.concat(all_dfs, ignore_index=True)
