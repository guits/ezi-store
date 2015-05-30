from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///ezistore.db', echo=False)
EzistoreDB = declarative_base()

class Passwords(EzistoreDB):
    __tablename__ = 'passwords'
    id = Column(Integer, primary_key=True)
    login = Column(String(250))
    password = Column(String(250))
    url = Column(String(250))
    comment = Column(String(250))

    def __init__(self, login, password, url, comment):
        self.login = login
        self.password = password
        self.url = url
        self.comment = comment

EzistoreDB.metadata.create_all(engine)

class Storage(object):
    def __init__(self):
        self._Session = sessionmaker(bind=engine)
        self._session = self._Session()

    def get_all(self):
        return self._session.query(Passwords).all()

    def get(self, search):
        return self._session.query(Passwords).filter(Passwords.comment.like("%s%%" % search)).all()

#TODO: Implement this method
    def delete(self, id):
        pass

    def add(self, login, password, url, comment):
        new = Passwords(login, password, url, comment)
        self._session.add(new)
        self._session.commit()
