import json
from src.s3_utils import get_s3_client, upload_json, download_json, upload_json_lines
from src.weather_api import extract_weather_for_locations, api_call_time
import boto3

BUCKET_NAME = "de-learning-aws-577500259760-eu-north-1-an"
#DESTINATION_KEY = "sandbox/uploaded_by_boto3_v2.json"


def main():

    s3_client = get_s3_client()

    ingestion_date, file_timestamp = api_call_time()
    destination_key = f"prepared/open_meteo/ingestion_date={ingestion_date}/open_meteo_{file_timestamp}"

    weather_json = extract_weather_for_locations()

    upload_json_lines(
        s3_client=s3_client,
        bucket_name=BUCKET_NAME,
        key=destination_key,
        data=weather_json
    )


    #assert downloaded == weather_json

    print(f"Data uploaded in NDJSON format: s3://{BUCKET_NAME}/{destination_key}")


if __name__ == "__main__":
    main()
