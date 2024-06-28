import json, tls_client, time
from modules.spoof import Spoof
from modules.logging import Logging
from modules.general import General
from modules.output import Output

class GiveSniper:
    def __init__(self, token, httptoken) -> None:
        self.session = tls_client.Session()
        self.token   = token
        self.httpt   = httptoken
        self.spoof   = Spoof()
        self.logging = Logging()
        self.general = General()
        self.output  = Output()
        self.setting = {}
        self.botjs   = {}
        self.bots    = []

    def join(self, guildid, channelid, messageid, bot, channelname, servername):
        time.sleep(self.setting["delay"])
        if self.botjs[bot]["React-Mode"]["Type"] == 1:
            emoji = self.botjs[bot]["React-Mode"]["emoji_data"]["emoji"]

            api = f"https://discord.com/api/v9/channels/{channelid}/messages/{messageid}/reactions/{emoji}/@me"
            headers = self.spoof.headers(self.token)
            r = self.session.put(api, headers=headers)
            if r.status_code == 204:
                self.output.terminal("GiveSniper", {"Message" : "Joined giveaway", "Bot" : bot, "Channel" : channelname, "Server" : servername}, True)

        elif self.botjs[bot]["React-Mode"]["Type"] == 2:
            api = "https://discord.com/api/v9/interactions"
            data = {
                "type" : 3,
                "guild_id" : guildid,
                "channel_id" : channelid,
                "message_id" : messageid,
                "application_id" : self.botjs[bot]["Application_ID"],
                "session_id" : self.httpt,
                "data" : {
                    "component_type" : self.botjs[bot]["React-Mode"]["button_data"]["component_type"],
                    "custom_id" : self.botjs[bot]["React-Mode"]["button_data"]["custom_id"]
                },
            }

            headers = self.spoof.headers(self.token)
            r = self.session.post(api, json=data, headers=headers)
            if r.status_code == 204:
                self.output.terminal("GiveSniper", {"Message" : "Joined giveaway", "Bot" : bot, "Channel" : channelname, "Server" : servername}, True)
                


    def detect(self, message):
        if message.author.name in self.bots:
            if self.botjs[message.author.name]["Win-Data"] in message.content:
                self.output.terminal("GiveSniper", {"Message" : "Won giveaway!", "Bot" : message.author.name, "Channel" : message.channel.name, "Server" : message.guild.name}, True)
            else:
                self.join(message.guild.id, message.channel.id, message.id, message.author.name, message.channel.name, message.guild.name)

    def init(self):
        with open("modules/Dependencies/givebots.json", "r") as f:
            bots = json.load(f)
            self.botjs = bots
            self.bots = [bot for bot in bots]
        self.setting = self.general.load_givesniper_settings()
