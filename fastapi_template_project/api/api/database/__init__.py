from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import settings


Session = sessionmaker()
engine = create_engine(settings.database_uri)
Session.configure(bind=engine)


Base = declarative_base()
Base.metadata.bind = engine


def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
