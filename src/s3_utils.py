import json
import boto3


def get_s3_client(profile_name: str | None = None, region_name: str = "eu-north-1",):
    session = boto3.Session(profile_name=profile_name, region_name = region_name)
    return session.client("s3")


def upload_json_lines(s3_client, bucket_name: str, key: str, data: dict) -> None:

    json_lines = "\n".join(
    		json.dumps(location, ensure_ascii=False)
    		for location in data
    ) + "\n"

    s3_client.put_object(
	Bucket=bucket_name,
	Key=key,
	Body=json_lines.encode("utf-8"),
	ContentType="application/x-ndjson",
    )
