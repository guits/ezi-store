from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import ezi-store

Base = declarative_base()
engine = create_engine('sqlite:///mymusic.db', echo=True)
print config.load(default_config)
exit(1)

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
 
engine = create_engine('sqlite:///sqlalchemy_example.db')
 
Base.metadata.create_all(engine)

exit(1)
