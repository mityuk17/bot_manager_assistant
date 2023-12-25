from db.db import Base
from sqlalchemy import Column, Integer, String, Time, BigInteger


class Newsletters(Base):
    __tablename__ = 'newsletters'
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(BigInteger)
    user_id = Column(BigInteger)
    time = Column(Time)
    week_days = Column(String)
