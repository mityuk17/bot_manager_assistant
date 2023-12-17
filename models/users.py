from pydantic import BaseModel
from datetime import time


class User(BaseModel):
    user_id: int
    chat_id: int
    full_name: str
    town: str
    time_start: time
    time_end: time
    week_days: str
    job_title: str
    product: str
    metrics: str
