from sqlalchemy import ForeignKey, Column, Table, Integer
from . import Base

user_permissions = Table('user_permissions', Base.metadata,  # type: ignore
                         Column('user_id', Integer, ForeignKey('users.id')),
                         Column('permission_id', Integer, ForeignKey('permissions.id')))
