from os import getenv

from talelio_backend.app_social.domain.actor_model import Actor
from talelio_backend.data.uow import UnitOfWork


# TODO: Return type
def create_actor(uow: UnitOfWork, user_id: int, username: str) -> None:
    FEDERATION_ROOT_URL = getenv('SOCIALS_FEDERATION_ROOT_URL')
    ENCRYPTION_KEY = getenv('SOCIALS_ENCRYPTION_KEY')

    if not FEDERATION_ROOT_URL or not ENCRYPTION_KEY:
        # TODO: Raise error
        print('Missing environment variables')

    with uow:
        if uow.user.get_by_id(user_id) is None:
            # TODO: Raise error
            print('User not found')

        actor = Actor(username, FEDERATION_ROOT_URL)
        actor.generate_key_pair(ENCRYPTION_KEY)

        print(actor)
