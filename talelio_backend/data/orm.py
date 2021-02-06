from sqlalchemy.orm import mapper
from sqlalchemy.schema import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import Integer, String

from talelio_backend.app_user.domain.user_model import User

metadata = MetaData()

user_table = Table('user', metadata, Column('id', Integer, primary_key=True, autoincrement=True),
                   Column('name', String))


def start_mappers() -> None:
    mapper(User, user_table)
