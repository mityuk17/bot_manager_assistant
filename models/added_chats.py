from pydantic import BaseModel


class AddedChats(BaseModel):
    chat_id: str
    title: str
