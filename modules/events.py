import json
import requests
import websocket
import time
import threading
from modules.spoof import Spoof
from modules.logging import Logging
from modules.output import Output
from modules.givesniper import GiveSniper
from modules.nitrosn import NitroSniper

class Events:
    def __init__(self, token, httptoken) -> None:
        self.token     = token
        self.httptoken = httptoken
        self.config    = {}
        self.events    = {}
        self.headers   = {}
        self.spoof     = Spoof()
        self.logging   = Logging()
        self.output    = Output()
        self.ws        = None
        self.dcws      = "wss://gateway.discord.gg/?v=9&encoding=json"
        self.lastack   = False
        self.hbint     = 0
        self.servers   = {}
        self.hookstyle = {}
        self.nitro     = False
        self.givsnipe  = False
        self.nitrosn   = None
        self.givesn    = None

    def load(self):
        with open("Assets/Events.json", "r") as f:
            self.events = json.load(f)

    def style(self):
        with open("Assets/Settings/webhook.json", "r") as f:
            self.hookstyle = json.load(f)

    def dumphooks(self, hooks, event):
        self.events[event]["webhooks"].append(hooks) 
        with open("Assets/Events.json", "w") as f:
            json.dump(self.events, f, indent=4)

    def setup(self, guildid):
        def category():
            api = "https://discord.com/api/v9/guilds/{}/channels".format(guildid)
            data = {"name": "Events", "type": 4}
            r = requests.post(api, json=data, headers=self.headers)
            while r.status_code == 429:
                self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                time.sleep(r.json()["retry_after"] + 5)
                r = requests.post(api, json=data, headers=self.headers)
            return r.json().get("id")

        def create(guildid, name, parent):
            api = "https://discord.com/api/v9/guilds/{}/channels".format(guildid)
            data = {"name": name, "type": 0, "parent_id": parent}
            r = requests.post(api, json=data, headers=self.headers)
            while r.status_code == 429:
                self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                time.sleep(r.json()["retry_after"] + 5)
                r = requests.post(api, json=data, headers=self.headers)
            return r.json().get("id")

        def webhook(channelid, name):
            api = "https://discord.com/api/v9/channels/{}/webhooks".format(channelid)
            data = {"name": name}
            r = requests.post(api, json=data, headers=self.headers)
            while r.status_code == 429:
                self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                time.sleep(r.json()["retry_after"] + 5)
                r = requests.post(api, json=data, headers=self.headers)
            return r.json().get("url")

        parent = category()
        for event in self.events:
            if self.events[event]["status"]:
                id = create(guildid, event, parent)
                hooks = webhook(id, event)
                self.dumphooks(hooks, event)
                time.sleep(1)

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
        try:
            while True:
                if self.hbint:
                    time.sleep(self.hbint / 1000)
                    if not self.lastack:
                        self.logging.Info("Heartbeat not acknowledged reauthenticating...")
                        self.ws.send(self.wspayload())
                    self.lastack = False
                    self.ws.send(json.dumps({"op": 1, "d": None}))
        except Exception as e:
            self.logging.Error(e)
            threading.Thread(target=self.run).start()

    def on_message(self, ws, message):
        if message:
            data = json.loads(message)
            if data["op"] == 10:
                self.hbint = data["d"]["heartbeat_interval"]
                threading.Thread(target=self.heartbeat).start()
                ws.send(self.wspayload())
            elif data["op"] == 11:
                self.lastack = True
            elif data['t'] == "GUILD_CREATE":
                self.servers[data.get('d').get('id')] = {"name": data.get('d').get('name')}
                if self.events.get("Guild Join").get("status"):
                    type    = data.get('t')
                    name    = data.get('d').get('name')
                    owner   = data.get('d').get('owner_id')
                    memberc = data.get('d').get('member_count')
                    vanyrle = data.get('d').get('vanity_url_code')
                    premium = "None" if not data.get('d').get('premium_tier') else data.get('d').get('premium_tier')
                    joinat  = data.get('d').get('joined_at')
                    data = {"Type": type, "Name": name, "Owner": owner, "Members": memberc, "Vanity": vanyrle, "Premium": premium, "Joined": joinat}
                    self.output.terminal("Guild Joined", data, True)
                    self.hooklog(data, "Guild Join")
            elif data['t'] == "GUILD_DELETE":
                if self.events.get("Guild Leave").get("status"):
                    type = data.get('t')
                    opcode = data.get("op")
                    server = data.get('d').get('id')
                    sname  = self.id_to_name(server)
                    data = {"Type": type, "Opcode": opcode, "Server Name": sname, "Server ID": server}
                    self.output.terminal("Guild Left", data, True)
                    self.hooklog(data, "Guild Leave")
            elif data['t'] == "GUILD_BAN_ADD":
                if self.events.get("Bans").get("status"):
                    type   = data.get('t')
                    opcode = data.get("op")
                    server = data.get('d').get('guild_id')
                    sname  = self.id_to_name(server)
                    data = {"Type": type, "Opcode": opcode, "Server": sname, "Server ID": server}
                    self.output.terminal("Ban", data, True)
                    self.hooklog(data, "Bans")
            elif data['t'] == "RELATIONSHIP_ADD":
                if self.events.get("Friends").get("status"):
                    type2    = data.get("d").get("type")
                    if str(type2) == "3":
                        type     = data.get('t')
                        opcode   = data.get("op")
                        username = data.get("d").get("user").get("username")
                        userid   = data.get("d").get("user").get("id")
                        globname = data.get("d").get("user").get("global_name")
                        data = {"Type": type, "Opcode": opcode, "Code": type2, "Username": username, "User ID": userid, "Global Name": globname}
                        self.output.terminal("New Friend", data, True)
                        self.hooklog(data, "Friends")
            elif data['t'] == "MESSAGE_CREATE":
                if self.nitro:
                    content, guildid, guild, chanlid, author, msgid = self.getdata(data)
                    result = self.nitrosn.detect(content, guild, chanlid)
                    if result:
                        self.hooklog(result, "Nitros")
                if self.givesn:
                    content, guildid, guild, chanlid, author, msgid = self.getdata(data)
                    result = self.givesn.detect(content, author, guild, guildid, chanlid, msgid)
                    status = result[0]
                    data   = result[1]
                    if status:
                        self.hooklog(data, "Giveaways", status)
            

    def getdata(self, data):
        content = data.get('d').get('content', "None") #
        guildid = data.get('d').get('guild_id', "None") # 
        guild   = self.id_to_name(guildid) # 
        chanlid = data.get('d').get('channel_id', "None") #
        author  = data.get('d').get('author').get('username', "None") #
        msgid   = data.get('d').get('id', "None") #

        return content, guildid, guild, chanlid, author, msgid

    def on_error(self, ws, error):
        if error:
            self.logging.Error("WS Error: {}".format(error))
        else:
            self.logging.Error("WS Error: Unknown")

    def on_close(self, ws):
        self.logging.Info("Connection closed")
    def on_open(self, ws):
        self.logging.Info("Opened events websocket...")

    def run(self):
        self.ws = websocket.WebSocketApp(
            self.dcws,
            on_message=self.on_message,
            on_close=self.on_close,
            on_open=self.on_open
        )
        self.ws.run_forever()

    def hooklog(self, dic, event, trigger=""):
        self.load()
        self.style()
        message = "```\n"
        keys = list(dic.keys())
        mkey = max(len(k) for k in keys)

        for key, value in dic.items():
            message += key.ljust(mkey) + "  :  " + str(value) + "\n"

        message += "```"
        data = {
            "embeds" : [{
                "title" : event,
                "author" : {
                    "name" : self.hookstyle.get("Author")
                },
                "color" : self.hookstyle["Color"],
                "description" : "Event Triggered: {}".format(trigger) if trigger else "Event Triggered",
                "fields" : [
                    {
                        "name" : "Event",
                        "value" : message,
                        "inline" : False
                    }
                ]
            }]
        }

        for webhook in self.events[event]["webhooks"]:
            r = requests.post(webhook, json=data)
            if r.status_code == 401:
                self.events[event]["webhooks"].remove(webhook)
                self.redump()

    def redump(self):
        with open("Assets/Events.json", "w") as f:
            json.dump(self.events, f, indent=4)

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
        for event in self.events:
            webhooks = self.events[event]["webhooks"]
            if not webhooks:
                self.events[event]["webhooks"] = []
                continue
            for webhook in webhooks:
                r = requests.get(webhook)
                while r.status_code == 429:
                    self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                    time.sleep(r.json()["retry_after"] + 5)
                    r = requests.get(webhook)
                if r.status_code == 404 or r.status_code != 200:
                    self.logging.Error("Webhook {} not found".format(webhook))
                    self.events[event]["webhooks"].remove(webhook)
                time.sleep(1)
        self.redump()

    def loadmodules(self):
        with open("Assets/Config.json", "r") as f:
            self.config = json.load(f)
            self.nitro    = self.config.get("Modules").get("nitro", False)
            if self.nitro:
                self.logging.Info("Setting up nitro sniper...")
                self.nitrosn = NitroSniper(self.token)
                self.nitrosn.init()
            self.givsnipe = self.config.get("Modules").get("givesniper", False)    
            if self.givsnipe:
                self.logging.Info("Setting up give sniper...")
                self.givesn = GiveSniper(self.token, self.httptoken)
                self.givesn.init()  

    def connect(self):
        threading.Thread(target=self.run).start()

    def init(self):
        self.load()
        self.get_servers()
        self.loadmodules()
        self.headers = self.spoof.headers(self.token)
        self.connect()