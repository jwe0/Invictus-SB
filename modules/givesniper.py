import json, tls_client
from modules.spoof import Spoof
from modules.logging import Logging

class GiveSniper:
    def __init__(self, token, httptoken) -> None:
        self.session = tls_client.Session()
        self.token   = token
        self.httpt   = httptoken
        self.spoof   = Spoof()
        self.logging = Logging()
        self.botjs   = {}
        self.bots    = []

    def join(self, guildid, channelid, messageid, bot):
        if self.botjs[bot]["React-Mode"]["Type"] == 1:
            emoji = self.botjs[bot]["React-Mode"]["emoji_data"]["emoji"]

            api = f"https://discord.com/api/v9/channels/{channelid}/messages/{messageid}/reactions/{emoji}/@me"
            headers = self.spoof.headers(self.token)
            r = self.session.put(api, headers=headers)
            if r.status_code == 204:
                self.logging.Info(f"Joined giveaway for {bot}")

        elif self.botjs[bot]["React-Mode"]["Type"] == 2:
            api = "https://discord.com/api/v9/interactions"
            print(self.botjs[bot]["React-Mode"]["button_data"]["component_type"])
            print(self.botjs[bot]["React-Mode"]["button_data"]["custom_id"])
            print(self.botjs[bot]["Application_ID"])
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
            print(json.dumps(data, indent=4))

            headers = self.spoof.headers(self.token)
            r = self.session.post(api, json=data, headers=headers)
            if r.status_code == 204:
                self.logging.Info(f"Joined giveaway for {bot}")


    def detect(self, message):
        if message.author.name in self.bots:
            if self.botjs[message.author.name]["Win-Data"] in message.content:
                self.logging.Info(f"Won giveaway for {message.author.name}")
            else:
                self.join(message.guild.id, message.channel.id, message.id, message.author.name)

    def init(self):
        with open("modules/Dependencies/givebots.json", "r") as f:
            bots = json.load(f)
            self.botjs = bots
            self.bots = [bot for bot in bots]
