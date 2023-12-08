from os import environ

DB_URL = "mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
    DB_USER=environ['DB_USER'],
    DB_PASSWORD=environ['DB_PASSWORD'],
    DB_HOST=environ['DB_HOST'],
    DB_PORT=environ['DB_PORT'],
    DB_NAME=environ['DB_NAME']
)

DYNAMODB_TABLE = environ.get('DYNAMODB_TABLE')
BUCKET_NAME = environ.get('BUCKET_NAME')
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = environ.get('AWS_SESSION_TOKEN')
REGION_NAME = environ.get('REGION_NAME')
SNS_TOPIC_ARN = environ.get('SNS_TOPIC_ARN')