from pydantic import BaseModel
from datetime import time


class Posts(BaseModel):
    id: int
    user_id: int
    chat_id: int
    time_type: str
    sent_time: time
