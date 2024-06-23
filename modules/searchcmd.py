import json

cmds = json.loads(open("modules/Dependencies/cmds.json").read())

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
    
    def gettroll(self, page):
        trollcmds = []
        for command in cmds:
            if cmds.get(command).get("section") == "troll":
                if cmds.get(command).get("page") == int(page):
                    trollcmds.append(cmds.get(command))
        return trollcmds
    
    def getfun(self, page):
        funcmds = []
        for command in cmds:
            if cmds.get(command).get("section") == "fun":
                if cmds.get(command).get("page") == int(page):
                    funcmds.append(cmds.get(command))
        return funcmds
    
    def getutilities(self, page):
        utilcmds = []
        for command in cmds:
            if cmds.get(command).get("section") == "utility":
                if cmds.get(command).get("page") == int(page):
                    utilcmds.append(cmds.get(command))
        return utilcmds
    



    def get(self, command):
        info = cmds[command]
        description = info["description"]
        params = info["params"]
        example = info["example"]
        return description, params, example