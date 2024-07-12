import json, datetime, urllib.parse
from modules.logging import Logging
from modules.colors import Colors

class Output:
    def __init__(self):
        self.pipes = "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"


    def output(self, title, message):
        with open("Assets/Config.json", "r") as f:
            config = json.load(f)
            mode = config.get("Output", "none")
            if mode == "codeblock":
                return self.code_block(title, message)
            elif mode == "codeblock2":
                return message
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
    
    def terminal(self, section, args, newline):
        message = []
        mkey = max(len(key) for key in args.keys())

        for key, value in args.items():
            message.append("[{}] |  [{}]  | {} | {}".format(datetime.datetime.now().strftime("%H:%M:%S"), f"{Colors.magenta}{section}{Colors.white}", key.ljust(mkey), value) + "\n")

        if not newline:
            message[-1] = message[-1].rstrip("\n")

        print("".join(message))

    def gettype(self):
        with open("Assets/Config.json", "r") as f:
            return json.load(f)["Type"]

    def table(self, array):
        if self.gettype() == 1:
            msg = self.mysqltable(array)
        elif self.gettype() == 2:
            msg = self.basicarrow(array)
        elif self.gettype() == 3:
            msg = self.code_block_2(array)
        else:
            msg = self.basicarrow(array)
        return msg

    def embed(self, title="", desc="", author="", color="", thumbnail=""):
        #https://invictus-sb.netlify.app/embed?title=ad&description=d&author=d&color=39bae6&thumbnail=https://i.imgur.com/TuL8lDN.jpeg
        base = "{}https://invictus-sb.netlify.app/embed".format(self.pipes)
        if title:
            base += "?title=" + urllib.parse.quote(title)
        if desc:
            base += "&description=" + urllib.parse.quote(desc)
        if author:
            base += "&author=" + urllib.parse.quote(author)
        if color:
            base += "&color=" + color
        if thumbnail:
            base += "&thumbnail=" + thumbnail
        return base
    
    def cmdcount(self):
        with open("modules/Dependencies/cmds.json", "r") as f:
            return len(json.load(f))
    
    def code_block_2(self, array):
        val_array = [val[1] for val in array if "[None]" not in val[1]]
        pad = max(len(val) for val in val_array) + 2
        msg = "> ```Invictus``````\n"
        for i in range(len(val_array[0])): 
            for j in range(len(val_array) - 1):
                msg += f"> {val_array[j][i].ljust(pad)} » {val_array[j + 1][i]}\n"
        msg += "> ``````{} commands loaded```".format(str(self.cmdcount()))
        return msg
    
    def basicarrow(self, array):
        global message
        paddings = []

        columns = [col[0] for col in array]
        values = [val[1] for val in array]
        
        message = ""

        for i in range(len(array)):
            padding1 = max(len(value) for value in values[i]) 
            padding2 = len(columns[i]) 
            paddings.append(max(padding1, padding2) + 5)
        
        for i in range(len(columns)):
            message += columns[i].ljust(paddings[i] + 2)

        message += "\n"

        for row in range(len(values[0])):
            for col in range(len(columns)):
                message += values[col][row].ljust(paddings[col] + 1) + " » " if col != len(columns) - 1 else values[col][row].ljust(paddings[col] + 1)
            message += "\n"
        return message

    def mysqltable(self, array):
        # Implement dynamic creation of mysql table format output like in help format
        # [("Column1", ["Value1", "Value2"]), ("Column2", ["Value3", "Value4"])]
        global message
        message = ""
        
        columns = [col[0] for col in array]
        values  = [val[1] for val in array]
        
        paddings = []
        for i in range(len(array)):
            padding1 = max(len(value) for value in values[i]) 
            padding2 = len(columns[i]) 
            paddings.append(max(padding1, padding2) + 2)
        
        def make_line():
            global message
            for i in range(len(paddings)):
                message += " + " + "-" * paddings[i] + "" if i != 0 else "+ " + "-" * paddings[i]
            message += " +\n"
        
        make_line()
        
        for i in range(len(columns)):
            message += "| " + columns[i].ljust(paddings[i] + 1)
        message += "|\n"
        
        make_line()
        for row in range(len(values[0])):
            for col in range(len(columns)):
                message += "| " + values[col][row].ljust(paddings[col] + 1)
            message += "|\n"
        
        make_line()

        return message