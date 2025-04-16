from datetime import datetime
from typing import List, Literal, TypedDict

from talelio_backend.app_social.domain.actor_model import Actor
from talelio_backend.app_social.domain.post_model import PostModel
from talelio_backend.data.repository import BaseRepository


class MediaRecord(TypedDict):
    url: str
    alt: str
    type: Literal['image', 'video']


class AudienceRecord(TypedDict):
    to: List[str]
    cc: List[str]


class PostRecord(TypedDict):
    id: int
    created_at: datetime
    updated_at: datetime
    content: str
    media: List[MediaRecord]
    audience: AudienceRecord
    platforms: List[str]


class SocialRepository(BaseRepository):

    def create_post(self, post: PostModel, identity_id: int) -> PostRecord:
        post_insert_query = """
            INSERT INTO social.post
            (
                identity_id,
                content
            )
            VALUES (%s, %s)
            RETURNING id;
            """

        post_select_query = """
            SELECT id, created_at, updated_at, content 
            FROM social.post
            WHERE id = %s;
            """

        media_insert_query = """
            INSERT INTO social.media
            (
                post_id,
                url,
                alt,
                type
            )
            VALUES (%s, %s, %s, %s);
            """

        media_select_query = """
            SELECT url, alt, type
            FROM social.media
            WHERE post_id = %s;
            """

        audience_insert_query = """
            INSERT INTO social.audience
            (
                post_id,
                recipient,
                delivery
            )
            VALUES (%s, %s, %s);
            """

        audience_select_query = """
            SELECT recipient, delivery
            FROM social.audience
            WHERE post_id = %s;
            """

        platform_insert_query = """
            INSERT INTO social.platform
            (
                post_id,
                platform
            )
            VALUES (%s, %s);
            """

        platform_select_query = """
            SELECT platform
            FROM social.platform
            WHERE post_id = %s;
            """

        with self.session as session:
            with session.cursor() as cursor:
                # Insert
                cursor.execute(post_insert_query, (identity_id, post.content))

                post_id = cursor.fetchone()[0]

                media_insert_rows = [(post_id, media.url, media.alt, media.type)
                                     for media in post.media]
                cursor.executemany(media_insert_query, media_insert_rows)

                recipient_insert_rows = ([(post_id, recipient, 'to')
                                          for recipient in post.audience.to] +
                                         [(post_id, recipient, 'cc')
                                          for recipient in post.audience.cc])
                cursor.executemany(audience_insert_query, recipient_insert_rows)

                platform_insert_rows = [(post_id, platform) for platform in post.platforms]
                cursor.executemany(platform_insert_query, platform_insert_rows)

                # Select
                cursor.execute(post_select_query, (post_id, ))
                post_select_row = cursor.fetchone()

                record = {
                    'id': post_select_row[0],
                    'created_at': post_select_row[1],
                    'updated_at': post_select_row[2],
                    'content': post_select_row[3],
                    'media': [],
                    'audience': {
                        'to': [],
                        'cc': [],
                    },
                    'platforms': [],
                }

                cursor.execute(media_select_query, (post_id, ))
                media_select_rows = cursor.fetchall()

                record['media'] = [{
                    'url': media_select_row[0],
                    'alt': media_select_row[1],
                    'type': media_select_row[2]
                } for media_select_row in media_select_rows]

                cursor.execute(audience_select_query, (post_id, ))
                audience_select_rows = cursor.fetchall()

                for recipient, delivery in audience_select_rows:
                    record['audience'][delivery].append(recipient)

                cursor.execute(platform_select_query, (post_id, ))
                platform_select_rows = cursor.fetchall()

                record['platforms'] = [
                    platform_select_row[0] for platform_select_row in platform_select_rows
                ]

                return record

    # TODO: Should query social.identity
    # TODO: Return type
    def get_identity_by_user_id(self, user_id: int):
        query = """
            SELECT * FROM 
            activitypub.actor 
            WHERE user_id = %s
            LIMIT 1;
        """

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(query, (user_id, ))

                return cursor.fetchone()

    # TODO: Revise
    def get_actor_by_user_id(self, user_id: int) -> bool:
        query = """
            SELECT EXISTS (
                SELECT 1 FROM activitypub.actor WHERE user_id = %s
            );
            """

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(query, (user_id, ))

                return cursor.fetchone()[0]

    # TODO: Return type
    def get_actor_by_username(self, username: str) -> None:
        query = """
            SELECT * FROM activitypub.actor WHERE username = %s;
            """

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(query, (username, ))

                return cursor.fetchone()

    # TODO: Return type
    def create_actor(self, actor: Actor, user_id: int) -> None:
        insert_query = """
            WITH created_actor AS
            (
                INSERT INTO activitypub.actor
                (
                    user_id,
                    username,
                    type,
                    actor_url,
                    inbox_url,
                    outbox_url,
                    followers_url,
                    following_url,
                    liked_url,
                    public_key,
                    private_key
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *
            )
            SELECT created_actor.id,
                   created_actor.created_at,
                   created_actor.updated_at,
                   created_actor.username,
                   created_actor.type,
                   created_actor.actor_url,
                   created_actor.inbox_url,
                   created_actor.outbox_url,
                   created_actor.followers_url,
                   created_actor.following_url,
                   created_actor.liked_url,
                   created_actor.public_key
            FROM created_actor;
            """

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(insert_query, (
                    user_id,
                    actor.username,
                    actor.type,
                    actor.actor_url,
                    actor.inbox_url,
                    actor.outbox_url,
                    actor.followers_url,
                    actor.following_url,
                    actor.liked_url,
                    actor.public_key,
                    actor.private_key,
                ))

                return cursor.fetchone()
