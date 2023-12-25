from db.db import Base
from sqlalchemy import Column, Integer, String, Time, BigInteger


class AddedChats(Base):
    __tablename__ = 'added_chats'
    chat_id = Column(BigInteger, primary_key=True)
    title = Column(String)
