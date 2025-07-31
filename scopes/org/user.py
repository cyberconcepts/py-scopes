# scopes.org.user

"""Basic user account (principal) definitions + access to identity provider."""

from dataclasses import dataclass, field
from typing import List, Optional

from scopes.web import client
from scopes import util

import config


@dataclass
class User:

    login: str
    email: str
    hashedPassword: Optional[str] = None
    firstName: str = ''
    lastName: str = ''
    grants: List[str] = field(default_factory=list)


class ExtUser:
    """All infos for exchanging user data with an external service.

       This base class implements the zitadel interface (as of version 3.3.2). 
       For other identity providers sublass accordingly.
    """

    provider = 'zitatel'
    endpoints = dict(
            users_human='v2/users/human',
    )

    def __init__(self, user, idPrefix=''):
        self.user = user
        self.userId = idPrefix + user.login

    def asDict(self):
        params = config.oidc_params
        data = dict(
            userId=self.userId,
            username=self.user.login,
            email=dict(email=self.user.email, isVerified=True),
            profile=dict(
                givenName=self.user.firstName,
                familyName=self.user.lastName,
            ),
            organization=dict(orgId=params['organization_id']),
        )
        if self.user.hashedPassword:
            data['hashedPassword'] = self.user.hashedPassword
        return data

    def send(self):
        clt = client.ApiClient(config.oidc_provider)
        data = self.asDict()
        res = clt.post(self.endpoints['users_human'], data)

