from pydantic import BaseModel
from datetime import time, datetime


class Posts(BaseModel):
    id: int | None
    user_id: int
    chat_id: int
    time_type: str
    sent_time: datetime
