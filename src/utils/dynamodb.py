from boto3.dynamodb.conditions import Attr
from . import AWS


dynamodb = AWS('dynamodb')


def put_item_to_dynamodb(table_name: str, item: dict) -> None:
    dynamodb = dynamodb.create_resource()
    table = dynamodb.Table(table_name)
    table.put_item(Item=item)


def scan_table(table_name: str, filter_expression: Attr) -> list[dict]:
    dynamodb = dynamodb.create_resource()
    table = dynamodb.Table(table_name)
    response = table.scan(FilterExpression=filter_expression)
    return response['Items']


def update_item_in_dynamodb(table_name: str, key: dict, update_expression: str, expression_attribute_values: dict) -> None:
    dynamodb = dynamodb.create_resource()
    table = dynamodb.Table(table_name)
    table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )