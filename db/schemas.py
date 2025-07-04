from sqlalchemy import Column, Integer, BigInteger, Boolean
from db.db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    peer_id = Column(BigInteger)
    ref_status = Column(Boolean)