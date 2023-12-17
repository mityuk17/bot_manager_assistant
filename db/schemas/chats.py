from db.db import Base
from sqlalchemy import Column, Integer, String, Time


class Chat(Base):
    __tablename__ = 'chats'
    chat_id = Column(Integer, primary_key=True)
    excluded_users = Column(String)



