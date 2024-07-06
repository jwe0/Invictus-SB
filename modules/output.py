import json, datetime
from modules.logging import Logging
from modules.colors import Colors

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
    
    def terminal(self, section, args, newline):
        message = []
        mkey = max(len(key) for key in args.keys())

        for key, value in args.items():
            message.append("[{}] |  [{}]  | {} | {}".format(datetime.datetime.now().strftime("%H:%M:%S"), f"{Colors.magenta}{section}{Colors.white}", key.ljust(mkey), value) + "\n")

        if not newline:
            message[-1] = message[-1].rstrip("\n")

        print("".join(message))

    def join_side_by_side(self, *args):
        split_args = [arg.splitlines() for arg in args]
        max_lines = max(len(lines) for lines in split_args)
        padded_args = [lines + [''] * (max_lines - len(lines)) for lines in split_args]

        combined_lines = []
        for lines in zip(*padded_args):
            combined_line = ""
            for i, line in enumerate(lines):
                if i == 0:
                    combined_line += line[:-1]
                else:
                    combined_line += line[1:]
            combined_lines.append(combined_line)

        return '\n'.join(combined_lines)

    def mysqltable(self, args):
        # Implement dynamic creation of mysql table format output like in help format
        # [("Column1", ["Value1", "Value2"]), ("Column2", ["Value3", "Value4"])]
        message = []
        for arg in args:
            submsg = ""
            column = arg[0]
            values = arg[1]
            padding = max(len(value) for value in values) + 2
            submsg += "+ " + "-" * padding    + " + \n"
            submsg += "| " + column.ljust(padding) + " | \n"
            submsg += "+ " + "-" * padding    + " + \n"
            for value in values:
                submsg += "| " + value.ljust(padding) + " | \n"
            submsg += "+ " + "-" * padding    + " + \n"
            message.append(submsg)
        return self.join_side_by_side(*message)
