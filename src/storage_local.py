import json
from pathlib import Path 

def store_weather_data_local(payload: dict, data_date: str, output_dir: Path, json_file_name: str) -> Path:
    # output_dir = Path(
    #     f"/opt/airflow/data/raw/weather/extraction_date={data_date}"
    # )
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{json_file_name}.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file)

    return output_path

def read_weather_data_local(input_path_string: str) -> dict:
    input_path = Path(input_path_string)
    with input_path.open(encoding="utf-8") as file:
        return json.load(file)