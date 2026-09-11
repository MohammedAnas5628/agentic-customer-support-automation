from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agentic Customer Support Automation"
    app_env: str = "development"
    debug: bool = True

    # AI
    gemini_api_key: str
    langsmith_api_key: str
    langsmith_tracing: bool = True
    gemini_chat_model: str = "gemini-2.0-flash"
    rag_top_k: int = 5
    rag_relevance_threshold: float = 0.55
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Database
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()