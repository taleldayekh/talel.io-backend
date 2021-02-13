from sqlalchemy.orm import mapper
from sqlalchemy.schema import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import Integer, String

from talelio_backend.app_account.domain.account_model import Account

metadata = MetaData()

account_table = Table('account', metadata,
                      Column('id', Integer, primary_key=True, autoincrement=True),
                      Column('email', String), Column('password', String))


def start_mappers() -> None:
    mapper(Account, account_table)
