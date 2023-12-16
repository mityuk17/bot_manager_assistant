from pydantic import BaseModel


class Chats(BaseModel):
    chat_id: int
    excluded_users: str
