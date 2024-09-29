from langchain_chroma import Chroma


class VectorStore:
    def __init__(self, embeddings, persist_directory):
        self.embeddings = embeddings
        self.persist_directory = persist_directory

    def create_vectorstore(self, documents):
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings(),
            persist_directory=self.persist_directory,
        )
        return vectorstore

    def load_vectorstore(self) -> Chroma:
        vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings(),
        )
        return vectorstore
