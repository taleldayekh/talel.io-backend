from talelio_backend.data.repository import BaseRepository


class SocialRepository(BaseRepository):

    def create_actor(self) -> None:
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
                VALUES ($s, $s, $s, $s, $s, $s, $s, $s, $s, $s, $s)
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
            """

        # insert_query = """
        #     WITH created_article AS
        #     (
        #         INSERT INTO article
        #         (
        #             user_id,
        #             title,
        #             slug,
        #             body,
        #             html,
        #             meta_description,
        #             table_of_contents,
        #             featured_image,
        #             url
        #         )
        #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        #         RETURNING *
        #     )
        #     SELECT created_article.id,
        #            created_article.created_at,
        #            created_article.updated_at,
        #            created_article.title,
        #            created_article.slug,
        #            created_article.body,
        #            created_article.html,
        #            created_article.meta_description,
        #            created_article.table_of_contents,
        #            created_article.featured_image,
        #            created_article.url,
        #            "user".id,
        #            "user".username,
        #            "user".location,
        #            "user".avatar_url
        #     FROM created_article JOIN "user"
        #     ON created_article.user_id = "user".id;
        #     """
