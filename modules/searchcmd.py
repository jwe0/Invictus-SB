import json

cmds = json.loads(open("modules/Dependencies/cmds.json").read())

class Search:
    def __init__(self):
        pass
    def cmd(self, page, section):
        commands = []
        for command in cmds:
            if cmds.get(command).get("section") == section:
                if cmds.get(command).get("page") == int(page):
                    commands.append(cmds.get(command))
        return (commands, len(commands))

    def get(self, command):
        info = cmds[command]
        description = info["description"]
        params = info["params"]
        example = info["example"]
        return description, params, example