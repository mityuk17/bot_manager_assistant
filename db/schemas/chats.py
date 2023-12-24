from db.db import Base
from sqlalchemy import Column, Integer, String, Time


class Chat(Base):
    __tablename__ = 'chats'
    chat_id = Column(String, primary_key=True)
    title = Column(String)



