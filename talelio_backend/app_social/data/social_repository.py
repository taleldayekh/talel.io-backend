from talelio_backend.app_social.domain.actor_model import Actor
from talelio_backend.data.repository import BaseRepository


class SocialRepository(BaseRepository):

    def get_actor_for_user(self, user_id: int) -> bool:
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
