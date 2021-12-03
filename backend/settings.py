from os import environ


class Database:
    service = 'postgresql'
    driver = 'asyncpg'

    name = environ.get("DB_NAME", "postgres")

    user = environ.get("DB_USER", "postgres")
    password = environ.get("DB_PASSWORD", "123456")

    host = environ.get("DB_HOST", "localhost")
    port = environ.get("DB_PORT", "5432")


    @classmethod
    def get_url(cls):
        return f'{cls.service}+{cls.driver}://{cls.user}:{cls.password}@{cls.host}:{cls.port}/{cls.name}'
