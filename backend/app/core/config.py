from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agentic Customer Support Automation"
    app_env: str = "development"
    debug: bool = True

    # AI
    gemini_api_key: str
    langsmith_api_key: str
    langsmith_tracing: bool = True

    # Database
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()