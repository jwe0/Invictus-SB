import time, tls_client
from modules.spoof import Spoof
from modules.logging import Logging
from modules.general import General
from modules.output import Output
# from modules.events import Events

class NitroSniper:
    def __init__(self, token) -> None:
        self.token   = token
        self.logging = Logging()
        self.spoof   = Spoof()
        self.general = General()
        self.output  = Output()
        # self.events  = Events(token)
        self.session = tls_client.Session()
        self.setting = {}
        self.headers = {}

    def redeem(self, codeid, channel, server):
        api = f"https://discord.com/api/v9/entitlements/gift-codes/{codeid}/redeem"
        r = self.session.post(api, headers=self.headers)
        if r.status_code == 200:
            data = {"Message" : "Redeemed code", "Code" : codeid, "Channel" : channel, "Server" : server, "Status" : "Redeemed"}
            self.output.terminal("Nitro Sniper", data, False)
            return data
        else:
            data = {"Message" : "Failed to redeem code", "Code" : codeid, "Channel" : channel, "Server" : server, "Status" : "Failed"}
            self.output.terminal("Nitro Sniper", data, True)
            return data

    def detect(self, messagec, servername, cid):
        if "discord.gift/" in messagec:
            codeid = messagec.split("/")[-1]
            if len(codeid) >= 16:
                channelname = self.session.get("https://discord.com/api/v10/channels/{}".format(cid), headers=self.headers).json().get("name", "None")
                time.sleep(self.setting["delay"])
                if self.setting["autoredeem"]:
                    data = self.redeem(codeid, channelname, servername)
                    return data
                else:
                    data = {"Message" : "Found code", "Code": codeid, "Channel" : channelname, "Server" : servername, "Status" : "N/A"}
                    self.output.terminal("Nitro Sniper", data, True)
                    return data

    def init(self):
        self.setting = self.general.load_nitrosniper_settings()
        self.headers = self.spoof.headers(self.token)

