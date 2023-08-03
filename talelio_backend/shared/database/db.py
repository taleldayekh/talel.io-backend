from os import getenv

import psycopg2

db_connection_values = {
    'db_host': getenv('DB_HOST'),
    'db_port': getenv('DB_PORT'),
    'db_name': getenv('DB_NAME'),
    'db_user': getenv('DB_USER'),
    'db_password': getenv('DB_PASSWORD')
}

for key, value in db_connection_values.items():
    if not isinstance(value, str):
        raise TypeError(f'No {key} env variable available')

connection = psycopg2.connect(f'''
    host={db_connection_values['db_host']}
    port={db_connection_values['db_port']}
    dbname={db_connection_values['db_name']}
    user={db_connection_values['db_user']}
    password={db_connection_values['db_password']}
    ''')

# CREATE_PROJECT_TABLE = (
#     """
#     CREATE TABLE IF NOT EXISTS project
#     (
#         id,
#         user_id,
#         created_at,
#         updated_at,
#         title,
#         body,
#         html
#     );
#     """
# )


def create_tables() -> None:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ACCOUNT_TABLE)
            cursor.execute(CREATE_USER_TABLE)
            cursor.execute(CREATE_ARTICLE_TABLE)
