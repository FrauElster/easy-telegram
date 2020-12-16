from sqlalchemy import ForeignKey, Column, Table, Integer
from . import Base

event_permissions = Table('event_permissions', Base.metadata,
                          Column('event_id', Integer, ForeignKey('events.id')),
                          Column('permission_id', Integer, ForeignKey('permissions.id')))
