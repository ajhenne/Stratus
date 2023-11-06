from sqlalchemy import create_engine, Table, Column, Integer, Boolean, String, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Pokemon(Base):
    __tablename__ = 'pokemon'
    internalId = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    dexNum = Column(Integer)
    formId = Column(String)
    smogon = Column(String)
    isFemale = Column(Boolean)
    hiddenAbility = Column(Boolean)
    abilities = Column(String)
    sprite = Column(String)