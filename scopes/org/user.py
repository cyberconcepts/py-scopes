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
    displayName: str = ''
    groups: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.displayName:
            self.displayName = ' '.join((self.firstName, self.lastName))


class ExtUser:
    """All infos for exchanging user data with an external service.

       This base class implements the zitadel interface (as of version 3.3.2). 
       For other identity providers sublass accordingly.
    """

    provider = 'zitatel'
    endpoints = dict(
            users_human='v2/users/human',
            #create_authorization='management/v1/zitadel.authorization.v2beta.AuthorizationService/CreateAuthorization',
            create_authorization='v2beta/authorizations',
    )

    def __init__(self, user, idPrefix=''):
        self.user = user
        self.userId = idPrefix + user.login
        self.client = client.ApiClient(config.oidc_provider)

    def asDict(self):
        params = config.oidc_params
        data = dict(
            userId=self.userId,
            username=self.user.login,
            email=dict(email=self.user.email, isVerified=True),
            profile=dict(
                givenName=self.user.firstName,
                familyName=self.user.lastName,
                displayName=self.user.displayName,
            ),
            organization=dict(orgId=params['organization_id']),
        )
        return data

    def create(self, updateIfExists=False):
        data = self.asDict()
        if self.user.hashedPassword:
            data['hashedPassword'] = self.user.hashedPassword
        status, res = self.client.post(self.endpoints['users_human'], data)
        if status > 201:
            if updateIfExists:
                return self.update()
        return status, res
        #if self.user.groups:
            #return self.createGroups()

    def update(self, createIfMissing=False):
        data = self.asDict()
        if self.user.hashedPassword:
            data['password'] = dict(hashedPassword=self.user.hashedPassword)
        status, res = self.client.put(self.endpoints['users_human'], self.userId, data)
        if status > 200:
            if createIfMissing:
                return self.create()
            else:
                return status, res
        #if self.user.groups:
            #return self.updateGroups()

    def createGroups(self):
        data = dict(
                userId=self.userId,
                projectId=config.oidc_params['project_id'],
                roleKeys=self.user.groups,
        )
        return self.client.post(self.endpoints['create_authorization'], data)
