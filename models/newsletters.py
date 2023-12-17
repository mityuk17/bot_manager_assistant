from pydantic import BaseModel
from datetime import time


class Newsletters(BaseModel):
    id: int
    message_id: int
    user_id: int
    chat_id: int
    time: time
    week_days: str

