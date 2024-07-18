import json, datetime, urllib.parse, time
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
                message = self.array_to_message(message)
                return self.code_block(title, message)
            elif mode == "table":
                return self.mysqltable(title, message)
            elif mode == "block":
                return self.code_block_2(title, message)
            #def embed(self, title="", desc="", author="", color="", thumbnail=""):
            elif mode == "embed":
                return self.embed(title, message, "Invictus", "", "")
            elif mode == "none":
                return Logging().Info(message)
            else:
                return self.custom(title, message, mode)
            return mode
        
    def istable(self, message):
        if "»" in message:
            return True
        elif "> ```Invictus``````" in message:
            return True
        elif "+ - " in message:
            return True
        
    def remove_empty_lines(self, message):
        lines = message.splitlines()
        lines[len(lines) - 1] = lines[len(lines) - 1].strip()
        return "\n".join(lines)

    def code_block(self, title, message):
        msg = """
```ansi
[[2;31m>[0m]  {title}   [[2;31m<[0m]

{message}
[[2;45m[0m[2;34m~[0m] Invictus [[2;34m~[0m]
```""".format(title=title, message=message)
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
        
    def uptime(self):
        with open("Assets/Settings/Cache.json", "r") as f:
            uptime = json.load(f).get("Uptime", 0)
            uptime = time.strftime('%H:%M:%S', time.gmtime(uptime))
            return uptime
        
    def logons(self):
        with open("Assets/Settings/Cache.json", "r") as f:
            logons = json.load(f).get("Logons", 0)
            return logons

    def embed(self, title="", desc="", author="", color="", thumbnail=""):
        #https://invictus-sb.netlify.app/embed?title=ad&description=d&author=d&color=39bae6&thumbnail=https://i.imgur.com/TuL8lDN.jpeg
        base = "{}https://invictus-sb.netlify.app/embed".format(self.pipes)
        message = self.array_to_message(desc)
        if title:
            base += "?title=" + urllib.parse.quote(title)
        if desc:
            base += "&description=" + urllib.parse.quote(message)
        if author:
            base += "&author=" + urllib.parse.quote(author)
        if thumbnail:
            base += "&thumbnail=" + thumbnail
        if color:
            base += "&colour=" + urllib.parse.quote(color)
        base += "&url=https://invictus-sb.netlify.app"
        print(base)
        return base
    
    def cmdcount(self):
        with open("modules/Dependencies/cmds.json", "r") as f:
            return len(json.load(f))
    
    def code_block_2(self, title, array):
        msg = ""
        msg = "> ```Invictus {}``````\n".format(title)
        messgae = self.array_to_message(array)
        for line in messgae.splitlines():
            msg += "> {}\n".format(line)
        msg += "> ``````Uptime: {}```".format(self.uptime())
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

    def mysqltable(self, title, array):
        # Implement dynamic creation of mysql table format output like in help format
        # [("Column1", ["Value1", "Value2"]), ("Column2", ["Value3", "Value4"])]
        global message
        array = self.message_to_array(array, title)
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

        return self.code_block(title, message)
    
    # Add a mode for custom formatting with json and shit

    def custom(self, title, array, mode):
        with open("Assets/Settings/Style.json", 'r') as f:
            style = json.load(f)
            style = style.get(mode, "")
            if not style:
                return self.array_to_message(array, title)
            msg = self.array_to_message(
                array, 
                style.get("Header").format(title), 
                style.get("CMDStart"), 
                style.get("CMDEnd"), 
                style.get("CMDSplit"), 
                style.get("Footer"), 
                style.get("Align"), 
                style.get("ColumnStart"), 
                style.get("ColumnEnd"),
                style.get("ColumnSplit")
                )
            
            return msg

    def message_to_array(self, message, title):
        if isinstance(message, list):
            return message
        return [(title, [line.strip() for line in message.splitlines()])]

    def array_to_message(self, array, title="", msgstart="", msgend="", msgsplit="»", footer="", align=True, columnstart="", columnend="", columnsplit="»"):
        message = ""
        # Add an instance check for arrays and if not then splitlines
        if title:
            message += title + "\n" 
        if isinstance(array, list):
            padings = []
            columns = [col[0] for col in array]
            values = [val[1] for val in array]
            for col, val in zip(columns, values):
                padings.append(max(len(col), *(len(v) for v in val)))
            message += columnstart
            for i in range(len(columns)):
                if columns[i]:
                    message += columns[i].ljust(padings[i]) + " {} ".format(columnsplit) if i != len(columns) - 1 else columns[i].ljust(padings[i])
            message += columnend
            message += "\n"
            for row in range(len(values[0])):
                for col in range(len(columns)):
                    if col == 0:
                        message += f"{msgstart}{values[col][row].ljust(padings[col])}{msgend}" if align else f"{msgstart}{values[col][row]}{msgend}"
                    elif col != len(columns):
                        message += f" {msgsplit} {values[col][row].ljust(padings[col])}" if align else f" {msgsplit} {values[col][row]}"
                    else:
                        message += f"{values[col][row].ljust(padings[col])}" if align else f"{values[col][row]}"
                message += "\n"
        else:
            lines = [line.strip() for line in array.splitlines()]
            for line in lines:
                if line:
                    message += msgstart + line + msgend + "\n"
        if footer:
            message += "\n" + footer
        return message
    