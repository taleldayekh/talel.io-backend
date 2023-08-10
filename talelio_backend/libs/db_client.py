from os import getenv
from typing import Dict, Union

from psycopg2 import OperationalError, connect, connection

from talelio_backend.shared.exceptions import DatabaseError

connection_values = {
    'dbname': getenv('DB_NAME'),
    'user': getenv('DB_USER'),
    'password': getenv('DB_PASSWORD'),
    'host': getenv('DB_HOST'),
    'port': getenv('DB_PORT'),
}


class DbClient:

    def __init__(self,
                 db_connection_values: Dict[str, Union[str, None]] = connection_values) -> None:
        for key, value in db_connection_values.items():
            if not isinstance(value, str):
                connection_value_error = f'No {key} env variable available'
                raise TypeError(connection_value_error)

        self.db_connection_values = connection_values

    @property
    def get_connection(self) -> connection:
        try:
            conn = connect(**self.db_connection_values)
            return conn
        except OperationalError as error:
            raise DatabaseError('Failed to connect to database') from error
