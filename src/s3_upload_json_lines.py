import os
from src.s3_utils import get_s3_client, upload_json_lines
from src.weather_api import extract_weather_for_locations, api_call_time

#BUCKET_NAME = "de-learning-aws-577500259760-eu-north-1-an"
#DESTINATION_KEY = "sandbox/uploaded_by_boto3_v2.json"


def main():
    
    bucket_name = os.environ["S3_BUCKET"]
    s3_client = get_s3_client(profile_name=os.getenv("AWS_PROFILE"))

    ingestion_date, file_timestamp = api_call_time()
    
    destination_key = (
        f"prepared/open_meteo/ingestion_date={ingestion_date}/"
        f"open_meteo_{file_timestamp}.jsonl"
    )

    weather_json = extract_weather_for_locations()

    upload_json_lines(
        s3_client=s3_client,
        bucket_name=bucket_name,
        key=destination_key,
        data=weather_json
    )

    print(
        f"Uploaded {len(weather_results)} location records "
        f"to s3://{bucket_name}/{destination_key}"
    )


if __name__ == "__main__":
    main()
