from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

from rest_framework.exceptions import NotAcceptable

import base64, random, binascii, string

key = 'AAAAAAAAAAAAAAAA'


def encrypt(raw):
    raw = pad(raw.encode(), 16)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    encrypted = base64.b64encode(cipher.encrypt(raw))

    return encrypted.decode('utf-8', 'ignore')
