import os, json,sqlite3

class Init:
    def __init__(self):
        pass
    def assets(self):
        if not os.path.exists("Assets"):
            os.mkdir("Assets")

    def msglogs(self):
        if not os.path.exists("Assets/Logs"):
            os.mkdir("Assets/Logs")

    def config(self):
        if not os.path.exists("Assets/Config.json"):
            with open("Assets/Config.json", "w") as f:
                output_modes = ["codeblock", "embed"]
                token  = input("[>] User token     : ")
                prefix = input("[>] Command prefix : ")
                output = input("[>] Output mode    : ")
                nitro  = input("[>] Nitro sniper?  : ")
                msglog = input("[>] Log messages?  : ")
                while output not in output_modes:
                    output = input("[!] Invalid output mode. Try again: ")
                json.dump({"Token": token, "Prefix": prefix, "Output": output, "Modules": {"nitro": True if nitro.lower() == "y" else False, "msglog": True if msglog.lower() == "y" else False}}, f, indent=4)

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
        self.msglogs()
        self.initalizesql()