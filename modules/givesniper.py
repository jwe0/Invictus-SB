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
        self.headers = {}
        self.bots    = []

    def join(self, guildid, channelid, messageid, bot, channelname, servername):
        time.sleep(self.setting["delay"])
        if self.botjs[bot]["React-Mode"]["Type"] == 1:
            emoji = self.botjs[bot]["React-Mode"]["emoji_data"]["emoji"]

            api = f"https://discord.com/api/v9/channels/{channelid}/messages/{messageid}/reactions/{emoji}/@me"
            r = self.session.put(api, headers=self.headers)
            if r.status_code == 204:
                data = {"Message" : "Joined giveaway", "Bot" : bot, "Channel" : channelname, "Server" : servername}
                self.output.terminal("GiveSniper", data, True)
                return data

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

            r = self.session.post(api, json=data, headers=self.headers)
            if r.status_code == 204:
                data = {"Message" : "Joined giveaway", "Bot" : bot, "Channel" : channelname, "Server" : servername}
                self.output.terminal("GiveSniper", data, True)
                return data
                

    def get_prize(self, bot, message):
        splitval = self.botjs[bot]["Prize-Split"]
        splitend = self.botjs[bot]["Split-End"]
        if not splitval:
            return "No prize specified"
        prize = message.split(splitval)[1]
        if splitend:
            prize = prize.split(splitend)[1]
        if prize:
            return prize
        return "No prize found"


    def detect(self, messagec, author, server, guildid, channelid, messageid):
        if author in self.bots:
            channel = self.session.get(f"https://discord.com/api/v9/channels/{channelid}", headers=self.headers).json().get("name", "None")
            if self.botjs[author]["Win-Data"] in messagec:
                prize = self.get_prize(author, messagec)
                data = {"Message" : "Won giveaway!", "Bot" : author, "Channel" : channel, "Server" : server, "Prize" : prize}
                self.output.terminal("GiveSniper", data, True)
                return ("won", data)
            else:
                data = self.join(guildid, channelid, messageid, author, channel, server)
                if data:
                    return ("joined", data)

    def init(self):
        with open("modules/Dependencies/givebots.json", "r") as f:
            bots = json.load(f)
            self.botjs = bots
            self.bots = [bot for bot in bots]
        self.headers = self.spoof.headers(self.token)
        self.setting = self.general.load_givesniper_settings()
