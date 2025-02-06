from talelio_backend.data.uow import UnitOfWork


# TODO: Return type
def get_actor(uow: UnitOfWork, username: str) -> None:
    # !
    print(username)
    # !

    with uow:
        actor = uow.social.get_actor_by_username(username)

        print(actor)

        # TODO: Include liked?
        # TODO: Return directly
        return {}
