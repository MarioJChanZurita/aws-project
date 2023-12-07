import boto3
from os import environ



class AWS():

    def __init__(self, type: str):
        self.type = type

    def create_client(self):
        return boto3.client(
            type,
            aws_access_key_id=environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=environ.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=environ.get("AWS_SESSION_TOKEN"),
            region_name=environ.get("REGION_NAME")
        )
    

    def create_resource(self):
        return boto3.resource(
            type,
            aws_access_key_id=environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=environ.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=environ.get("AWS_SESSION_TOKEN"),
            region_name=environ.get("REGION_NAME")
        )
    