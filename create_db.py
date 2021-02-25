from peers.db import engine, Base, Session
import peers.models
session = Session()
Base.metadata.create_all(engine)
session.commit()

