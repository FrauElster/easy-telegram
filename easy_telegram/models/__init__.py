from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr


class Base:
    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True)


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from .. import _db_file

Base = declarative_base(cls=Base)
engine = create_engine(f'sqlite:///{_db_file}')
