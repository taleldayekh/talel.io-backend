from dataclasses import dataclass


@dataclass
class User:
    username: str
    location: str = ''
    avatar_url: str = 'default.jpg'
