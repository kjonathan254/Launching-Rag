from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str

    # OpenAI Configuration
    OPENAI_API_KEY: str
    OPENAI_EMBED_MODEL: str = "text-embedding-3-large"
    OPENAI_CHAT_MODEL: str = "gpt-4o"

    # AI Provider (openai or anthropic)
    AI_PROVIDER: str = "openai"

    # Anthropic Configuration (optional)
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_CHAT_MODEL: str = "claude-3-5-sonnet-20241022"

    # RAG Parameters
    chunk_size: int = 400
    chunk_overlap: int = 60
    default_top_k: int = 6
    temperature: float = 0.1

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
