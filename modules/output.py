import json, urllib.parse
from modules.logging import Logging

class Output:
    def __init__(self):
        self.pipes = "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"


    def output(self, title, message):
        with open("Assets/Config.json", "r") as f:
            config = json.load(f)
            mode = config.get("Output", "Text")
            if mode == "codeblock":
                return self.code_block(title, message)
            elif mode == "none":
                return Logging().Info(message)
            return mode
        
    def remove_empty_lines(self, message):
        lines = message.splitlines()
        lines[len(lines) - 1] = lines[len(lines) - 1].strip()
        return "\n".join(lines)


    
    def code_block(self, title, message):
        message = self.remove_empty_lines(message)
        msg = """
```ansi
[[2;31m>[0m]  {title}   [[2;31m<[0m]

{message}

[[2;45m[0m[2;34m~[0m] Invictus [[2;34m~[0m]
```
""".format(title=title, message=message)
        return msg
    
    def funny_line(self, message):
        linestart = "[[2;33m![0m]"
        newmessage = ""
        for line in message.splitlines():
            newmessage += f"{linestart} {line}\n"
        return newmessage
    