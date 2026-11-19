from storage_local import read_weather_data_local, store_weather_data_local
from pathlib import Path 
from datetime import datetime, timezone

def transform_weather_data(extract_result: dict) -> dict:
    input_path = Path(extract_result["raw_path"])
    data_date = extract_result["data_date"]
    
    json_data = read_weather_data_local(input_path)

    hourly = json_data["hourly"]

    rows = [
        {
            "observation_time": timestamp,
            "temperature_c": temperature,
            "precipitation_mm": precipitation,
            "source_name": "open_meteo",
        }
        for timestamp, temperature, precipitation in zip(
            hourly["time"],
            hourly["temperature_2m"],
            hourly["precipitation"],
            strict=True,
        )
    ]

    output_dir = Path(
        f"/opt/airflow/data/processed/weather/extraction_date={data_date}"
    )

    
    local_output = store_weather_data_local(rows, data_date,output_dir,"weather_rows")

    return {
        "processed_path": str(local_output),
        "record_count": len(rows),
        "data_date": data_date,
    }



def transform_weather_data_locations(extract_result: dict) -> dict:
    input_path = Path(extract_result["raw_path"])
    fetched_at = extract_result["fetched_at"]

    raw_payload = read_weather_data_local(input_path)

    locations = raw_payload.get("locations")

    if not isinstance(locations, list) or not locations:
        raise ValueError("Raw weather payload does not contain any locations")

    rows: list[dict] = []

    for location_payload in locations:
        location_id = location_payload.get("location_id")
        location_name = location_payload.get("location_name")

        if not location_id or not location_name:
            raise ValueError("Location payload is missing location_id or location_name")

        hourly = location_payload.get("hourly")

        if not hourly:
            raise ValueError(
                f"Location '{location_id}' response does not contain hourly data"
            )

        times = hourly.get("time")
        temperatures = hourly.get("temperature_2m")
        precipitation = hourly.get("precipitation")
        wind_speeds = hourly.get("wind_speed_10m")
        humidity = hourly.get("relative_humidity_2m")

        required_arrays = {
            "time": times,
            "temperature_2m": temperatures,
            "precipitation": precipitation,
            "wind_speed_10m": wind_speeds,
            "relative_humidity_2m": humidity,
        }

        for name, values in required_arrays.items():
            if values is None:
                raise ValueError(
                    f"Location '{location_id}' response does not contain '{name}' values"
                )

        array_lengths = {
            len(values)
            for values in required_arrays.values()
        }

        if len(array_lengths) != 1:
            raise ValueError(
                f"Location '{location_id}' hourly arrays have different lengths"
            )

        for (
            observation_time,
            temperature,
            precipitation_value,
            wind_speed,
            relative_humidity,
        ) in zip(
            times,
            temperatures,
            precipitation,
            wind_speeds,
            humidity,
            strict=True,
        ):
            rows.append(
                {
                    "location_id": location_id,
                    "location_name": location_name,
                    "latitude": location_payload["latitude"],
                    "longitude": location_payload["longitude"],
                    "observation_time": observation_time,
                    "temperature_c": temperature,
                    "precipitation_mm": precipitation_value,
                    "wind_speed_kph": wind_speed,
                    "relative_humidity_pct": relative_humidity,
                    "source_name": "open_meteo",
                    "fetched_at": fetched_at,
                }
            )

    output_dir = Path(
        f"/opt/airflow/data/processed/weather/fetched_at={fetched_at}"
    )

    local_output = store_weather_data_local(
        payload=rows,
        data_date=fetched_at,
        output_dir=output_dir,
        json_file_name="weather_forecast_rows",
    )

    print(
        f"Transformed {len(rows)} forecast rows for "
        f"{len(locations)} locations at {local_output}"
    )

    return {
        "processed_path": str(local_output),
        "location_count": len(locations),
        "record_count": len(rows),
        "fetched_at": fetched_at,
    }