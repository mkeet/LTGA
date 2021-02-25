from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://peers:putyourpasswordhere@localhost/peers', echo=True)
Base = declarative_base()

Session = sessionmaker()
Session.configure(bind=engine)
