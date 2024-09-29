import os

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)

from app.config import settings
from app.utils.file_loader import load_yaml


def qa_prompt():
    prompt_data = load_yaml(
        os.path.join(settings.PROMPT_BASE_DIR, "qa_prompt_template.yaml")
    )
    return ChatPromptTemplate.from_messages(
        [
            ("system", prompt_data["system_message"]),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", prompt_data["human_template"]),
        ]
    )


def qa_langsmith_prompt():
    prompt = load_yaml(
        os.path.join(settings.PROMPT_BASE_DIR, "qa_langsmith_prompt_template.yaml")
    )
    return PromptTemplate.from_template(prompt["prompt"])
