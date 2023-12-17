from pydantic import BaseModel


class Chat(BaseModel):
    chat_id: int
    excluded_users: str
