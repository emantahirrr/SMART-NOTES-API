from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    llm_base_url: str
    llm_api_key: str
    llm_model: str

    class Config:
        env_file = ".env"
settings = Settings()