# scopes.web.client

"""Web client functionality: access to web sites, APIs - including authentication."""

from datetime import datetime, timedelta, timezone
import json
import jwt
import requests

import config


def postApi(url, token=None):
    if token is None:
        token = authenticateJwt()
    headers = dict(Authorization=f'Bearer {token}')
    resp = requests.post(url, headers=headers)
    data = resp.json()
    data['_auth_token'] = token
    return data

def authenticateJwt(paramsName='zitadel_params'):
    params = getattr(config, paramsName)
    keyData = loadPrivateKeyData(params['private_key_file'])
    userId = keyData['userId']
    keyId = keyData['keyId']
    key = keyData['key']
    now = datetime.now(timezone.utc)
    token_lifetime=params.get('token_lifetime', 60)
    payload = dict(
            iss=userId, sub=userId, aud=config.oidc_provider,
            iat=now, exp=now + timedelta(minutes=token_lifetime),
    )
    jwToken = jwt.encode(payload, key, algorithm="RS256", 
                         headers=dict(alg='RS256', kid=keyId))
    data = dict(
            grant_type='urn:ietf:params:oauth:grant-type:jwt-bearer',
            scope='openid urn:zitadel:iam:org:project:id:zitadel:aud',
            assertion=jwToken,
    )
    print(data)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = config.oidc_provider + '/oauth/v2/token'
    print(url)
    resp = requests.post(url, data=data, headers=headers)
    if resp.status_code != 200:
        print(resp.text)
        return None
    tdata = resp.json()
    return tdata['access_token']

def loadPrivateKeyData(fn='.private-key.json'):
    with open(fn) as f:
        return json.load(f)
