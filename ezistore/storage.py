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

    def __init__(self, login=None, password=None, comment=None, url=None):
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

    def delete(self, id):
        result = self._session.query(Passwords).filter(Passwords.id==id).delete()
        print result
        return result

    def add(self, login = None, password = None, url = None, comment = None):
        new = Passwords(login = login, password = password, url = url, comment = comment)
        self._session.add(new)
        self._session.commit()
