from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URI = getenv('DB_URI')

if not isinstance(DB_URI, str):
    raise TypeError('No database URI provided')

engine = create_engine(DB_URI)
default_session = sessionmaker(bind=engine)
