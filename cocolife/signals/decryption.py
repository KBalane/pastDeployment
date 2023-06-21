from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

from rest_framework.exceptions import NotAcceptable

import base64, random, binascii, string

key = 'AAAAAAAAAAAAAAAA'


def decrypt(enc):
    try:
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        decrypted = unpad(cipher.decrypt(enc), 16)

        return decrypted.decode('utf-8', 'ignore')
    except Exception as e:
        raise NotAcceptable(detail=str(e))
