from pydantic import BaseModel
from datetime import time


class Newsletters(BaseModel):
    id: int | None
    message_id: int
    user_id: int
    time: time
    week_days: str

