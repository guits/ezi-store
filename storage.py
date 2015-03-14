from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///ezistore.db', echo=False)


class Server_gpg(Base):
    __tablename__ = 'srv_gpg'
    id = Column(Integer, primary_key=True)
    keyid = Column(String(250))
    expires = Column(String(250))
    length = Column(String(250))
    fingerprint = Column(String(250))
    type = Column(String(3))
    uids = Column(String(250))

    def __init__(self, keyid, expires, length, fingerprint, type, uids):
        self.keyid = keyid
        self.expires = expires
        self.length = length
        self.fingerprint = fingerprint
        self.type = type
        self.uids = uids

class Client_gpg(Base):
    __tablename__ = 'client_gpg'
    id = Column(Integer, primary_key=True)
    keyid = Column(String(250))
    expires = Column(String(250))
    length = Column(String(250))
    fingerprint = Column(String(250))
    type = Column(String(3))
    uids = Column(String(250))

    def __init__(self, keyid, expires, length, fingerprint, type, uids):
        self.keyid = keyid
        self.expires = expires
        self.length = length
        self.fingerprint = fingerprint
        self.type = type
        self.uids = uids

Base.metadata.create_all(engine)


class Storage(object):
    def __init__(self):
        self._Session = sessionmaker(bind=engine)
        self._session = self._Session()

    def get_keys(self):
        return self._session.query(Setup).all()

    def set_key(self, keyid, expires, length, fingerprint, type, uids):
        new_key = Setup(keyid = '123', expires = '21/02/00', length='1024', fingerprint='aa:cc', type='pub', uids='foo')
        self._session.add(new_key)
        self._session.commit()
