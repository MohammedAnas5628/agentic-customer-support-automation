import pytest
from pydantic import SecretStr, ValidationError
from fastapi.testclient import TestClient

from backend.app.core.config import Settings
from backend.app.main import app
from backend.app.schemas.rag import RagQueryRequest
from backend.app.schemas.support import SupportQueryRequest


BASE_SETTINGS = {
    "gemini_api_key": "test-gemini-key",
    "langsmith_api_key": "test-langsmith-key",
    "database_url": "sqlite+aiosqlite:///./test.db",
}


def test_settings_reject_short_jwt_secret():
    with pytest.raises(ValidationError, match="JWT_SECRET"):
        Settings(_env_file=None, jwt_secret="too-short", **BASE_SETTINGS)


def test_settings_accept_valid_jwt_secret_and_mask_secrets():
    settings = Settings(
        _env_file=None,
        jwt_secret="a" * 32,
        **BASE_SETTINGS,
    )

    assert isinstance(settings.jwt_secret, SecretStr)
    assert isinstance(settings.gemini_api_key, SecretStr)
    assert "test-gemini-key" not in repr(settings)


def test_ai_request_boundaries_reject_control_characters_and_oversized_input():
    with pytest.raises(ValidationError):
        RagQueryRequest(query="hello\x00world")
    with pytest.raises(ValidationError):
        SupportQueryRequest(message="x" * 4001)


def test_security_headers_are_added():
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert "frame-ancestors 'none'" in response.headers["Content-Security-Policy"]


def test_rate_limiter_is_registered_on_app():
    assert app.state.limiter is not None
    assert app.state.limiter._default_limits
