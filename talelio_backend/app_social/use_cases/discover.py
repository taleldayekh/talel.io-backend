from typing import List, TypedDict

from talelio_backend.data.uow import UnitOfWork
from talelio_backend.shared.exceptions import UserError


class WebFingerLink(TypedDict):
    rel: str
    type: str
    href: str


class WebFinger(TypedDict):
    subject: str
    links: List[WebFingerLink]


def webfinger_discover(uow: UnitOfWork, username: str) -> WebFinger:
    with uow:
        actor = uow.social.get_actor_by_username(username)

        if not actor:
            raise UserError(f"Actor with username '{username}' not found")

        return {
            'subject': f"acct:{username}@talel.io",
            'links': [{
                'rel': 'self',
                'type': 'application/activity+json',
                'href': actor[6],
            }]
        }
