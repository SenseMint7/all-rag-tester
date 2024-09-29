import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import qa
from app.config import settings as application_settings
from app.containers import Container
from app.schemas.base import ResponseBase

logger = logging.getLogger("uvicorn")

container = Container()


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore
    openai_api_key = application_settings.OPENAI_API_KEY
    if not openai_api_key:
        logger.error("OPENAI_API_KEY 환경변수가 존재하지 않습니다.")

    yield


app = FastAPI(
    title=application_settings.PROJECT_NAME,
    version=application_settings.PROJECT_VERSION,
    description=application_settings.PROJECT_DESCRIPTION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.container = container  # type: ignore

app.include_router(qa.router, prefix="/qa", tags=["QA"])


@app.get(
    "/health",
    response_model=ResponseBase,
    description="Health Check API",
)
def health_check() -> ResponseBase:
    return ResponseBase(
        code=200,
        message="Server Alive",
        data={"status": "alive"},
    )
