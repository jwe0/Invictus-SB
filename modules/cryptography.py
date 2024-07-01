import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class Crypto:
    def __init__(self):
        pass

    def rot(self, string, mode="encode", shift=13):
        alph = 'abcdefghijklmnopqrstuvwxyz'
        if mode == "encode":
            result = ''.join(alph[(alph.index(char) + shift) % 26] if char in alph else char for char in string)
        elif mode == "decode":
            result = ''.join(alph[(alph.index(char) - shift) % 26] if char in alph else char for char in string)

        return result
    
    def b64(self, string, mode="encode"):
        if mode == "encode":
            result = base64.b64encode(string.encode()).decode()
        elif mode == "decode":
            result = base64.b64decode(string.encode()).decode()

        return result