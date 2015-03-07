from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///ezistore.db', echo=False)

# {'dummy': u'', 'keyid': u'904F1ABA14E52AB0', 'expires': u'1457164543', 'subkeys': [], 'length': u'4096', 'ownertrust': u'u', 'algo': u'1', 'fingerprint': u'9126B6976BA0178FEDC909BC904F1ABA14E52AB0', 'date': u'1425628543', 'trust': u'u', 'type': u'pub', 'uids': [u'ezi_store_srv (ezi-store server key) <ezi-store@zigzag.sx>']}

class Setup(Base):
    __tablename__ = 'setup'
    id = Column(Integer, primary_key=True)
    keyid = Column(String(250))
    expires = Column(String(250))
    length = Column(String(250))
    fingerprint = Column(String(250))
    type = Column(String(3))
    uids = Column(String(250))
 
Base.metadata.create_all(engine)


class Storage(object):
    def __init__(self):
        Session = sessionmaker(bind=engine)
        session = Session()


 
# Create an artist
new_artist = Artist("Newsboys")
new_artist.albums = [Album("Read All About It", 
                           datetime.date(1988,12,01),
                           "Refuge", "CD")]
 
# add more albums
more_albums = [Album("Hell Is for Wimps",
                     datetime.date(1990,07,31),
                     "Star Song", "CD"),
               Album("Love Liberty Disco", 
                     datetime.date(1999,11,16),
                     "Sparrow", "CD"),
               Album("Thrive",
                     datetime.date(2002,03,26),
                     "Sparrow", "CD")]
new_artist.albums.extend(more_albums)
 
# Add the record to the session object
session.add(new_artist)
# commit the record the database
session.commit()
 
# Add several artists
session.add_all([
    Artist("MXPX"),
    Artist("Kutless"),
    Artist("Thousand Foot Krutch")
    ])
session.commit()
