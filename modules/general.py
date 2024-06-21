import json, os
from pystyle import Colors, Colorate, Center

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
        return token, prefix, nitro, msgl
    
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
    