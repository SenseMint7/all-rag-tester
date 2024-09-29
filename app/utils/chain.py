from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def create_qa_chain(retriever, prompt, llm):
    chain = (
        {
            "context": lambda x: retriever.get_relevant_documents(x["question"]),
            "chat_history": lambda x: x["chat_history"],
            "question": lambda x: x["question"],
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def create_langsmith_qa_chain(retriever, prompt, llm):
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
