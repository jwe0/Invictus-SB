import json

cmds = json.loads(open("modules/Dependencies/cmds.json").read())

class Search:
    def __init__(self):
        pass
    def cmd(self, page, section):
        commands = []
        pages = []
        for command in cmds:
            if cmds.get(command).get("section") == section:
                if cmds.get(command).get("page") == int(page):
                    commands.append(cmds.get(command))
                if cmds.get(command).get("page") not in pages:
                    pages.append(cmds.get(command).get("page"))

        return (commands, len(commands), max(pages))

    def get(self, command):
        info = cmds[command]
        description = info["description"]
        params = info["params"]
        example = info["example"]
        return description, params, example