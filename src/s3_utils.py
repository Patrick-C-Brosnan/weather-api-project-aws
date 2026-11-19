import json

import boto3


def get_s3_client(profile_name: str = "de-learning"):
    session = boto3.Session(profile_name=profile_name)
    return session.client("s3")


def download_json(s3_client, bucket_name: str, key: str) -> dict:
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    return json.loads(response["Body"].read())


def upload_json(s3_client, bucket_name: str, key: str, data: dict) -> None:

    body = json.dumps(data).encode("utf-8")

    s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=body,
        ContentType="application/json",
    )

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
