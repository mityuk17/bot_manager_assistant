from db.db import Base
from sqlalchemy import Column, Integer, String, Time


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, primary_key=True)
    full_name = Column(String)
    town = Column(String)
    time_start = Column(Time)
    time_end = Column(Time)
    week_days = Column(String)
    job_title = Column(String)
    product = Column(String)
    metrics = Column(String)
