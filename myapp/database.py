from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging

logging.basicConfig()

engine = create_engine('mysql://root:123456Vv@localhost/test', pool_size=5, max_overflow=0, pool_timeout=3)
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():    
    import myapp.models
    Base.metadata.create_all(bind=engine)