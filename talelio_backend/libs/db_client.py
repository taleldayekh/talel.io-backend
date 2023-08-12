from os import getenv
from typing import Dict, Optional, Union

from psycopg2 import OperationalError, connect
from psycopg2.extensions import connection

from talelio_backend.shared.exceptions import DatabaseError


class DbClient:

    def __init__(self, db_connection_values: Optional[Dict[str, Union[str, None]]] = None) -> None:
        if db_connection_values is None:
            self.db_connection_values = {
                'dbname': getenv('DB_NAME'),
                'user': getenv('DB_USER'),
                'password': getenv('DB_PASSWORD'),
                'host': getenv('DB_HOST'),
                'port': getenv('DB_PORT'),
            }
        else:
            self.db_connection_values = db_connection_values

        for key, value in self.db_connection_values.items():
            if not isinstance(value, str):
                connection_value_error = f'No {key} available'
                raise TypeError(connection_value_error)

    @property
    def get_connection(self) -> connection:
        try:
            conn = connect(f"""
                dbname={self.db_connection_values['dbname']}
                user={self.db_connection_values['user']}
                password={self.db_connection_values['password']}
                host={self.db_connection_values['host']}
                port={self.db_connection_values['port']}
            """)

            return conn
        except OperationalError as error:
            raise DatabaseError('Failed to connect to database') from error
