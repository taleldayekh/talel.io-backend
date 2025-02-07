from base64 import b64decode, b64encode, urlsafe_b64decode
from dataclasses import dataclass, field
from typing import TypedDict

from talelio_backend.shared.utils.crypto import encrypt, generate_key_pair


class ActorModelPublicKey(TypedDict):
    id: str
    owner: str
    publicKeyPem: str


class ActorModel(TypedDict):
    context: str
    id: str
    type: str
    preferredUsername: str
    inbox: str
    outbox: str
    followers: str
    following: str
    publicKey: ActorModelPublicKey


@dataclass
class Actor:
    username: str
    federation_root_url: str
    type: str = field(default='Person')
    actor_url: str = field(init=False)
    inbox_url: str = field(init=False)
    outbox_url: str = field(init=False)
    followers_url: str = field(init=False)
    following_url: str = field(init=False)
    liked_url: str = field(init=False)
    public_key = ''
    private_key = ''

    def __post_init__(self) -> None:
        self.actor_url = f'{self.federation_root_url}/users/{self.username}'
        self.inbox_url = f'{self.actor_url}/inbox'
        self.outbox_url = f'{self.actor_url}/outbox'
        self.followers_url = f'{self.actor_url}/followers'
        self.following_url = f'{self.actor_url}/following'
        self.liked_url = f'{self.actor_url}/liked'

    # TODO: Reiterate
    def generate_key_pair(self, encryption_key: str) -> None:
        private_key, public_key = generate_key_pair()

        encrypted_private_key = encrypt(private_key, encryption_key.encode('utf-8'))

        private_key_str = b64encode(encrypted_private_key).decode('utf-8')
        public_key_str = public_key.decode('utf-8')

        self.private_key = private_key_str
        self.public_key = public_key_str

    @classmethod
    def from_db(cls, actor_record, federation_root_url) -> 'Actor':
        actor = cls(username=actor_record[4], federation_root_url=federation_root_url)

        actor.type = actor_record[5]
        actor.actor_url = actor_record[6]
        actor.inbox_url = actor_record[7]
        actor.outbox_url = actor_record[8]
        actor.followers_url = actor_record[9]
        actor.following_url = actor_record[10]
        actor.liked_url = actor_record[11]
        actor.public_key = actor_record[12]

        return actor

    def to_dict(self) -> ActorModel:
        return {
            'context': 'https://www.w3.org/ns/activitystreams',
            'id': self.actor_url,
            'type': self.type,
            'preferredUsername': self.username,
            'inbox': self.inbox_url,
            'outbox': self.outbox_url,
            'followers': self.followers_url,
            'following': self.following_url,
            'publicKey': {
                'id': f'{self.actor_url}#main-key',
                'owner': self.actor_url,
                'publicKeyPem': self.public_key,
            }
        }
