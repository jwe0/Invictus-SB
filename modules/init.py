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
            open("Assets/IPcache.json", "w").write("{}")

    def scripts(self):
        if not os.path.exists("Scripts"):
            os.mkdir("Scripts")

    def scrapes(self):
        if not os.path.exists("Scrapes"):
            os.mkdir("Scrapes")

    def settings(self):
        if not os.path.exists("Assets/Settings"):
            os.mkdir("Assets/Settings")

        if not os.path.exists("Assets/Settings/givesniper.json"):
            config = {
                "delay" : 1
            }

            with open("Assets/Settings/givesniper.json", "w") as f:
                json.dump(config, f, indent=4)

        if not os.path.exists("Assets/Settings/nitrosniper.json"):
            config = {
                "delay" : 1,
                "autoredeem" : True
            }

            with open("Assets/Settings/nitrosniper.json", "w") as f:
                json.dump(config, f, indent=4)

        if not os.path.exists("Assets/Settings/massreact.json"):
            config = {
                "emojis" : []
            }

            with open("Assets/Settings/massreact.json", "w") as f:
                json.dump(config, f, indent=4)

        if not os.path.exists("Assets/Presence.json"):
            config = {}

            with open("Assets/Presence.json", "w") as f:
                json.dump(config, f, indent=4)

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
                givesniper = input("[>] GiveSniper?     : ")
                custompres = input("[>] Custom presence? : ")

                json.dump({"Token": token, 
                           "Prefix": prefix, 
                           "Output": output, 
                           "Modules": {"nitro": True if nitro.lower() == "y" else False, 
                                       "msglog": True if msglog.lower() == "y" else False, 
                                       "antitokenlog": True if antitl.lower() == "y" else False, 
                                       "autologout": True if autolo.lower() == "y" else False, 
                                       "givesniper": True if givesniper.lower() == "y" else False, 
                                       "custompresence": True if custompres.lower() == "y" else False}, 
                            "Keys" : {"gelboorukey": gelkey, "gelbooruid": userid}, 
                            "TCrypt": True if tcrypt.lower() == "y" else False, 
                            "Account": {"password": userpass} if autolo.lower() == "y" else {}
                        }, f, indent=4)
                if custompres.lower() == "y":
                    self.presinit()
                
    def presinit(self):
        custompres = input("[>] Custom presence? : ")
        if custompres.lower() == "y":
            clientid = input("[>] Enter client ID: ")
            clientms = input("[>] Enter presence message: ")
            clientli = input("[>] Enter large image key: ")
            if clientli:
                clientlit = input("[>] Enter large image text: ")
            clientsi = input("[>] Enter small image key: ")
            if clientsi:
                clientsit = input("[>] Enter small image text: ")

            cb = input("[>] Buttons? : ")
            if cb.lower() == "y":
                buttons = []
                print("[*] Enter !q to quit buttons")
                clientbt = input("[>] Enter button label: ")
                clientbu = input("[>] Enter button url: ")
                while clientbt != "!q":
                    buttons.append({"label": clientbt, "url": clientbu})
                    clientbt = input("[>] Enter button label: ")
                    clientbu = input("[>] Enter button url: ")


        with open("Assets/Presence.json", "w") as f:
            presence_data = {
                "Presence": {
                    "Default" : {
                        "ClientID": clientid if custompres.lower() == "y" else "",
                        "State": clientms if custompres.lower() == "y" else "Invictus selfbot best",
                        "LargeImageKey": clientli if custompres.lower() == "y" else "",
                        "LargeImageText": clientlit if custompres.lower() == "y" else "",
                        "SmallImageKey": clientsi if custompres.lower() == "y" else "",
                        "SmallImageText": clientsit if custompres.lower() == "y" else "",
                        "Buttons" : buttons if cb.lower() == "y" else []
                    }
                }
            }
            json.dump(presence_data, f, indent=4)

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

    def eventloggerinit(self):
        if not os.path.exists("Assets/Events.json"):
            with open("Assets/Events.json", "w") as f:
                jsondata = {
                    "Guild Join"  : {"status" : False, "name" : "Guild Join", "webhooks" : []},
                    "Guild Leave" : {"status" : False, "name" : "Guild Leave", "webhooks" : []},
                    "Bans"        : {"status" : False, "name" : "Bans", "webhooks" : []},
                    "Giveaways"   : {"status" : False, "name" : "Giveaways", "webhooks" : []},
                    "Nitros"      : {"status" : False, "name" : "Nitros", "webhooks" : []}
                }
                json.dump(jsondata, f, indent=4)




    def init(self):
        self.assets()
        self.ipcache()
        self.msglogs()
        self.settings()
        self.scripts()
        self.scrapes()
        self.initalizesql()
        self.eventloggerinit()
        self.config()
