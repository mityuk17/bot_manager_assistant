from db.db import Base
from sqlalchemy import Column, Integer, String, Time


class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    chat_id = Column(Integer)
    time_type = Column(String)
    sent_time = Column(Time)