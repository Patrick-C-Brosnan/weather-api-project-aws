import requests
import json
from pathlib import Path
from datetime import datetime, timezone

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_LOCATIONS = [
    {"location_id": "london", "location_name": "London", "latitude": 51.5072, "longitude": -0.1276},
    {"location_id": "manchester", "location_name": "Manchester", "latitude": 53.4808, "longitude": -2.2426},
    {"location_id": "birmingham", "location_name": "Birmingham", "latitude": 52.4862, "longitude": -1.8904},
    {"location_id": "edinburgh", "location_name": "Edinburgh", "latitude": 55.9533, "longitude": -3.1883},
    {"location_id": "cardiff", "location_name": "Cardiff", "latitude": 51.4816, "longitude": -3.1791},
]

HOURLY_VARIABLES = [
    "temperature_2m",
    "precipitation",
    "wind_speed_10m",
    "relative_humidity_2m",
]

def api_call_time():
    now = datetime.now(timezone.utc)
    ingestion_date = now.strftime("%Y-%m-%d")          # 2026-11-13
    file_timestamp = now.strftime("%Y%m%dT%H%M%S")     # 20261113T115900

    print(ingestion_date, file_timestamp)
    return ingestion_date, file_timestamp

def extract_weather_for_locations() -> dict:
    params = {
        "latitude": ",".join(
            str(location["latitude"]) for location in WEATHER_LOCATIONS
        ),
        "longitude": ",".join(
            str(location["longitude"]) for location in WEATHER_LOCATIONS
        ),
        "hourly": ",".join(HOURLY_VARIABLES),
        "timezone": "Europe/London",
        "past_days": 7,
    }

    response = requests.get(
        OPEN_METEO_URL,
        params=params,
        timeout=30,
    )
    response.raise_for_status()

    payload = response.json()

    if not isinstance(payload, list):
        raise ValueError("Expected a list of location responses from Open-Meteo")

    if len(payload) != len(WEATHER_LOCATIONS):
        raise ValueError(
            f"Expected {len(WEATHER_LOCATIONS)} location responses, got {len(payload)}"
        )

    for location, location_payload in zip(WEATHER_LOCATIONS, payload):
        location_payload["location_id"] = location["location_id"]
        location_payload["location_name"] = location["location_name"]

        validate_weather_payload(location_payload)

    payload_length = len(payload)

    print(f"Payload received with length {payload_length}")

    return payload


def validate_weather_payload(payload: dict) -> None:
    hourly = payload.get("hourly")

    if not hourly:
        raise ValueError("API response does not contain hourly data")

    times = hourly.get("time")
    temperatures = hourly.get("temperature_2m")
    precipitation = hourly.get("precipitation")

    if times is None:
        raise ValueError("API response does not contain hourly time values")

    if temperatures is None:
        raise ValueError("API response does not contain temperature values")

    if precipitation is None:
        raise ValueError("API response does not contain precipitation values")

    if not (
        len(times) == len(temperatures) == len(precipitation)
    ):
        raise ValueError("Weather arrays have different lengths")
