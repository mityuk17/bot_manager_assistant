from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    chat_id: int
    user_id: int
    full_name: str
    town: str
    time_start: datetime
    time_end: datetime
    week_days: str
    job_title: str
    product: str
    metrics: str
