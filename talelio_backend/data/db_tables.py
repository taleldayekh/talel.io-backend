from psycopg2.extensions import connection

from talelio_backend.libs.db_client import DbClient

TIME_ZONE = 'Europe/Berlin'

create_account_table = f"""
    CREATE TABLE IF NOT EXISTS account
    (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE '{TIME_ZONE}'),
        updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE '{TIME_ZONE}'),
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(134) NOT NULL,
        verified BOOLEAN NOT NULL DEFAULT FALSE
    );
    """

create_user_table = f"""
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
    """

create_article_table = f"""
    CREATE TABLE IF NOT EXISTS article
    (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        user_id INTEGER REFERENCES "user" (id) ON DELETE CASCADE,
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE '{TIME_ZONE}'),
        updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE '{TIME_ZONE}'),
        title VARCHAR(255) NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        body TEXT NOT NULL,
        html TEXT NOT NULL,
        meta_description TEXT NOT NULL,
        table_of_contents TEXT NOT NULL,
        featured_image VARCHAR(255) NOT NULL,
        url TEXT NOT NULL
    );
    """

create_paid_article_table = f"""
    CREATE TABLE IF NOT EXISTS paid_article
    (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        user_id INTEGER REFERENCES "user" (id) ON DELETE CASCADE,
        article_id INTEGER REFERENCES article (id) ON DELETE CASCADE,
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE '{TIME_ZONE}'),
        updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE '{TIME_ZONE}'),
        body TEXT NOT NULL,
        html TEXT NOT NULL,
    )
    """


def create_db_tables() -> connection:
    db_client = DbClient()
    conn = db_client.get_connection

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(create_account_table)
            cursor.execute(create_user_table)
            cursor.execute(create_article_table)
            cursor.execute(create_paid_article_table)

    return conn


def drop_db_tables() -> connection:
    db_client = DbClient()
    conn = db_client.get_connection

    with conn:
        with conn.cursor() as cursor:
            query = """
                DROP TABLE account CASCADE;
                DROP TABLE "user" CASCADE;
                DROP TABLE article;
            """

            cursor.execute(query)

    return conn
