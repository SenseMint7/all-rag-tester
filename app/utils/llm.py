from langchain_openai.chat_models import ChatOpenAI


def qa_chat_openai() -> ChatOpenAI:
    return ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
