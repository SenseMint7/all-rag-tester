from pydantic import BaseModel


class QAQuery(BaseModel):
    question: str
