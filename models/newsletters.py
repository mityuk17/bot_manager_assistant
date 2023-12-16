from pydantic import BaseModel
from datetime import datetime


class Newsletters(BaseModel):
    id: int
    message_id: int
    user_id: int
    chat_id: int
    time: datetime
    week_days: str

