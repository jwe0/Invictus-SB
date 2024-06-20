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
        return token, prefix, nitro
    
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
    
    def help_format(self, array):
        max_option_length = max(len(option) for option, description in array)
        
        message = ""
        for option, description in array:
            padding = max_option_length - len(option)
            message += f"{option}{' ' * padding} {description}\n"
        
        return message
    
    
