from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):

    host: str
    port: int
    db: int


class PostgresSettings(BaseSettings):

    password: str
    user: str
    db: str
    host: str
    port: int
    schema: str

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file='../../.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_nested_delimiter='__'
    )

    redis: RedisSettings
    postgres: PostgresSettings
    echo: bool = True
    log_level: str
    twit_numbers: int
    max_twits: int
    feed_partitions: int

settings = Settings()