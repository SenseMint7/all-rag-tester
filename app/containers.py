from dependency_injector import containers, providers

from app.config import settings
from app.databases.vectorstore import VectorStore
from app.services.qa_service import QAService
from app.utils.embeddings import get_embeddings
from app.utils.memory import Memory
from app.utils.retriever import Retriever


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.qa",
        ]
    )

    memory = providers.Singleton(Memory, redis_url=settings.REDIS_URL)

    vectorstore = providers.Singleton(
        VectorStore,
        embeddings=get_embeddings,
        persist_directory=settings.VECTOR_STORE_DIR,
    )

    retriever = providers.Singleton(
        Retriever,
        vectorstore=vectorstore,
        local_file_stor_dir=settings.LOCAL_FILE_STORE_DIR,
        upload_file_dir=settings.UPLOAD_FILE_DIR,
    )

    qa_service = providers.Factory(
        QAService,
        retriever=retriever,
        memory=memory,
    )
