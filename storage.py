from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///ezistore.db', echo=False)


class Setup(Base):
    __tablename__ = 'setup'
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


Session=sessionmaker(bind=engine)
session = Session()
new_key = Setup(keyid = '123', expires = '21/02/00', length='1024', fingerprint='aa:cc', type='RSA', uids='foo')
session.add(new_key)
session.commit()

res = session.query(Setup).all()
print res
for r in res:
    print r.keyid, r.id

#class Storage(object):
#    def __init__(self):
#        Session = sessionmaker(bind=engine)
#        session = Session()
#
#
# 
## Create an artist
#new_artist = Artist("Newsboys")
#new_artist.albums = [Album("Read All About It", 
#                           datetime.date(1988,12,01),
#                           "Refuge", "CD")]
# 
## add more albums
#more_albums = [Album("Hell Is for Wimps",
#                     datetime.date(1990,07,31),
#                     "Star Song", "CD"),
#               Album("Love Liberty Disco", 
#                     datetime.date(1999,11,16),
#                     "Sparrow", "CD"),
#               Album("Thrive",
#                     datetime.date(2002,03,26),
#                     "Sparrow", "CD")]
#new_artist.albums.extend(more_albums)
# 
## Add the record to the session object
#session.add(new_artist)
## commit the record the database
#session.commit()
# 
## Add several artists
#session.add_all([
#    Artist("MXPX"),
#    Artist("Kutless"),
#    Artist("Thousand Foot Krutch")
#    ])
#session.commit()
