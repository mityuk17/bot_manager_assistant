from db.db import Base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger


class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    chat_id = Column(BigInteger)
    time_type = Column(String)
    sent_time = Column(DateTime)
