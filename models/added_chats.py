from pydantic import BaseModel


class AddedChats(BaseModel):
    chat_id: int
    title: str
