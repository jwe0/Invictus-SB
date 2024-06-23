import os, json,sqlite3
from modules.general import General

class Init:
    def __init__(self):
        self.general = General()

    def assets(self):
        if not os.path.exists("Assets"):
            os.mkdir("Assets")

    def msglogs(self):
        if not os.path.exists("Assets/Logs"):
            os.mkdir("Assets/Logs")

    def ipcache(self):
        if not os.path.exists("Assets/IPcache.json"):
            open("Assets/IPcache.json", "w").close()

    def config(self):
        if not os.path.exists("Assets/Config.json"):
            self.general.clear()
            self.general.art()
            with open("Assets/Config.json", "w") as f:
                output_modes = ["codeblock"]
                token  = input("[>] User token     : ")
                prefix = input("[>] Command prefix : ")
                output = input("[>] Output mode    : ")
                while output not in output_modes:
                    output = input("[!] Invalid output mode. Try again: ")
                nitro  = input("[>] Nitro sniper?  : ")
                msglog = input("[>] Log messages?  : ")
                tcrypt = input("[>] Encrypt token? : ")
                if tcrypt.lower() == "y":
                    tpass = input("[>] Enter encryption password: ")
                    token = self.general.tcrypt(token, tpass)
                antitl = input("[>] Anti tokenlog? : ")
                autolo = input("[>] Auto logout?   : ")
                if autolo.lower() == "y":
                    userpass = input("[>] Enter account password: ") 
                    if tcrypt.lower() == "y":
                        userpass = self.general.tcrypt(userpass, tpass)
                gelkey   = input("[>] Enter gelbooru API key: ")
                if gelkey:
                    userid = input("[>] Enter gelbooru user ID: ")
                json.dump({"Token": token, "Prefix": prefix, "Output": output, "Modules": {"nitro": True if nitro.lower() == "y" else False, "msglog": True if msglog.lower() == "y" else False, "antitokenlog": True if antitl.lower() == "y" else False, "autologout": True if autolo.lower() == "y" else False}, "Keys" : {"gelboorukey": gelkey, "gelbooruid": userid}, "TCrypt": True if tcrypt.lower() == "y" else False, "Account": {"password": userpass} if autolo.lower() == "y" else {}}, f, indent=4)

    def initalizesql(self):
        if not os.path.exists("Databases"):
            os.mkdir("Databases")
        
        if not os.path.exists("Databases/messages.db"):
            conn = sqlite3.connect("Databases/messages.db")
            c = conn.cursor()
            c.execute("CREATE TABLE messages (userid TEXT, username TEXT, message TEXT, time TEXT)")
            conn.commit()
            conn.close()
        
        if not os.path.exists("Databases/deleted.db"):
            conn = sqlite3.connect("Databases/deleted.db")
            c = conn.cursor()
            c.execute("CREATE TABLE messages (userid TEXT, username TEXT, message TEXT, time TEXT)")
            conn.commit()
            conn.close()




    def init(self):
        self.assets()
        self.config()
        self.ipcache()
        self.msglogs()
        self.initalizesql()