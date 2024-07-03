from core.Exceptions import IncorrectApiRequestException, IncorrectAuthAttemptException
from core.ApiRequest import ApiRequest
from core.User import users
from core.Token import MakeAuthToken

class MakeAuthTokenApiRequest(ApiRequest):

    def __call__(self) -> str:
        if type(self.data) != dict:
            raise IncorrectApiRequestException('Incorrect input JSON')
        with users as _users:
            if self.data['user'] not in _users:
                raise IncorrectAuthAttemptException('Incorrect user id or key')
            if not (user := _users[self.data['user']]).check_key(self.data['key']):
                raise IncorrectAuthAttemptException('Incorrect user id or key')
        return MakeAuthToken(user)