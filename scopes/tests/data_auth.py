# scopes.tests.data_auth

"""provide response data for testing (via dummy_requests)"""

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
        "kid": "316638486247563085",
        "alg": "RS256",
        "n": "167qFCfRa0tRR0MZv-PQVwdiVFf0NtfN-zFAogRASm6437sbXfsfxkpbh1F77TwQdl4qlR5Na_Ecs8VTxOuyHmuhIJ4FyZV4M0h71KRw7LCTVuNw7mWLpbjKPBzidyhctbkJrkcKtJymnHELsct0CdT16Lb27phd_0cBJexGbwhVNQBs10VbkvUJHHOJe6A_JVS9Q3_3MEWyCyFoHPeMchlk_Gd6yMiH4aJ1ql3GZD6c2JB9crloTH_oPWWFQObGoXTKcFonEBdkrwuCQfRVOfGh8UIhIcTM0JNgqtQOCcIkf0emfI30SoWSc6Qz8lU70Vpmb3qQgsqATFICgzgABw",
        "e": "AQAB"},
       {"use": "sig",
        "kty": "RSA",
        "kid": "316766976250797901",
        "alg": "RS256",
        "n": "yZKIsrUWT2fEj4OtUUFYQbEe_Clodz464tn5vMAQ0q8zV07bqFaA7WKuBflowYctDNxoxdbiFNISpKEOx6yFnx7_g6Zd46DWsj5ggGZvNkgOa9SqTIsA7ho9nk7LDLQRpV0k5N1HkiG66GUqUCV2llJhstpTDQQLDvhI3qussG2HyylpTQSu-9b6gry0rb397yjAnXQu6tFOubEDteTN0fLNMblcdd2AvZKpGA2o_-M5U6AckezfmBCBdHWmrwxpjGGf7KWqGg8j6bJkV3sMg4XfD2x0KNog_3D-0pSx6k8dSWZGkNlDxB5AdWvNDYg1stkvjeNEbIJAhv0-awLs9Q",
        "e": "AQAB"}]}
}

from scopes.tests.dummy_requests import response_data
response_data.update(oidc_data)
