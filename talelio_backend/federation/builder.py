from datetime import timezone

from talelio_backend.app_social.domain.post_model import MediaType, PostModel


# TODO: Return type
def build_activitypub_create_activity(post: PostModel):
    attachment = [{
        'type':
        media.type.value.title(),
        'mediaType': (f'{media.type.value}/jpeg'
                      if media.type == MediaType.IMAGE else f'{media.type.value}/mp4'),
        'url':
        media.url,
        'name':
        media.alt,
        'summary':
        media.alt,
    } for media in post.media] if post.media else []

    return {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': f'https://social.talel.io/users/talel/outbox/{post.id}',
        'published': post.created_at.replace(tzinfo=timezone.utc),
        'type': 'Create',
        'actor': 'https://social.talel.io/users/talel',
        'to': post.audience.to,
        'cc': post.audience.cc,
        'object': {
            'id': f'https://social.talel.io/users/talel/objects/{post.id}',
            'published': post.created_at.replace(tzinfo=timezone.utc),
            'type': 'Note',
            'content': post.content,
            'attachment': attachment,
            'attributedTo': 'https://social.talel.io/users/talel',
            'to': post.audience.to,
            'cc': post.audience.cc,
        }
    }


# def build_atproto_post_record():
#     pass
