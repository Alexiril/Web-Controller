from jwt import encode, decode
from core.User import User


class AuthToken:

    def __init__(self, user: User) -> None:
        self.user: User = user
        #self.value = encode({}, )