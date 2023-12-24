from pydantic import BaseModel
from datetime import time


class Posts(BaseModel):
    id: int | None
    user_id: int
    chat_id: str
    time_type: str
    sent_time: time
