import boto3
from enum import Enum
from src.utils import const
from boto3.dynamodb.conditions import Attr

class DynamoDB():

    def __init__(self, service):
        self.service = service

    def agregar(self, table_name: str, item: dict):
        table = self.service.Table(table_name)
        table.put_item(
            Item=item
        )

    def escanear_tabla(self, table_name: str, filter_expression: Attr) -> list[dict]:
        table = self.service.Table(table_name)
        response = table.scan(
            FilterExpression=filter_expression
        )
        return response['Items']

    def actualizar(self, table_name: str, key: dict, update_expression: str, expression_attribute_values: dict):
        table = self.service.Table(table_name)
        table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )

class SNS():

    def __init__(self, service):
        self.service = service

    def publicar_msg(self, message: str, topic_arn: str):
        self.service.publish(
            TopicArn=topic_arn,
            Message=message
        )

class S3():

    def __init__(self, service):
        self.service = service

    def subir(self, file, filename):
        self.service.upload_file(
            file,
            BUCKET_NAME,
            filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": 'multipart/form-data'
            }
        )

class AWSServices(Enum):
    dynamodb = DynamoDB
    s3 = S3
    sns = SNS

class AWS():

    def __init__(self, service: AWSServices):
        match(service):
            case service.DynamoDB:
                return DynamoDB(self.crear_recurso('dynamodb'))
            case service.S3:
                return S3(self.crear_cliente('s3'))
            case service.SNS:
                return SNS(self.crear_cliente('sns'))

    def crear_cliente(self):
        return boto3.client(
            self.type,
            aws_access_key_id=const.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=const.AWS_SECRET_ACCESS_KEY,
            aws_session_token=const.AWS_SESSION_TOKEN,
            region_name=const.REGION_NAME
        )
    
    def crear_recurso(self):
        return boto3.resource(
            self.type,
            aws_access_key_id=const.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=const.AWS_SECRET_ACCESS_KEY,
            aws_session_token=const.AWS_SESSION_TOKEN,
            region_name=const.REGION_NAME
        )