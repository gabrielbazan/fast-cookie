from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from environment import get_database_uri


database_uri = get_database_uri()


Session = sessionmaker()
engine = create_engine(database_uri)
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
