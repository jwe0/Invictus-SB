import json, os, base64, requests
from pystyle import Colors, Colorate, Center
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class General:
    def __init__(self):
        pass

    def load_config(self):
        with open("Assets/Config.json", "r") as f:
            config = json.load(f)

            token  = config.get("Token", "")
            prefix = config.get("Prefix", "")

            nitro  = config.get("Modules", {}).get("nitro", False)
            msgl   = config.get("Modules", {}).get("msglog", False)
            tcrypt = config.get("TCrypt", False)
            antitl = config.get("Modules", {}).get("antitokenlog", False)
            autolo = config.get("Modules", {}).get("autologout", False)
            userps = config.get("Account", {}).get("password", "")
            gelkey = config.get("Keys", {}).get("gelbooru", "")
            userid = config.get("Keys", {}).get("gelbooruuser", "")
            givesn = config.get("Modules", {}).get("givesniper", False)
            if tcrypt:
                self.clear()
                self.art()
                tpass  = input("[>] Enter encryption password: ")
                token  = self.tdecrypt(token, tpass)
                userps = self.tdecrypt(userps, tpass)
        return token, prefix, nitro, msgl, antitl, autolo, userps, tcrypt, gelkey, userid, givesn
    
    def art(self):
        ascii_art = """

 ██▓ ███▄    █ ██▒   █▓ ██▓ ▄████▄  ▄▄▄█████▓ █    ██   ██████      ██████  ▄▄▄▄   
▓██▒ ██ ▀█   █▓██░   █▒▓██▒▒██▀ ▀█  ▓  ██▒ ▓▒ ██  ▓██▒▒██    ▒    ▒██    ▒ ▓█████▄ 
▒██▒▓██  ▀█ ██▒▓██  █▒░▒██▒▒▓█    ▄ ▒ ▓██░ ▒░▓██  ▒██░░ ▓██▄      ░ ▓██▄   ▒██▒ ▄██
░██░▓██▒  ▐▌██▒ ▒██ █░░░██░▒▓▓▄ ▄██▒░ ▓██▓ ░ ▓▓█  ░██░  ▒   ██▒     ▒   ██▒▒██░█▀  
░██░▒██░   ▓██░  ▒▀█░  ░██░▒ ▓███▀ ░  ▒██▒ ░ ▒▒█████▓ ▒██████▒▒   ▒██████▒▒░▓█  ▀█▓
░▓  ░ ▒░   ▒ ▒   ░ ▐░  ░▓  ░ ░▒ ▒  ░  ▒ ░░   ░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░   ▒ ▒▓▒ ▒ ░░▒▓███▀▒
 ▒ ░░ ░░   ░ ▒░  ░ ░░   ▒ ░  ░  ▒       ░    ░░▒░ ░ ░ ░ ░▒  ░ ░   ░ ░▒  ░ ░▒░▒   ░ 
 ▒ ░   ░   ░ ░     ░░   ▒ ░░          ░       ░░░ ░ ░ ░  ░  ░     ░  ░  ░   ░    ░ 
 ░           ░      ░   ░  ░ ░                  ░           ░           ░   ░      
                   ░       ░                                                     ░ 

"""

        print(Colorate.Vertical(Colors.red_to_green, Center.XCenter(ascii_art)))

    def clear(self):
        os.system("clear") if os.name != "nt" else os.system("cls")

    def basic_padding(self, array):
        return max(len(name) for _, name in array)
    
    def help_format(self, dic):
        array = []

        for command in dic:
            param2 = ""
            name = command.get("name")
            description = command.get("description")
            params = command.get("params")
            for param in params:
                param2 += "[{}] ".format(param[0])
            array.append((name, param2, description))


        message = ""
        options      = []
        arguments    = []
        descriptions = []

        for option, argument, description in array:
            options.append(option)
            arguments.append(argument if argument else "[None]")
            descriptions.append(description)


        options_padding   = max(len(option) for option in options) + 2
        arguments_padding = max(len(argument) for argument in arguments) + 2


        message += f"{'Command'.ljust(options_padding)} | {'Arguments'.ljust(arguments_padding)} | Description\n"
        for i in range(len(options)):
            message += f"{options[i].ljust(options_padding)} | {arguments[i].ljust(arguments_padding)} | {descriptions[i]}\n"
        
        

        return message
    
    def removespecial(self, message):
        return message.replace("'", "").replace('"', "").replace("ansii", "").replace("`", "")
    
    def tcrypt(self, token, key):
        data = token.encode()

        while len(key) < 16:
            key += "*"

        key = key.encode()

        cipher = AES.new(key, AES.MODE_CBC)
        dbytes = cipher.encrypt(pad(data, AES.block_size))

        iv = base64.b64encode(cipher.iv).decode()
        ct = base64.b64encode(dbytes).decode()

        result = json.dumps({"iv": iv, "ciphertext": ct})

        return base64.b64encode(result.encode()).decode()
    
    def tdecrypt(self, token, key):
        token = json.loads(base64.b64decode(token).decode())

        iv = base64.b64decode(token["iv"])
        ct = base64.b64decode(token["ciphertext"])

        while len(key) < 16:
            key += "*"

        key = key.encode()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        data = unpad(cipher.decrypt(ct), AES.block_size)

        return data.decode()

    def checktoken(self, token):
        api = "https://discord.com/api/v9/users/@me"

        headers = {
            "authorization": token
        }

        response = requests.get(api, headers=headers)

        if response.status_code == 200:
            return True
        else:
            return False