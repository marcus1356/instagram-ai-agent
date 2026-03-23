from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Instagram AI Agent"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./instagram_agent.db"

    # Claude (Anthropic)
    ANTHROPIC_API_KEY: str

    # OpenAI (DALL-E)
    OPENAI_API_KEY: str

    # Scheduler
    POST_HOUR: int = 9       # hora do post diário (9h)
    POST_MINUTE: int = 0

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
