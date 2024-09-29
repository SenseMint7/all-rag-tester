import os

from langchain.retrievers import EnsembleRetriever, ParentDocumentRetriever
from langchain.storage import LocalFileStore, create_kv_docstore
from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.databases.vectorstore import VectorStore
from app.utils.file_loader import load_all_pdf


class Retriever:
    def __init__(
        self, vectorstore: VectorStore, local_file_stor_dir: str, upload_file_dir: str
    ) -> None:
        self.init_vectorstore = vectorstore
        self.local_file_stor_dir = local_file_stor_dir
        self.upload_file_dir = upload_file_dir

        self.vectorstore = None
        self.parent_retriever = None
        self.bm25_retriever = None
        self.ensemble_retriever = None

    def initialize_retrievers(self) -> None:
        if os.listdir(self.upload_file_dir):
            self.vectorstore = self.init_vectorstore.load_vectorstore()
            self.parent_retriever = self.get_parent_document_retriever()
            self.bm25_retriever = self.get_bm25_retriever()
            self.ensemble_retriever = self.get_ensemble_retriever()

    def get_bm25_retriever(self) -> BM25Retriever:
        all_docs = load_all_pdf(self.upload_file_dir)
        retriever = BM25Retriever.from_documents(all_docs)
        retriever.k = 1
        return retriever

    def get_parent_document_retriever(self) -> ParentDocumentRetriever:
        fs = LocalFileStore(self.local_file_stor_dir)
        store = create_kv_docstore(fs)
        child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300, chunk_overlap=50
        )
        parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )

        return ParentDocumentRetriever(
            vectorstore=self.vectorstore,
            docstore=store,
            child_splitter=child_splitter,
            parent_splitter=parent_splitter,
        )

    def get_ensemble_retriever(self) -> EnsembleRetriever:
        return EnsembleRetriever(
            retrievers=[self.parent_retriever, self.bm25_retriever], weights=[0.6, 0.4]
        )
