from os import environ


class DatabaseSetting:
    HOST = "DATABASE_HOST"
    DRIVER = "DATABASE_DRIVER"
    PORT = "DATABASE_PORT"
    USER = "DATABASE_USER"
    PASSWORD = "DATABASE_PASSWORD"
    DATABASE_NAME = "DATABASE_NAME"


def get_database_uri():
    host = environ[DatabaseSetting.HOST]
    driver = environ[DatabaseSetting.DRIVER]
    port = environ[DatabaseSetting.PORT]
    user = environ[DatabaseSetting.USER]
    password = environ[DatabaseSetting.PASSWORD]
    database_name = environ[DatabaseSetting.DATABASE_NAME]

    return f"{driver}://{user}:{password}@{host}:{port}/{database_name}"
