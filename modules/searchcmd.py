import json

cmds = json.loads(open("modules/cmds.json").read())

class Search:
    def __init__(self):
        pass

    def getraid(self, page):
        raidcmds = []
        for command in cmds:
            if cmds.get(command).get("section") == "raid":
                if cmds.get(command).get("page") == int(page):
                    raidcmds.append(cmds.get(command))
        return raidcmds


    def get(self, command):
        info = cmds[command]
        description = info["description"]
        params = info["params"]
        example = info["example"]
        return description, params, example