import json, os, base64, requests, random, string, time, datetime
from pystyle import Colors, Colorate, Center
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from modules.logging import Logging
from modules.output import Output

class General:
    def __init__(self):
        self.logging = Logging()
        self.output  = Output()
        self.config  = {}
        self.type    = 0


    def load_config(self):
        with open("Assets/Config.json", "r") as f:
            config = json.load(f)
            self.config = config
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
            preses = config.get("Modules", {}).get("custompresence", False)
            footer = config.get("Modules", {}).get("customfooter", False)

            if tcrypt:
                self.clear()
                self.art()
                tpass  = input("[>] Enter encryption password: ")
                try:
                    token  = self.tdecrypt(token, tpass)
                    if userps:
                        userps = self.tdecrypt(userps, tpass)
                except Exception as e:
                    self.logging.Error("Invalid encryption password.")
                    input("[>] Press enter to exit.")
                    exit()
        return token, prefix, nitro, msgl, antitl, autolo, userps, tcrypt, gelkey, userid, givesn, preses, footer
    
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

    def loadtype(self):
        with open("Assets/Config.json", "r") as f:
            self.type = json.load(f)["Type"]

    def basic_padding(self, array):
        return max(len(name) for _, name in array)
    
    def help_format(self, dic):
        prefix = self.config.get("Prefix", "")
        array = []
        for command in dic:
            param2 = ""
            params = command.get("params")
            for param in params:
                param2 += "({}) ".format(param[0])
            array.append((command.get("name"), param2, command.get("description")))
        options      = [prefix + option if option      else "(None)" for option, _, _      in array]
        arguments    = [argument        if argument    else "(None)" for _, argument, _    in array]
        descriptions = [description     if description else "(None)" for _, _, description in array]
        table = [("Commands", options), ("Arguments", arguments), ("Description", descriptions)]
        return table
    
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
            return (True, response.status_code, response.json())
        else:
            return (False, response.status_code, response.json())
        
    def load_givesniper_settings(self):
        with open("Assets/Settings/givesniper.json", "r") as f:
            return json.load(f)
        
    def load_nitrosniper_settings(self):
        with open("Assets/Settings/nitrosniper.json", "r") as f:
            return json.load(f)
        
    def load_massreact_settings(self):
        with open("Assets/Settings/massreact.json", "r") as f:
            return json.load(f)
        
    def randomnstring(self, length):
        return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    
    def ping(self, page):
        start = time.time()
        if "https://" not in page:
            page = "https://" + page
        requests.get(page)
        end = time.time()
        timems = int((end - start) * 1000)
        return str(timems)
    
    def guildid_name(self, id):
        api = "https://discord.com/api/v9/guilds/{}".format(id)
        r = requests.get(api, headers={"authorization": self.config.get("Token")})
        if r.status_code == 200:
            return r.json()["name"]
        else:
            return "Not found"
        
    def get_footer(self):
        with open("Assets/Settings/footer.json", "r") as f:
            return json.load(f)
    
    def update_logons(self):
        with open("Assets/Settings/Cache.json", 'r') as f:
            config = json.load(f)

            logons = config["Logons"]
            logons = int(logons) + 1
            config["Logons"] = logons

            with open("Assets/Settings/Cache.json", 'w') as f:
                json.dump(config, f, indent=4)

    def update_uptime(self):
        while True:
            with open("Assets/Settings/Cache.json", 'r') as f:
                config = json.load(f)

                uptime = config["Uptime"]
                uptime = int(uptime) + 1
                config["Uptime"] = uptime

                with open("Assets/Settings/Cache.json", 'w') as f:
                    json.dump(config, f, indent=4)


            time.sleep(1)
            