from typing import Any

from langchain_openai import OpenAIEmbeddings

from app.config import settings


def get_embeddings() -> Any:
    embeddings = OpenAIEmbeddings(
        openai_api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_EMBEDDING_MODEL,
    )
    return embeddings
