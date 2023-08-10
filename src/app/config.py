from pydantic import BaseSettings


class Settings(BaseSettings):
    db_uri: str
    server_env: str = "not set"
    development: bool = True
    log_level: str = "DEBUG"
    log_location: str = "local"
    log_config: str = "logging/config.json"
    app_title: str = "code-challenge".replace("-", " ").title()


settings = Settings()
