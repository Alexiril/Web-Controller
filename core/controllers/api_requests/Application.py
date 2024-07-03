from typing import Any
from core.ApiRequest import ApiRequest
from core.Application import applications
from core.Exceptions import IncorrectApiRequestException, IncorrectApplicationRequestException, UnauthorizedException

class GetApplications(ApiRequest):

    def __call__(self) -> list[dict[str, Any]]:
        if self.user == None:
            raise UnauthorizedException("API request requires authentication.")
        with applications as _apps:
            result = [_apps[x] for x in self.user.granted_apps if x in _apps]
        result = [{
            'id': x.id,
            'headline': x.name,
            'icon': x.icon
        } for x in result]
        return result
    
class ApplicationRequest(ApiRequest):

    def __call__(self) -> Any:
        if self.user == None:
            raise UnauthorizedException("User must be authenticated to use the app request.")
        if type(self.data) != dict:
            raise IncorrectApiRequestException('Incorrect input JSON')
        appid = self.data.get("appid", "")
        with applications as apps:
            if appid not in apps or appid not in self.user.granted_apps:
                raise IncorrectApplicationRequestException(f'Unknown app {appid}')
            rh = apps[appid].request_handler
        return rh(self.handler,
                  self.user,
                  self.data.get("command", ""),
                  self.data.get("data", {}))