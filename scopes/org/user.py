# scopes.org.user

"""Basic user account (principal) definitions + access to identity provider."""

from scopes.web import client
from scopes import util

import config


@dataclass
class User:

    name: str
    login: str
    email: str
    fullName: str


class ExtUser:
    """All infos for exchanging user data with an external service.

       This base class implements the zitadel interface. For other
       identity providers sublass accordingly.
    """

    provider = 'zitatel'
    endpoints = dict(
            users='v2/users',
    )

    def __init__(self, user, organization, userId=None, userIdPrefix=''):
        self.user = user

    def asDict(self):
        return dict(username=self.user.name)

    def send(self):
        clt = client.ApiClient(config.oidc_provider)
        data = self.asDict()
        res = clt.post(config.oidc_provider_endpoints['users'], data)

   grants: List[str]
