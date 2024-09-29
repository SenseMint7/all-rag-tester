import os
from typing import Any, List

from fastapi import HTTPException
from langchain_core.runnables import RunnableSerializable

from app.utils.chain import create_qa_chain
from app.utils.file_loader import load_pdf
from app.utils.llm import qa_chat_openai
from app.utils.memory import Memory
from app.utils.prompt import qa_prompt
from app.utils.retriever import Retriever


class QAService:
    def __init__(
        self,
        retriever: Retriever,
        memory: Memory,
    ):
        self.retriever = retriever
        self.memory = memory

    @staticmethod
    def exist_file(file_path: str):
        if not os.listdir(file_path):
            raise HTTPException(
                status_code=400, detail="파일을 업로드 후 질문해 주시길 바랍니다."
            )

    @staticmethod
    def check_file(filename: str, file_path: str):
        if not filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="PDF 파일만 업로드 가능합니다.")
        if os.path.exists(file_path):
            raise HTTPException(
                status_code=400, detail="해당이름의 파일이 이미 존재합니다."
            )

    @staticmethod
    async def save_file(file, file_path):
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

    def pdf_to_vectorstore(self, file_path: str):
        documents = load_pdf(file_path)
        self.retriever.vectorstore = self.retriever.init_vectorstore.load_vectorstore()
        parent_retriever = self.retriever.get_parent_document_retriever()
        parent_retriever.add_documents(documents)

    def get_qa_chain(self) -> RunnableSerializable[Any, str]:
        ensemble_retriever = self.retriever.ensemble_retriever
        prompt = qa_prompt()
        llm = qa_chat_openai()

        chain = create_qa_chain(ensemble_retriever, prompt, llm)

        return chain

    def get_chat_history(self, user_id: str) -> List[dict]:
        history = self.memory.get_redis_history(user_id)
        return self.memory.get_chat_history(history)
