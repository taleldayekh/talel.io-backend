from base64 import b64decode, b64encode
from dataclasses import dataclass, field

from talelio_backend.shared.utils.crypto import encrypt, generate_key_pair


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

    def generate_key_pair(self, encryption_key: str) -> None:
        private_key, public_key = generate_key_pair()
        encryption_key_bytes = b64decode(encryption_key)

        encrypted_private_key = encrypt(private_key, encryption_key_bytes)

        private_key_str = b64encode(encrypted_private_key).decode('utf-8')
        public_key_str = public_key.decode('utf-8')

        self.private_key = private_key_str
        self.public_key = public_key_str

    # TODO
    @classmethod
    def from_db(cls) -> 'Actor':
        pass

    # TODO
    def to_dict(self):
        pass
