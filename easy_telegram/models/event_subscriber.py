from sqlalchemy import Table, Column, Integer, ForeignKey
from . import Base

event_subscriber = Table('event_subscriber', Base.metadata,
                         Column('event_id', Integer, ForeignKey('events.id')),
                         Column('user_id', Integer, ForeignKey('users.id')))
