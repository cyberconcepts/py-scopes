# scopes.tests.scratch

"""for keeping experimental and demonstration code and data (mainly for testing)"""

import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.utils import int_to_bytes
from scopes import util

# generate (and serialize) or load private key
# generate public JWKS (key set) from private ky

#private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
#pem = private_key.private_bytes(encoding=serialization.Encoding.PEM, 
#                                format=serialization.PrivateFormat.PKCS8,
#                                encryption_algorithm=serialization.NoEncryption())

pem = b'-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQD1ipW1hnV+OWF/\nE09YEQB9GTwQ0DUhmM1ZtmONV3xp1zrpLsvQtJJ6lZ8rp+ws35HGEEQWuBvgKP+K\nyyhILkgHp5LUtXsIruvo/+20Gbxr3bbIp2Omv8NuUnQIlb0SkZwauz/iLi+dFnoW\nTzkCwRnOPG+xqrSzD4CUCIZc4fU61h457I5PWTgK+bZXlsPytook9HpCIPX+9PaU\n935KHeWLonx3GZWqcqUyHSUn8dgRMypaKO70zCZkZWwDbCkJv7OUuY9QijN9niA+\nX3MFyqf9+WK7/lLnNYimdXk9Pz9Lim7HhoAApoW/0ueUfok54OIzuemTAUaunaN6\nmdOvh54dAgMBAAECggEAAWW5Vx7kAY1Bto104U51EEm519EvhUm6B5T4+VTp5LYK\nF1rEMIFwtBkoFfjzLJFEwEakJ8Hgq80TIRdyJ72r9ACIPGtTlH0Jjg94IqyvwOy6\n23fPEXkrLHR0Z5g8bR+6A95liQrA+tCD1QVFRAWUktlkVXfxRC95TMCA3i7rakGG\no6BbyUD2Hp7IEO5fbfKNiqrUO/LwvLOMBTe3Q9EVv7fblm21HiwWG26RgO29UtFo\nEKcaALSqIYwYCkc9EuLpcGRzLfH1opid3Xtu4+hm5enNgdXZRKr9lSQUCSi9oZRE\npszNGyDsaot2ixwKP3c6Eo3bQKMmXXw8Y3JsNiZzIQKBgQD8QuCjKyAeH0QrhW1Y\nvSmUC3q517WZPRgsEMx917MYn/Gl1ywsROjawP/ClxTZkpXVgALFvrggjB75p/QG\noFamZpf9U95fVivAkANQYmhGmqPVQUeb2vgHQOdPSdvvMoRumcEcfS/dOo9R//s+\nfrBQNYfp/tTttdyM2N0CzsuBzQKBgQD5LjX8SvLPe6q6xJchdExywbTk+DLtiKDs\nT5avaGhOqzYhir6FvEt7Gw74J6IWzIt5X4OteSkpRvj2TN0ik+KAfZOk+v9C5iK7\nxbicWj5XSaPJcYvhxogO7mb8sSrl/cY20HRkCsyQOKeH005PHsGZztZoHrsF6t2X\nbtKgNWp9kQKBgHLDHh09RlxNzx6Zkfh3/k1qt4eKmgQ/5hpN/ioWElVWloHjFSaC\npwi2GuT1BLhC1sWNejVqIaw08vaTMRI+qY0ESYsnN5hZxIfTPJ66VkQgn/4pt6Ex\nCfuKzHCm4la8vcDvVApY7YiQ1pjwguWYjy++WrnahBYs0UyGcG2RlMXVAoGBAJNJ\nf1ubqZ5+yNIQ9gwuRCno2dYl52SESCqmeLlCC7XEegCllCxUuoEP429HbgXv7dlW\nXe0iGvRtISflEyknJNEyaR0xx8RxZ8J6Ar9YkFTkEE44MajIww+gV3ux9Vtw/8LS\nwJmJ0JTHCC++9SDLW0BhBFcTIxVCWKz0MsfECyghAoGAOLm2dF59JiiiynGiWXzJ\nZcbZQStR+ysjLX+RqTATAorhweUiv+HwbB4boWhOnDD7q3t+93GnzeqI9m9Q5yo6\nRTyyNYa4uJXMMarZxi3m+RGvuCC2h+7ja6H6UGg3xrHNwcykJkuRAZvqCN+f6Nxo\njc8o9LMimQyTv+yptrOhi2w=\n-----END PRIVATE KEY-----\n'
private_key = serialization.load_pem_private_key(pem, password=None)
public_key = private_key.public_key()

nums = public_key.public_numbers()
#e = base64.urlsafe_b64encode(int_to_bytes(nums.e)).rstrip(b'=')
#e = base64.urlsafe_b64encode(nums.e.to_bytes(3)).rstrip(b'=')
e = b'AQAB'
#n = base64.urlsafe_b64encode(int_to_bytes(nums.n)).rstrip(b'=')
n = util.b64e(nums.n.to_bytes(256))

# data from example session with zitadel

keys_response = {"keys":[{"use":"sig","kty":"RSA","kid":"317781576895225677","alg":"RS256","n":"rBE2kf4S1-uLqTKoRcxmBDZXeNU0PcDZtXX3pYK4hbE_cVNqMnWZQNXh4asLvZ_VpInIRI_gRe5pFfrUfnFppnu7sgUGPHS_i6E1JSDWDDViwU0DbQXzTMA36xb8fI9vm_StrKqQ2snpkV2YprWC597vOa6w8eWMEfwWV39gmpgjyaYfwKi2ldvnn_djYSEyy6Cs8QW9L8uaTKDYUuuIY7iyjTRI7kM1boZcg26WQ4nDgSU8BMEmPGc-h7BHIm3PVEKNBUU3dRIcvIlnAx7AJoqdmUU0BllMGOd-To7PP760Vx4gYBsTFRGaQ_9P7vRApn0Wywnhj0BaVWGyJPkggQ","e":"AQAB"}]}

token_response = {'access_token': 'WGn4xjOluOgEugwqfxACziBZxAxQ1SKBKU6p27DysWw9slM55Fn7wkz_avpy5BjFR1uU_2rJoQTMNsO8NyxOEkmhbpP9xURUQrLRBiZT', 'token_type': 'Bearer', 'expires_in': 43199, 'id_token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjMxNzc4MTU3Njg5NTIyNTY3NyIsInR5cCI6IkpXVCJ9.eyJhbXIiOlsicHdkIl0sImF0X2hhc2giOiJQbC1kMjBvRG9DRHZqTUtGMmF4S3N3IiwiYXVkIjpbIjMxMTYxMzExOTgxNjM5MjUyNSIsIjMxNDQ2OTIwOTA3OTkzMDcwMSIsIjMxMTQ3MjQ1MTc2ODg2ODY4NSJdLCJhdXRoX3RpbWUiOjE3NDU5MTAxNTksImF6cCI6IjMxMTYxMzExOTgxNjM5MjUyNSIsImNsaWVudF9pZCI6IjMxMTYxMzExOTgxNjM5MjUyNSIsImVtYWlsIjoiaGVsbXV0Lm1lcnpAcG9zdGVvLmRlIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV4cCI6MTc0NTk1MzUwOSwiZmFtaWx5X25hbWUiOiJVc2VyIiwiZ2VuZGVyIjoibWFsZSIsImdpdmVuX25hbWUiOiJUZXN0IiwiaWF0IjoxNzQ1OTEwMzA5LCJpc3MiOiJodHRwczovL2ExLmN5Ny5kZSIsImxvY2FsZSI6ImRlIiwibmFtZSI6IlRlc3QgVXNlciIsIm5vbmNlIjoiMVJGem9RNDkyazNWTFEzcyIsInByZWZlcnJlZF91c2VybmFtZSI6InRzdDkiLCJzaWQiOiJWMV8zMTc3ODQyMjY2MjE2MTE4NTMiLCJzdWIiOiIzMTE4NDY3OTY3Mzk1MzQ2NjkiLCJ1cGRhdGVkX2F0IjoxNzQ1MzA1MTkzLCJ1cm46eml0YWRlbDppYW06b3JnOnByb2plY3Q6MzExNDcyNDUxNzY4ODY4Njg1OnJvbGVzIjp7ImNjLXVzZXIiOnsiMzExNDczNTAyMjc0MjQ4NTI1IjoiY3liZXJjb25jZXB0cy5hMS5jeTcuZGUifX0sInVybjp6aXRhZGVsOmlhbTpvcmc6cHJvamVjdDpyb2xlcyI6eyJjYy11c2VyIjp7IjMxMTQ3MzUwMjI3NDI0ODUyNSI6ImN5YmVyY29uY2VwdHMuYTEuY3k3LmRlIn19LCJ1cm46eml0YWRlbDppYW06dXNlcjpyZXNvdXJjZW93bmVyOmlkIjoiMzExNDczNTAyMjc0MjQ4NTI1IiwidXJuOnppdGFkZWw6aWFtOnVzZXI6cmVzb3VyY2Vvd25lcjpuYW1lIjoiY3liZXJjb25jZXB0cyIsInVybjp6aXRhZGVsOmlhbTp1c2VyOnJlc291cmNlb3duZXI6cHJpbWFyeV9kb21haW4iOiJjeWJlcmNvbmNlcHRzLmExLmN5Ny5kZSJ9.hx8JWXWVPq-WfBx9AMgFRWaEX3CioU8BCZwT3d8YETMejsR33LDsbPfnzO0Dbw885tiyNIsdNRj7lfk5HtuZVWdHx58hnaMw-czGhIfB0GXvuh2UFemBoLNJLajtRvCBi-YIZ_c6TD0Ryd2wn_yQlgY1J2R8xTsBWeKM_SYqlKU20r4r3nsX4krg6Q9x-Kc3k0Rg3lMXoxFYgQSzXrKjxTI3HHb03H4lzgmrdcbQqfbLoHKdvGxzfo-Gf8Rlt9rQ-fpGu7fRfPJQV14SPJ6CQtKP0adq_D2blcp1I1xKXML8TytJa05RjL_l_KH-segFfORtGMc4mYo8JUpMW0KOvg'}

token_id_claims = {'amr': ['pwd'], 'at_hash': 'Pl-d20oDoCDvjMKF2axKsw', 'aud': ['311613119816392525', '314469209079930701', '311472451768868685'], 'auth_time': 1745910159, 'azp': '311613119816392525', 'client_id': '311613119816392525', 'email': 'helmut.merz@posteo.de', 'email_verified': True, 'exp': 1745953509, 'family_name': 'User', 'gender': 'male', 'given_name': 'Test', 'iat': 1745910309, 'iss': 'https://a1.cy7.de', 'locale': 'de', 'name': 'Test User', 'nonce': '1RFzoQ492k3VLQ3s', 'preferred_username': 'tst9', 'sid': 'V1_317784226621611853', 'sub': '311846796739534669', 'updated_at': 1745305193, 'urn:zitadel:iam:org:project:311472451768868685:roles': {'cc-user': {'311473502274248525': 'cyberconcepts.a1.cy7.de'}}, 'urn:zitadel:iam:org:project:roles': {'cc-user': {'311473502274248525': 'cyberconcepts.a1.cy7.de'}}, 'urn:zitadel:iam:user:resourceowner:id': '311473502274248525', 'urn:zitadel:iam:user:resourceowner:name': 'cyberconcepts', 'urn:zitadel:iam:user:resourceowner:primary_domain': 'cyberconcepts.a1.cy7.de'}
