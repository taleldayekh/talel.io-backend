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

TIME_ZONE = 'Europe/Berlin'

CREATE_ACCOUNT_TABLE = (f"""
    CREATE TABLE IF NOT EXISTS account
    (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE '{TIME_ZONE}'),
        updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE '{TIME_ZONE}'),
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(134) NOT NULL,
        verified BOOLEAN NOT NULL DEFAULT TRUE
    );
    """)

CREATE_USER_TABLE = (f"""
    CREATE TABLE IF NOT EXISTS "user"
    (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        account_id INTEGER REFERENCES account (id) ON DELETE CASCADE UNIQUE,
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE '{TIME_ZONE}'),
        updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE '{TIME_ZONE}'),
        username VARCHAR(20) UNIQUE NOT NULL,
        location VARCHAR(50),
        avatar_url VARCHAR(255)
    );
    """)

CREATE_ARTICLE_TABLE = (f"""
    CREATE TABLE IF NOT EXISTS article
    (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        user_id INTEGER REFERENCES "user" (id) ON DELETE CASCADE,
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE '{TIME_ZONE}'),
        updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE '{TIME_ZONE}'),
        title VARCHAR(255) NOT NULL,
        slug TEXT NOT NULL,
        body TEXT NOT NULL,
        html TEXT NOT NULL,
        meta_description TEXT NOT NULL,
        table_of_contents TEXT NOT NULL,
        featured_image VARCHAR(255) NOT NULL,
        url TEXT NOT NULL
    );
    """)

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
