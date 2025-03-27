# scopes.util

import base64
import hashlib
from secrets import choice
import string

# random strings, hashes, encodings
# for authentication, encryption, and other purposes

BASE = string.ascii_letters + string.digits
BASE2 = BASE + '-._~'

def rndstr(size=16):
    return ''.join([choice(BASE) for _ in range(size)])

def rndstr2(size=64):
    return ''.join([choice(BASE2) for _ in range(size)])

def b64e(b):
    return base64.urlsafe_b64encode(b).rstrip(b'=')

def hashS256(s):
    h = hashlib.sha256(s.encode('ascii')).digest()
    return b64e(h).decode('ascii')

