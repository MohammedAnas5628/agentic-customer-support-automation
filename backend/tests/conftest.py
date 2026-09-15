import os
import pytest

# Ensure environment variables are populated for testing before any application imports
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("GEMINI_API_KEY", "test-gemini-key-1234567890")
os.environ.setdefault("LANGSMITH_API_KEY", "test-langsmith-key-1234567890")
os.environ.setdefault("LANGSMITH_TRACING", "false")
os.environ.setdefault("JWT_SECRET", "test-jwt-secret-minimum-32-characters-required-for-auth")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
os.environ.setdefault("RAG_TOP_K", "5")
os.environ.setdefault("RAG_RELEVANCE_THRESHOLD", "0.55")
