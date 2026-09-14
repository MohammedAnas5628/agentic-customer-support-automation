from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agentic Customer Support Automation"
    app_env: str = "development"
    debug: bool = False

    # AI
    gemini_api_key: SecretStr
    langsmith_api_key: SecretStr
    langsmith_tracing: bool = True
    gemini_chat_model: str = "gemini-3.6-flash"
    rag_top_k: int = 5
    rag_relevance_threshold: float = 0.55
    jwt_secret: SecretStr
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    memory_compaction_message_threshold: int = 24
    memory_recent_message_limit: int = 12
    memory_summary_max_chars: int = 6000

    # Database
    database_url: str

    @field_validator("jwt_secret")
    @classmethod
    def validate_jwt_secret(cls, value: SecretStr) -> SecretStr:
        secret = value.get_secret_value().strip()
        if len(secret) < 32:
            raise ValueError("JWT_SECRET must contain at least 32 characters")
        return SecretStr(secret)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()