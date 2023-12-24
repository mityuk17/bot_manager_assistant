from db.db import Base
from sqlalchemy import Column, Integer, String, Time


class AddedChats(Base):
    __tablename__ = 'added_chats'
    chat_id = Column(String, primary_key=True)
    title = Column(String)
