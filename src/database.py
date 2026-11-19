import os
from pathlib import Path
from storage_local import read_weather_data_local
import psycopg

def insert_into_database(transform_result: dict) -> dict:
    input_path = Path(transform_result["processed_path"])
    data_date = transform_result["fetched_at"]

    rows = read_weather_data_local(input_path)

    rows_loaded_successfully = load_weather_rows_new(rows)

    return {
        "rows_loaded": rows_loaded_successfully,
        "data_date": data_date,
    }

def get_database_connection():
    return psycopg.connect(
        host="postgres",
        port=5432,
        dbname="analytics",
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

def load_weather_rows(rows: list[dict]) -> int:
    insert_sql = """
        INSERT INTO raw_weather_observations (
            observation_time,
            temperature_c,
            precipitation_mm,
            source_name
        )
        VALUES (
            %(observation_time)s,
            %(temperature_c)s,
            %(precipitation_mm)s,
            %(source_name)s
        )
        ON CONFLICT (observation_time)
        DO UPDATE SET
            temperature_c = EXCLUDED.temperature_c,
            precipitation_mm = EXCLUDED.precipitation_mm,
            source_name = EXCLUDED.source_name,
            loaded_at = CURRENT_TIMESTAMP
    """

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.executemany(insert_sql, rows)
            return cursor.rowcount

def load_weather_rows_new(rows: list[dict]) -> int:
    insert_sql = """
        INSERT INTO weather_raw.raw_weather_observations (
            location_id,
            location_name,
            latitude,
            longitude,
            observation_time,
            temperature_c,
            precipitation_mm,
            wind_speed_kph,
            relative_humidity_pct,
            fetched_at
        )
        VALUES (
            %(location_id)s,
            %(location_name)s,
            %(latitude)s,
            %(longitude)s,
            %(observation_time)s,
            %(temperature_c)s,
            %(precipitation_mm)s,
            %(wind_speed_kph)s,
            %(relative_humidity_pct)s,
            %(fetched_at)s
        )
        ON CONFLICT (location_id,observation_time)
        DO UPDATE SET
            temperature_c = EXCLUDED.temperature_c,
            precipitation_mm = EXCLUDED.precipitation_mm,
            wind_speed_kph = EXCLUDED.wind_speed_kph,
            relative_humidity_pct = EXCLUDED.relative_humidity_pct,
            fetched_at = EXCLUDED.fetched_at
    """

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.executemany(insert_sql, rows)
            return cursor.rowcount