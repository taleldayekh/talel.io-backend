from talelio_backend.app_social.domain.post_model import AudienceModel, MediaModel, PostModel
from talelio_backend.data.uow import UnitOfWork


def publish_post(uow: UnitOfWork, user_id: int, platforms, post):
    with uow:
        # TODO: Replace actor with identity
        identity = uow.social.get_actor_by_user_id(user_id)

        if not identity:
            print('No social identity found for user')
            # TODO: Raise a custom exception
            pass

        # TODO: Check this value
        print('Identity')
        print(identity)

        media = [MediaModel(**media) for media in post.get('media', [])]
        audience = AudienceModel(**post.get('audience', {}))

        post = PostModel(
            platforms=platforms,
            content=post.get('content'),
            media=media,
            audience=audience,
        )

        errors = post.validate_for_platforms()

        # TODO: Platforms cannot be empty, does the validator consider this?

        if errors:
            print('Platform validation failed')
            # TODO: Raise a custom exception
            pass

        # uow.social.create_post(post)
