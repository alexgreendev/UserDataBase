import copy

import sqlalchemy
from sqlalchemy import MetaData


# noinspection PyAttributeOutsideInit
from sqlalchemy.orm import scoped_session, sessionmaker


# noinspection PyAttributeOutsideInit
class DB(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DB, cls).__new__(cls)
            cls.engine = None
            cls.conn = None
            cls.error = False
            cls.metadata = MetaData()
            cls.db_session = None
        return cls.instance

    def connect(self, **kwargs):
        if self.engine is None:
            try:
                connection_path = f"{kwargs['type']}+{kwargs['driver']}://" \
                                  f"{kwargs['user']}:{kwargs['password']}@" \
                                  f"{kwargs['host']}:{kwargs['port']}"
                self.engine = sqlalchemy.create_engine(connection_path, echo=True, connect_args={'connect_timeout': 10})
                self.conn = self.engine.connect()
                self.conn.execute(f"CREATE DATABASE IF NOT EXISTS {kwargs['db_name']}")
                self.engine = sqlalchemy.create_engine(f"{connection_path}/{kwargs['db_name']}", echo=True)
                self.conn = self.engine.connect()
                self.db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=self.engine))
                self.session = self.db_session()
            except Exception as error:
                self.error = error
        return self.error, copy.copy(self.engine)

    def get_connection(self):
        return copy.copy(self.engine)

