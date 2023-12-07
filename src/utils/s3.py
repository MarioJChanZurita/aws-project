import boto3
from os import environ


def create_client(type: str):
    return boto3.client(type,
            aws_access_key_id=environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=environ.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=environ.get("AWS_SESSION_TOKEN"),
            region_name=environ.get("REGION_NAME")
        )


def create_resource(type: str):
    return boto3.resource(type,
            aws_access_key_id=environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=environ.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=environ.get("AWS_SESSION_TOKEN"),
            region_name=environ.get("REGION_NAME")
        )
    
    
def upload_file_to_s3(file, filename) -> None:
    s3 = create_client('s3')
    s3.upload_file(
        file,
        environ.get('BUCKET_NAME'),
        filename,
        ExtraArgs={
            "ACL": "public-read",
            "ContentType": 'multipart/form-data'
        }
    )