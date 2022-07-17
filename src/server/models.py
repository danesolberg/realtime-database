from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, primary_key=False)

    def __repr__(self):
        return f"<Person(id={self.id}, name='{self.name}', age={self.age})>"

class Query(Base):
    __tablename__ = "queries"
    id = Column(Integer, primary_key=True)
    content = Column(String, primary_key=False)

    def __repr__(self):
        return f"<Query(id={self.id}, content={self.content})>"

Base.TBLNAME_TO_CLASS = {}

for mapper in Base.registry.mappers:
    cls = mapper.class_
    classname = cls.__name__
    if not classname.startswith('_'):
        tblname = cls.__tablename__
        Base.TBLNAME_TO_CLASS[tblname] = cls
