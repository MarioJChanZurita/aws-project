from os import environ


DB_URL = "mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
    DB_USER=environ['DB_USER'],
    DB_PASSWORD=environ['DB_PASSWORD'],
    DB_HOST=environ['DB_HOST'],
    DB_PORT=environ['DB_PORT'],
    DB_NAME=environ['DB_NAME']
)