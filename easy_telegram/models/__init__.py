from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr


class Base:
    @declared_attr
    def __tablename__(cls):  # pylint: disable=E0213
        return f"{cls.__name__.lower()}s"  # pylint: disable=E1101

    id = Column(Integer, primary_key=True)


from sqlalchemy import create_engine  # noqa: E402 # pylint: disable=C0413
from sqlalchemy.ext.declarative import declarative_base  # noqa: E402 # pylint: disable=C0413
from .. import DB_FILE  # noqa: E402 # pylint: disable=C0413

Base = declarative_base(cls=Base)  # type: ignore
engine = create_engine(f'sqlite:///{DB_FILE}')
