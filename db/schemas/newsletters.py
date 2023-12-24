from db.db import Base
from sqlalchemy import Column, Integer, String, Time


class Newsletters(Base):
    __tablename__ = 'newsletters'
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer)
    user_id = Column(Integer)
    time = Column(Time)
    week_days = Column(String)
