import base64, json
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
    
    def aes_cbc(self, string, key, mode):
        data = string.encode()
        key  = key.encode()
        if mode == "encode":
            cipher = AES.new(key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    
            iv = base64.b64encode(cipher.iv).decode()
            ct = base64.b64encode(ct_bytes).decode()
    
            result = json.dumps({"iv": iv, "ciphertext": ct})
    
            return base64.b64encode(result.encode()).decode()

        elif mode == "decode":
            token = json.loads(base64.b64decode(string).decode())
    
            iv = base64.b64decode(token["iv"])
            ct = base64.b64decode(token["ciphertext"])
    
            cipher = AES.new(key, AES.MODE_CBC, iv)
            data = unpad(cipher.decrypt(ct), AES.block_size)
    
            return data.decode()

    def aes_ctr(self, string, key, mode):
        data = string.encode()
        key  = key.encode()
        if mode == "encode":
            cipher = AES.new(key, AES.MODE_CTR)
            ct_bytes = cipher.encrypt(data)

            iv = base64.b64encode(cipher.nonce).decode()
            ct = base64.b64encode(ct_bytes).decode()

            result = json.dumps({"iv": iv, "ciphertext": ct})

            return base64.b64encode(result.encode()).decode()

        elif mode == "decode":
            token = json.loads(base64.b64decode(string).decode())

            iv = base64.b64decode(token["iv"])
            ct = base64.b64decode(token["ciphertext"])

            cipher = AES.new(key, AES.MODE_CTR, nonce=iv)
            data = cipher.decrypt(ct)

            return data.decode()

    def aes_cfb(self, string, key, mode):
        data = string.encode()
        key  = key.encode()
        if mode == "encode":
            cipher = AES.new(key, AES.MODE_CFB)
            ct_bytes = cipher.encrypt(data)

            iv = base64.b64encode(cipher.iv).decode()
            ct = base64.b64encode(ct_bytes).decode()

            result = json.dumps({"iv": iv, "ciphertext": ct})

            return base64.b64encode(result.encode()).decode()

        elif mode == "decode":
            token = json.loads(base64.b64decode(string).decode())

            iv = base64.b64decode(token["iv"])
            ct = base64.b64decode(token["ciphertext"])

            cipher = AES.new(key, AES.MODE_CFB, iv)
            data = cipher.decrypt(ct)

            return data.decode()

    def aes_ofb(self, string, key, mode):
        data = string.encode()
        key  = key.encode()
        if mode == "encode":
            cipher = AES.new(key, AES.MODE_OFB)
            ct_bytes = cipher.encrypt(data)

            iv = base64.b64encode(cipher.iv).decode()
            ct = base64.b64encode(ct_bytes).decode()

            result = json.dumps({"iv": iv, "ciphertext": ct})

            return base64.b64encode(result.encode()).decode()

        elif mode == "decode":
            token = json.loads(base64.b64decode(string).decode())

            iv = base64.b64decode(token["iv"])
            ct = base64.b64decode(token["ciphertext"])

            cipher = AES.new(key, AES.MODE_OFB, iv)
            data = cipher.decrypt(ct)

            return data.decode()