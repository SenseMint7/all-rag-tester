import os
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

if os.getenv("APP_ENV") == "test":
    env_location: str = f"{os.getcwd()}/.env.test"
else:
    env_location = f"{os.getcwd()}/.env"

load_dotenv(env_location, override=True)


class ApplicationSettings(BaseSettings):
    PROJECT_NAME: str = "All RAG Tester"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "test the methodology of all RAG"
    PROJECT_ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")

    EXCEPT_PATH_LIST: list[str] = ["/health", "/openapi.json"]
    EXCEPT_PATH_REGEX: str = "^(/docs|/redoc)"

    # Data Path
    UPLOAD_FILE_DIR: str = os.getenv("UPLOAD_FILE_DIR", "./data/file")
    LOCAL_FILE_STORE_DIR: str = os.getenv(
        "LOCAL_FILE_STORE_DIR", "./data/local_file_store"
    )
    VECTOR_STORE_DIR: str = os.getenv("VECTOR_STORE_DIR", "./data/vectorstore")
    PROMPT_BASE_DIR: str = os.getenv("PROMPT_BASE_DIR", "./data/prompt")

    # OpenAI
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_EMBEDDING_MODEL: str = os.getenv(
        "your-openai-embedding-model", "text-embedding-3-large"
    )

    # Lang Smith
    # LANGCHAIN_TRACING_V2: str = os.getenv("LANGCHAIN_TRACING_V2", "true")
    # LANGCHAIN_ENDPOINT: str = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    # LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY")
    # LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT", "rag-test")

    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: str = os.getenv("REDIS_PORT", "6379")
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"


settings = ApplicationSettings()
