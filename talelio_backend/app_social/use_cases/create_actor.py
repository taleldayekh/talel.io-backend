from os import getenv

from talelio_backend.app_social.domain.actor_model import Actor
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.shared.exceptions import UserError


# TODO: Return type
def create_actor(uow: UnitOfWork, user_id: int, username: str) -> None:
    FEDERATION_ROOT_URL = getenv('SOCIALS_FEDERATION_ROOT_URL')
    ENCRYPTION_KEY = getenv('SOCIALS_ENCRYPTION_KEY')

    if not FEDERATION_ROOT_URL or not ENCRYPTION_KEY:
        raise ValueError(
            'Missing "SOCIALS_FEDERATION_ROOT_URL" or "SOCIALS_ENCRYPTION_KEY" environment variables'
        )

    with uow:
        actor_exists = uow.social.get_actor_by_user_id(user_id)

        if actor_exists:
            raise UserError(f"Actor for user with id '{user_id}' already exists")

        actor = Actor(username, FEDERATION_ROOT_URL)
        actor.generate_key_pair(ENCRYPTION_KEY)

        actor_record = uow.social.create_actor(actor, user_id)

        # TODO: Include liked?
        # TODO: Return directly
        actor_object = {
            '@context': 'https://www.w3.org/ns/activitystreams',
            'id': actor_record[5],
            'type': actor_record[4],
            'preferredUsername': actor_record[3],
            'inbox': actor_record[6],
            'outbox': actor_record[7],
            'followers': actor_record[8],
            'following': actor_record[9],
            'publicKey': {
                'id': actor_record[5] + '#main-key',
                'owner': actor_record[5],
                'publicKeyPem': actor_record[11],
            }
        }

        print(actor_object)
