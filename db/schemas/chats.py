from db.db import Base
from sqlalchemy import Column, Integer, String, Time, BigInteger


class Chat(Base):
    __tablename__ = 'chats'
    chat_id = Column(BigInteger, primary_key=True)
    title = Column(String)



