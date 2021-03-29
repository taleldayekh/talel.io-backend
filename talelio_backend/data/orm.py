from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.schema import Column, MetaData, Table
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Integer, String, Text

from talelio_backend.app_account.domain.account_model import Account
from talelio_backend.app_project.domain.project_model import Project
from talelio_backend.app_user.domain.user_model import User

metadata = MetaData()

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

project_table = Table('project', metadata,
                      Column('id', Integer, primary_key=True, autoincrement=True),
                      Column('user_id', Integer, ForeignKey('user.id')),
                      Column('created_at', DateTime, server_default=func.now()),
                      Column('updated_at', DateTime, onupdate=func.now()), Column('title', String),
                      Column('body', Text), Column('html', Text))


def start_mappers() -> None:
    mapper(
        Account,
        account_table,
        properties={'user': relationship(User, backref='account', uselist=False, lazy='joined')})

    mapper(User, user_table, properties={'project': relationship(Project, backref='user')})

    mapper(Project, project_table)
