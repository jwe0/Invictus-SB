import json, time, requests, base64
from pypresence import Presence as PyPres
from modules.logging import Logging

class Presence:
    def __init__(self, token):
        self.token   = token
        self.RPC     = None
        self.cur     = ""
        self.logging = Logging()

    def pres(self, profile="Default"):
        self.cur = profile
        if self.RPC is not None:
            self.RPC.close()
        with open("Assets/Presence.json", 'r') as f:
            config = json.load(f)

            clientid = config.get("Presence").get(profile).get("ClientID")
            state    = config.get("Presence").get(profile).get("State")
            largekey = config.get("Presence").get(profile).get("LargeImageKey")
            largetxt = config.get("Presence").get(profile).get("LargeImageText")
            smallkey = config.get("Presence").get(profile).get("SmallImageKey")
            smalltxt = config.get("Presence").get(profile).get("SmallImageText")
            buttons  = config.get("Presence").get(profile).get("Buttons")


        self.RPC = PyPres(clientid)
        self.RPC.connect()
        self.RPC.update(state=state, 
                        large_image=largekey if largekey else None, 
                        large_text=largetxt if largetxt else None, 
                        small_image=smallkey if smallkey else None, 
                        small_text=smalltxt if smalltxt else None, 
                        buttons=buttons if buttons else None, 
                        start=time.time()
                        )
        


        while True:
            time.sleep(1)


    def stoppres(self):
        self.RPC.close()

    def listpres(self):
        with open("Assets/Presence.json", 'r') as f:
            pres = []
            config = json.load(f)

            for profile in config.get("Presence"):
                pres.append(profile if profile != self.cur else profile + " (Current)")

            return pres
        
    def addpres(self, name, id, state="", largeimagekey="", largeimagetext="", smallimagekey="", smallimagetext=""):
        with open("Assets/Presence.json", "r") as f:
            data = json.load(f)

        with open("Assets/Presence.json", "w") as f:
            data["Presence"][name] = {"ClientID": id, "State": state, "LargeImageKey": largeimagekey, "LargeImageText": largeimagetext, "SmallImageKey": smallimagekey, "SmallImageText": smallimagetext, "Buttons": []}
            json.dump(data, f, indent=4)

        
    def altadd(self, name, state, largeimagekeypath="", largeimagetext="", smallimagekeypath="", smallimagetext=""):
        id = self.createapp(name)
        if largeimagekeypath is not None:
            lkeyname = self.addasset(id, largeimagekeypath)
        if smallimagekeypath is not None:
            skeyname = self.addasset(id, smallimagekeypath)
        self.addpres(name, id, state, lkeyname if largeimagekeypath else None, largeimagetext, skeyname if smallimagekeypath else None, smallimagetext)

    def createapp(self, name):
        createapi = "https://discord.com/api/v9/applications"
        data      = {"name" : name}
        headers = {"authorization" : self.token}
        r = requests.post(createapi, json=data, headers=headers)
        if r.status_code == 429:
            self.logging.error("Waiting {}s to create app because of rate limit".format(r.json().get("retry_after")))
            time.sleep(r.json()["retry_after"] + 5)
        return r.json().get("id")
    
    def img_to_b64(self, img):
        with open(img, "rb") as f:
            return base64.b64encode(f.read()).decode()
    
    def addasset(self, id, path):
        print(id, path)
        assetsapi = "https://discord.com/api/v9/oauth2/applications/{}/assets".format(id)
        data = {"name" : path.split(".")[0].replace("/", ""), "image":"data:image/png;base64,{}".format(self.img_to_b64(path)), "type": 2}
        headers = {"authorization" : self.token}
        r = requests.post(assetsapi, json=data, headers=headers)
        if r.status_code == 429:
            self.logging.error("Waiting {}s to add asset because of rate limit".format(r.json().get("retry_after")))
            time.sleep(r.json()["retry_after"] + 5)
        print(r.status_code, r.text)
        return r.json().get("name")

