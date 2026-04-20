from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    stripe_secret_key_sandbox: str
    airalo_api_key: str
    airalo_api_secret: str

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
