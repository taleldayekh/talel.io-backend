from os import getenv

from talelio_backend.app_social.domain.actor_model import Actor, ActorModel
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.shared.exceptions import UserError


def get_actor(uow: UnitOfWork, username: str) -> ActorModel:
    FEDERATION_ROOT_URL = getenv('SOCIALS_FEDERATION_ROOT_URL')

    if not FEDERATION_ROOT_URL:
        raise ValueError('Missing "SOCIALS_FEDERATION_ROOT_URL" environment variable')

    with uow:
        actor = uow.social.get_actor_by_username(username)

        if not actor:
            raise UserError(f"Actor with username '{username}' not found")

        db_actor = Actor.from_db(actor, FEDERATION_ROOT_URL)

        return db_actor.to_dict()
