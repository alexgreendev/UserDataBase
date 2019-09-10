import hashlib
import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table

Base = declarative_base()


# noinspection SpellCheckingInspection
class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    access_level = Column(Integer())
    password = Column(String(128))

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.access_level = kwargs['access_level']
        self.password = hashlib.sha256(str(kwargs['password']).encode('utf-8')).hexdigest()

    @staticmethod
    def init_model(metadata):
        Table('users', metadata,
              Column('id', Integer(), primary_key=True),
              Column('name', String(20)),
              Column('access_level', Integer()),
              Column('password', String(128))
              )
