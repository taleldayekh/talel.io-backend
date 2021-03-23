from sqlalchemy import ForeignKey
from sqlalchemy.orm import registry, relationship  # type: ignore
from sqlalchemy.schema import Column, MetaData, Table
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Integer, String

from talelio_backend.app_account.domain.account_model import Account
from talelio_backend.app_user.domain.user_model import User

metadata = MetaData()
mapper_registry = registry()

account_table = Table('account', metadata,
                      Column('id', Integer, primary_key=True, autoincrement=True),
                      Column('created_at', DateTime, server_default=func.now()),
                      Column('updated_at', DateTime, onupdate=func.now()), Column('email', String),
                      Column('password', String), Column('verified', Boolean))

user_table = Table('user', metadata, Column('id', Integer, primary_key=True, autoincrement=True),
                   Column('account_id', Integer, ForeignKey('account.id')),
                   Column('created_at', DateTime, server_default=func.now()),
                   Column('updated_at', DateTime, onupdate=func.now()), Column('username', String),
                   Column('avatar_url', String), Column('location', String))


def start_mappers() -> None:
    mapper_registry.map_imperatively(
        Account,
        account_table,
        properties={'user': relationship(User, backref='account', uselist=False, lazy='joined')})
    mapper_registry.map_imperatively(User, user_table)
