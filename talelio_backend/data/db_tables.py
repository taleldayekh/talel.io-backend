from psycopg2.extensions import connection

from talelio_backend.libs.db_client import DbClient

TIME_ZONE = 'Europe/Berlin'

# Schemas
CREATE_ACTIVITYPUB_SCHEMA = "CREATE SCHEMA IF NOT EXISTS activitypub;"

# Tables
CREATE_ACCOUNT_TABLE = f"""
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

CREATE_USER_TABLE = f"""
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

CREATE_ARTICLE_TABLE = f"""
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

CREATE_ACTOR_TABLE = f"""
    CREATE TABLE IF NOT EXISTS activitypub.actor 
    (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        user_id INTEGER UNIQUE REFERENCES "user" (id),
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE '{TIME_ZONE}'),
        updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE '{TIME_ZONE}'),
        username VARCHAR(20) UNIQUE NOT NULL,
        type VARCHAR(50) NOT NULL DEFAULT 'Person',
        actor_url TEXT UNIQUE NOT NULL,
        inbox_url TEXT UNIQUE NOT NULL,
        outbox_url TEXT UNIQUE NOT NULL,
        followers_url TEXT UNIQUE NOT NULL,
        following_url TEXT UNIQUE NOT NULL,
        liked_url TEXT UNIQUE NOT NULL,
        public_key TEXT NOT NULL,
        private_key TEXT NOT NULL
    );
    """


def create_db_tables() -> connection:
    db_client = DbClient()
    conn = db_client.get_connection

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_ACTIVITYPUB_SCHEMA)
            cursor.execute(CREATE_ACCOUNT_TABLE)
            cursor.execute(CREATE_USER_TABLE)
            cursor.execute(CREATE_ARTICLE_TABLE)
            cursor.execute(CREATE_ACTOR_TABLE)

    return conn


def drop_db_tables() -> connection:
    db_client = DbClient()
    conn = db_client.get_connection

    with conn:
        with conn.cursor() as cursor:
            query = """
                DROP TABLE IF EXISTS article CASCADE;
                DROP TABLE IF EXISTS "user" CASCADE;
                DROP TABLE IF EXISTS account CASCADE;
                DROP SCHEMA IF EXISTS activitypub CASCADE;
            """

            cursor.execute(query)

    return conn
