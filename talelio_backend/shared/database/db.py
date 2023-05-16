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
        raise TypeError(f'No {value} env variable available')

connection = psycopg2.connect(f'''
    host={db_connection_values['db_host']}
    port={db_connection_values['db_port']}
    dbname={db_connection_values['db_name']}
    user={db_connection_values['db_user']}
    password={db_connection_values['db_password']}
    ''')

CREATE_ACCOUNT_TABLE = ("""
    CREATE TABLE IF NOT EXISTS account
    (
        id SERIAL,
        created_at TIMESTAMP WITH TIME ZONE,
        updated_at TIMESTAMP WITH TIME ZONE,
        email VARCHAR(255),
        password VARCHAR(255),
        verified BOOLEAN
    );
    """)

# CREATE_USER_TABLE = (
#     """
#     CREATE TABLE IF NOT EXISTS user
#     (
#         id SERIAL,
#         account_id,
#         created_at TIMESTAMP WITH TIME ZONE,
#         updated_at TIMESTAMP WITH TIME ZONE,
#         username VARCHAR(255),
#         location VARCHAR(255),
#         avatar_url VARCHAR(255)
#     );
#     """
# )

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

# CREATE_ARTICLE_TABLE = (
#     """
#     CREATE TABLE IF NOT EXISTS article
#     (
#         id,
#         user_id,
#         created_at,
#         updated_at,
#         title,
#         slug,
#         body,
#         meta_description,
#         html,
#         table_of_contents,
#         featured_image,
#         url
#     );
#     """
# )


def create_tables() -> None:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ACCOUNT_TABLE)
            # cursor.execute(CREATE_USER_TABLE)
            # cursor.execute(CREATE_PROJECT_TABLE)
            # cursor.execute(CREATE_ARTICLE_TABLE)
