# scopes.tests.data_auth

"""provide response data for testing (via dummy_requests)"""

from cryptography.hazmat.primitives.asymmetric import rsa
from scopes import util

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()
public_key_n = util.b64e(public_key.public_numbers().n.to_bytes(256)).decode('ASCII')

oidc_data = {
    'test://oidc/.well-known/openid-configuration': {
        "issuer": "test://oidc",
        "authorization_endpoint": "test://oidc/oauth/v2/authorize",
        "token_endpoint": "test://oidc/oauth/v2/token",
        "introspection_endpoint": "test://oidc/oauth/v2/introspect",
        "userinfo_endpoint": "test://oidc/oidc/v1/userinfo",
        "revocation_endpoint": "test://oidc/oauth/v2/revoke",
        "end_session_endpoint": "test://oidc/oidc/v1/end_session",
        "device_authorization_endpoint": "test://oidc/oauth/v2/device_authorization",
        "jwks_uri": "test://oidc/oauth/v2/keys"},
    'test://oidc/oauth/v2/keys': { "keys": [
       {"use": "sig",
        "kty": "RSA",
        "kid": "316766976250797901",
        "alg": "RS256",
        "n": public_key_n,
        "e": "AQAB"}]},
    'test://oidc/oauth/v2/token': {
        "access_token": "abcde12345"},
    'test://oidc/v2/users/human': {
        "code": 1}
}

from scopes.tests.dummy_requests import response_data
response_data.update(oidc_data)
