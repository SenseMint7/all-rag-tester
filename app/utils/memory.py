from typing import List

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_redis import RedisChatMessageHistory


class Memory:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url

    def get_redis_history(self, session_id: str) -> BaseChatMessageHistory:
        return RedisChatMessageHistory(session_id, redis_url=self.redis_url)

    @staticmethod
    def create_chain_with_history(
        chain,
        history,
        input_messages_key="question",
        history_messages_key="chat_history",
    ):
        return RunnableWithMessageHistory(
            chain,
            history,
            input_messages_key=input_messages_key,
            history_messages_key=history_messages_key,
        )

    @staticmethod
    def get_chat_history(history: BaseChatMessageHistory) -> List[dict]:
        return [
            {
                "role": "human" if isinstance(message, HumanMessage) else "ai",
                "content": message.content,
            }
            for message in history.messages
        ]

    @staticmethod
    def add_message_to_history(
        history: BaseChatMessageHistory, user_message, ai_message
    ) -> None:
        history.add_user_message(user_message)
        history.add_ai_message(ai_message)
