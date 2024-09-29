from app.utils.chain import create_qa_chain
from app.utils.llm import qa_chat_openai
from app.utils.prompt import qa_prompt
from app.worker.celery_config import celery_app, memory, retriever


@celery_app.task
def generate_chat_task(question: str, user_id: str = "user"):
    ensemble_retriever = retriever.ensemble_retriever
    if ensemble_retriever is None:
        retriever.initialize_retrievers()
        ensemble_retriever = retriever.ensemble_retriever

    prompt = qa_prompt()
    llm = qa_chat_openai()

    qa_chain = create_qa_chain(ensemble_retriever, prompt, llm)
    chain_with_history = memory.create_chain_with_history(
        qa_chain,
        memory.get_redis_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )

    result = chain_with_history.invoke(
        {"question": question},
        config={"configurable": {"session_id": user_id}},
    )

    # Langsmith Evaluation
    # langsmith_prompt = qa_langsmith_prompt()
    # qa_langsmith_chain = create_langsmith_qa_chain(ensemble_retriever, langsmith_prompt, llm)
    # evaluation_runnable = RunnableParallel(
    #     {
    #         "context": ensemble_retriever,
    #         "answer": qa_langsmith_chain,
    #         "question": RunnablePassthrough(),
    #     }
    # )
    # _ = evaluation_runnable.invoke(question)

    return result


@celery_app.task
def update_retrievers_task():
    retriever.initialize_retrievers()
