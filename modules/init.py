import os, json

class Init:
    def __init__(self):
        pass
    def assets(self):
        if not os.path.exists("Assets"):
            os.mkdir("Assets")

    def config(self):
        if not os.path.exists("Assets/Config.json"):
            with open("Assets/Config.json", "w") as f:
                output_modes = ["codeblock", "embed"]
                token  = input("[>] User token     : ")
                prefix = input("[>] Command prefix : ")
                output = input("[>] Output mode    : ")
                nitro  = input("[>] Nitro sniper?  : ")
                while output not in output_modes:
                    output = input("[!] Invalid output mode. Try again: ")
                json.dump({"Token": token, "Prefix": prefix, "Output": output, "Modules": {"nitro": True if nitro.lower() == "y" else False}}, f, indent=4)


    def init(self):
        self.assets()
        self.config()