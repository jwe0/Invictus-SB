import time, tls_client
from modules.spoof import Spoof
from modules.logging import Logging
from modules.general import General
from modules.output import Output
from modules.events import Events

class NitroSniper:
    def __init__(self, token) -> None:
        self.token   = token
        self.logging = Logging()
        self.spoof   = Spoof()
        self.general = General()
        self.output  = Output()
        self.events  = Events(token)
        self.session = tls_client.Session()
        self.setting = {}

    def redeem(self, codeid, channel, server):
        api = f"https://discord.com/api/v9/entitlements/gift-codes/{codeid}/redeem"
        headers = self.spoof.headers(self.token)
        r = self.session.post(api, headers=headers)
        if r.status_code == 200:
            self.output.terminal("Nitro Sniper", {"Message" : "Found code", "Code" : codeid, "Channel" : channel, "Server" : server, "Status" : "Redeemed"}, False)
            self.events.hooklog({"Message" : "Found code", "Code" : codeid, "Channel" : channel, "Server" : server, "Status" : "Redeemed"}, "Nitros")
        else:
            self.output.terminal("Nitro Sniper", {"Message" : "Found code", "Code": codeid, "Channel" : channel, "Server" : server, "Status" : "Failed"}, True)
            self.events.hooklog({"Message" : "Found code", "Code": codeid, "Channel" : channel, "Server" : server, "Status" : "Failed"}, "Nitros")

    def detect(self, message):
        if "discord.gift/" in message.content:
            codeid = message.content.split("/")[-1]
            if len(codeid) >= 16:
                time.sleep(self.setting["delay"])
                if self.setting["autoredeem"]:
                    self.redeem(codeid, message.channel.name, message.guild.name)
                else:
                    self.output.terminal("Nitro Sniper", {"Message" : "Found code", "Code": codeid, "Channel" : message.channel.name, "Server" : message.guild.name, "Status" : "N/A"}, True)
                    self.events.hooklog({"Message" : "Found code", "Code": codeid, "Channel" : message.channel.name, "Server" : message.guild.name, "Status" : "N/A"}, "Nitros")
    def init(self):
        self.setting = self.general.load_nitrosniper_settings()

