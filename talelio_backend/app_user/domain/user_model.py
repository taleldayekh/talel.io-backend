class User:

    def __init__(self, username: str, location: str = '', avatar_url: str = 'default.jpg') -> None:
        self.username = username
        self.location = location
        self.avatar_url = avatar_url
