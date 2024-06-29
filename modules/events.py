import json
import requests
import websocket
import time
import threading
from modules.spoof import Spoof
from modules.logging import Logging
from modules.output import Output

class Events:
    def __init__(self, token) -> None:
        self.token   = token
        self.config  = {}
        self.headers = {}
        self.spoof   = Spoof()
        self.logging = Logging()
        self.output  = Output()
        self.ws      = None
        self.dcws    = "wss://gateway.discord.gg/?v=9&encoding=json"
        self.lastack = False
        self.hbint   = 0
        self.servers = {}

    def load(self):
        with open("Assets/Events.json", "r") as f:
            self.config = json.load(f)

    def dumphooks(self, hooks, event):
        self.config[event]["webhooks"].append(hooks) 
        with open("Assets/Events.json", "w") as f:
            json.dump(self.config, f, indent=4)

    def setup(self, guildid):
        def category():
            api = "https://discord.com/api/v9/guilds/{}/channels".format(guildid)
            data = {"name": "Events", "type": 4}
            r = requests.post(api, json=data, headers=self.headers)
            return r.json().get("id")

        def create(guildid, name, parent):
            api = "https://discord.com/api/v9/guilds/{}/channels".format(guildid)
            data = {"name": name, "type": 0, "parent_id": parent}
            r = requests.post(api, json=data, headers=self.headers)
            return r.json().get("id")

        def webhook(channelid, name):
            api = "https://discord.com/api/v9/channels/{}/webhooks".format(channelid)
            data = {"name": name}
            r = requests.post(api, json=data, headers=self.headers)
            return r.json().get("url")

        parent = category()
        for event in self.config:
            if self.config[event]["status"]:
                id = create(guildid, event, parent)
                hooks = webhook(id, event)
                self.dumphooks(hooks, event)

    def wspayload(self):
        return json.dumps({
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "windows",
                    "$browser": "Discord",
                    "$device": "desktop"
                }
            }
        })

    def heartbeat(self):
        while True:
            if self.hbint:
                time.sleep(self.hbint / 1000)
                if not self.lastack:
                    self.ws.send(json.dumps({"op": 1, "d": None}))
                self.lastack = False
                self.ws.send(json.dumps({"op": 1, "d": None}))

    def on_message(self, ws, message):
        data = json.loads(message)
        if data["op"] == 10:
            self.hbint = data["d"]["heartbeat_interval"]
            threading.Thread(target=self.heartbeat).start()
            ws.send(self.wspayload())
        elif data["op"] == 11:
            self.lastack = True
        elif data['t'] == "GUILD_CREATE":
            self.servers[data.get('d').get('id')] = {"name": data.get('d').get('name')}
            if self.config.get("Guild Join").get("status"):
                name    = data.get('d').get('name')
                owner   = data.get('d').get('owner_id')
                memberc = data.get('d').get('member_count')
                vanyrle = data.get('d').get('vanity_url_code')
                premium = "None" if not data.get('d').get('premium_tier') else data.get('d').get('premium_tier')
                joinat  = data.get('d').get('joined_at')
                data = {"Name": name, "Owner": owner, "Members": memberc, "Vanity": vanyrle, "Premium": premium, "Joined": joinat}
                self.output.terminal("Guild Joined", data, True)
                self.hooklog(data, "Guild Join")
        elif data['t'] == "GUILD_DELETE":
            if self.config.get("Guild Leave").get("status"):
                type = data.get('t')
                opcode = data.get("op")
                server = data.get('d').get('id')
                sname  = self.id_to_name(server)
                data = {"Type": type, "Opcode": opcode, "Server Name": sname, "Server ID": server}
                self.output.terminal("Guild Left", data, True)
                self.hooklog(data, "Guild Leave")
        elif data['t'] == "GUILD_BAN_ADD":
            if self.config.get("Bans").get("status"):
                type   = data.get('t')
                opcode = data.get("op")
                server = data.get('d').get('guild_id')
                sname  = self.id_to_name(server)
                data = {"Type": type, "Opcode": opcode, "Server": sname, "Server ID": server}
                self.output.terminal("Ban", data, True)
                self.hooklog(data, "Bans")

    def on_error(self, ws, error):
        self.logging.Error(error)

    def on_close(self, ws):
        self.logging.Info("Connection closed")
    def on_open(self, ws):
        self.logging.Info("Opened events websocket...")

    def run(self):
        self.ws = websocket.WebSocketApp(
            self.dcws,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        self.ws.run_forever()

    def hooklog(self, dic, event):
        self.load()
        message = ""

        for key, value in dic.items():
            message += "**" + str(key) + "**" + ": " + str(value) + "\n"
        data = {
            "content" : event,
            "embeds" : [{
                "title" : event,
                "description" : "Event Triggered",
                "fields" : [
                    {
                        "name" : "Event",
                        "value" : message,
                        "inline" : False
                    }
                ]
            }]
        }

        for webhook in self.config[event]["webhooks"]:
            r = requests.post(webhook, json=data)
            if r.status_code == 401:
                self.config[event]["webhooks"].remove(webhook)
                self.redump()

    def redump(self):
        with open("Assets/Events.json", "w") as f:
            json.dump(self.config, f, indent=4)

    def get_servers(self):
        api = "https://discord.com/api/v9/users/@me/guilds"
        headers = {"Authorization": self.token}

        r = requests.get(api, headers=headers)
        for guild in r.json():
            name = guild.get("name")
            id = guild.get("id")
            self.servers[id] = {"name": name}

    def id_to_name(self, id):
        return self.servers[id]["name"]
    
    def checkhooks(self):
        self.load()
        for event in self.config:
            webhooks = self.config[event]["webhooks"]
            if not webhooks:
                self.config[event]["webhooks"] = []
                continue
            for webhook in webhooks:
                r = requests.get(webhook)
                if r.status_code == 404:
                    self.config[event]["webhooks"].remove(webhook)
                


        self.redump()
    
    def init(self):
        self.load()
        self.get_servers()
        self.headers = self.spoof.headers(self.token)
        threading.Thread(target=self.run).start()