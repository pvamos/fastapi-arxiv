# app/api/models.py

from sqlalchemy import Column, BigInteger, Integer, SmallInteger, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ArxivQuery(Base):
    __tablename__ = 'queries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    query_id = Column(BigInteger)
    timestamp = Column(BigInteger)
    status = Column(SmallInteger)
    num_results = Column(SmallInteger)
    num_entries = Column(SmallInteger)
    query = Column(Text)

class ArxivResult(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    query_id = Column(BigInteger)
    timestamp = Column(BigInteger)
    result_number = Column(SmallInteger)
    author = Column(Text)
    title = Column(Text)
    journal = Column(Text)

