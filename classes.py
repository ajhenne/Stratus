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

class Aprimon(Base):
    __tablename__ = 'aprimon_master'
    internalId = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    fast = Column(Boolean)
    lure = Column(Boolean)
    level = Column(Boolean)
    heavy = Column(Boolean)
    love = Column(Boolean)
    moon = Column(Boolean)
    dream = Column(Boolean)
    safari = Column(Boolean)
    beast = Column(Boolean)
    sport = Column(Boolean)