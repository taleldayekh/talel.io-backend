from contextlib import contextmanager
from os import getenv
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URI = getenv('DB_URI')

engine = create_engine(DB_URI)
default_session = sessionmaker(bind=engine)


@contextmanager
def session_manager(session_factory: sessionmaker = default_session) -> Generator:
    session = session_factory()

    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()
