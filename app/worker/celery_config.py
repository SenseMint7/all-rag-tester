from celery import Celery

from app.config import settings
from app.databases.vectorstore import VectorStore
from app.utils.embeddings import get_embeddings
from app.utils.memory import Memory
from app.utils.retriever import Retriever

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

celery_app = Celery(
    "app",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    include=["app.worker.tasks"],
)

celery_app.conf.broker_connection_retry_on_startup = True

vectorstore = VectorStore(
    embeddings=get_embeddings,
    persist_directory=settings.VECTOR_STORE_DIR,
)

retriever = Retriever(
    vectorstore=vectorstore,
    local_file_stor_dir=settings.LOCAL_FILE_STORE_DIR,
    upload_file_dir=settings.UPLOAD_FILE_DIR,
)

retriever.initialize_retrievers()

memory = Memory(redis_url=settings.REDIS_URL)
