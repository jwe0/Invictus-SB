import discord, requests, socket, threading, phonenumbers, time, subprocess, websocket, json, random, tls_client, os, socket, base64
from phonenumbers import carrier
from pystyle import Center
from phonenumbers import geocoder
from bs4 import BeautifulSoup
from discord.ext import commands
from modules.colors import Colors
from modules.general import General
from modules.logging import Logging
from modules.init import Init
from modules.output import Output
from modules.database import Database
from modules.searchcmd import Search
from modules.spoof import Spoof
from modules.antitokenlog import AntiTokenLog
from modules.mreact import MassReact
from modules.presence import Presence
from modules.events import Events
from modules.cryptography import Crypto

class Bot:
    def __init__(self):
        # Loading other classes into this class
        self.general  = General()
        self.logging  = Logging()
        self.output   = Output().output
        self.output2  = Output()
        self.database = Database()
        self.search   = Search()
        self.spoof    = Spoof()
        self.crypto   = Crypto()
        self.events   = None
        self.presence = None
        self.massr    = None
        self.anti     = None
        self.givesn   = None
        self.nitrosn  = None


        # Discord.py things
        self.bot    = None
        self.prefix = ""
        self.token  = ""

        # Modules
        self.nitro    = False
        self.messagel = False
        self.give     = False
        self.session  = tls_client.Session()


        # Storing values
        self.lastcommand = ""
        self.cmds        = json.loads(open("modules/Dependencies/cmds.json").read())
        self.sessionheaders = ""
        self.nitrosettings  = {}
        self.givesettings   = {}
        self.scripts        = []

        # Api keys
        self.gelkey = ""
        self.userid = ""
        


    def initalize(self):
        @self.bot.event
        async def on_ready():
            self.logging.Info("Starting event logger...")
            self.events = Events(self.token, self.bot.http.token)
            self.events.init()
            self.general.clear()
            self.general.art()
            print(Center.XCenter(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})\n"))

        @self.bot.event
        async def on_command(ctx):
            self.lastcommand = ctx.message.content + "\n"

        @self.bot.event
        async def on_command_error(ctx, error):
            self.logging.Error(str(error))

        @self.bot.event
        async def on_message(message):
            await self.bot.process_commands(message)
            if self.messagel:
                self.database.messageloggeradd(message.author.id, message.author.name, self.general.removespecial(message.content), message.created_at.strftime("%Y-%m-%d - %H:%M:%S"))

        @self.bot.event
        async def on_message_delete(message):
            if self.messagel:
                self.database.deletedloggeradd(message.author.id, message.author.name,self.general.removespecial(message.content), message.created_at.strftime("%Y-%m-%d - %H:%M:%S"))
                


        @self.bot.command()
        async def help(ctx):
            await ctx.message.delete()
            options = [
                {"name": "raid", "description": "Commands for raiding", "params": [], "section": "raid", "page": 1},
                {"name": "troll", "description": "Commands for trolling", "params": [], "section": "troll", "page": 1},
                {"name": "fun", "description": "Commands for fun", "params": [], "section": "fun", "page": 1},
                {"name": "utilities", "description": "Commands for utility", "params": [], "section": "utilities", "page": 1},
                {"name": "nsfw", "description": "Commands for NSFW", "params": [], "section": "nsfw", "page": 1},
                {"name": "crypto", "description": "Commands for cryptography", "params": [], "section": "crypto", "page": 1},
            ]

            message = self.general.help_format(options)
            await ctx.send(self.output("Help", message))

        @self.bot.command()
        async def raid(ctx, page=1):
            await ctx.message.delete()
            cmds = self.search.cmd(page, "raid")
            await ctx.send(self._help("Raid", cmds, page))

        @self.bot.command()
        async def troll(ctx, page=1):
            await ctx.message.delete()
            cmds = self.search.cmd(page, "troll")
            await ctx.send(self._help("Troll", cmds, page))

        @self.bot.command()
        async def fun(ctx, page=1):
            await ctx.message.delete()
            cmds = self.search.cmd(page, "fun")
            await ctx.send(self._help("Fun", cmds, page))

        @self.bot.command()
        async def utilities(ctx, page=1):
            await ctx.message.delete()
            cmds = self.search.cmd(page, "utility")
            await ctx.send(self._help("Utilities", cmds, page))

        @self.bot.command()
        async def nsfw(ctx, page=1):
            await ctx.message.delete()
            cmds = self.search.cmd(page, "nsfw")
            await ctx.send(self._help("NSFW", cmds, page))

        @self.bot.command()
        async def crypto(ctx, page=1):
            await ctx.message.delete()
            cmds = self.search.cmd(page, "crypto")
            await ctx.send(self._help("Crypto", cmds, page))

        # Raid commands
        @self.bot.command()
        async def messagespam(ctx, message="INVICTUS ON TOP", count=50, delay=2, thread="n", randstr="y"):
            await ctx.message.delete()
            WAIT = [False, 0]
            api = "https://discord.com/api/v9/channels/{}/messages".format(ctx.channel.id)
            headers = {"authorization": self.token}

            def send():
                data = {"content": message if randstr == "n" else message + " - [" + self.general.randomnstring(16) + "]"}
                r = requests.post(api, json=data, headers=headers)
                if r.status_code == 429:
                    self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                    WAIT[0] = True
                    WAIT[1] = r.json()["retry_after"]

            for i in range(int(count)):
                if WAIT[0]:
                    time.sleep(WAIT[1])
                    WAIT[0] = False
                if thread == "n":
                    send()
                else:
                    threading.Thread(target=send).start()
                time.sleep(delay)

        @self.bot.command()
        async def pinspam(ctx, count=50, delay=2, thread="n"):
            await ctx.message.delete()
            WAIT = [False, 0]
            api = "https://discord.com/api/v9/channels/{}/pins/{}"

            def send():
                r = requests.put(api.format(ctx.channel.id, message.id), headers={"authorization": self.token})
                if r.status_code == 429:
                    self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                    WAIT[0] = True
                    WAIT[1] = r.json()["retry_after"]

            for message in await ctx.channel.history(limit=count).flatten():
                if WAIT[0]:
                    time.sleep(WAIT[1])
                    WAIT[0] = False
                if thread == "n":
                    send()
                else:
                    threading.Thread(target=send).start()
                time.sleep(delay)

        @self.bot.command()
        async def threadspam(ctx, message="INVICTUS ON TOP", count=50, delay=2, thread="n"):
            await ctx.message.delete()
            WAIT = [False, 0]
            api = "https://discord.com/api/v9/channels/{}/threads".format(ctx.channel.id)

            def send():
                r = requests.post(api, json={"name": message}, headers={"authorization": self.token})
                if r.status_code == 429:
                    self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                    WAIT[0] = True
                    WAIT[1] = r.json()["retry_after"]

            for i in range(int(count)):
                if WAIT[0]:
                    time.sleep(WAIT[1])
                    WAIT[0] = False
                if thread == "n":
                    send()
                else:
                    threading.Thread(target=send).start()
                time.sleep(int(delay))

        @self.bot.command()
        async def createchannels(ctx, name="INVICTUS ON TOP", count=50, delay=2, thread="n"):
            await ctx.message.delete()
            WAIT = [False, 0]
            api = "https://discord.com/api/v9/guilds/{}/channels".format(ctx.guild.id)
            data = {"name": name, "type": 0}
            headers = {"authorization": self.token}

            def send():
                r = requests.post(api, json=data, headers=headers)
                if r.status_code == 429:
                    self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                    WAIT[0] = True
                    WAIT[1] = r.json()["retry_after"]

            for i in range(int(count)):
                if WAIT[0]:
                    time.sleep(WAIT[1])
                    WAIT[0] = False
                if thread == "n":
                    send()
                else:
                    threading.Thread(target=send).start()
                time.sleep(int(delay))
        @self.bot.command()
        async def createroles(ctx, name="INVICTUS ON TOP", count=50, delay=2, thread="n"):
            await ctx.message.delete()
            WAIT = [False, 0]
            api = "https://discord.com/api/v9/guilds/{}/roles".format(ctx.guild.id)
            data = {"name": name}
            headers = {"authorization": self.token}

            def send():
                r = requests.post(api, json=data, headers=headers)
                if r.status_code == 429:
                    self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                    WAIT[0] = True
                    WAIT[1] = r.json()["retry_after"]

            for i in range(int(count)):
                if WAIT[0]:
                    time.sleep(WAIT[1])
                    WAIT[0] = False
                if thread == "n":
                    send()
                else:
                    threading.Thread(target=send).start()
                time.sleep(int(delay))
        @self.bot.command()
        async def deletechannels(ctx, delay=2, thread="n"):
            await ctx.message.delete()
            WAIT = [False, 0]

            def send(id):
                api = "https://discord.com/api/v9/channels/{}".format(id)
                r = requests.delete(api, headers={"authorization": self.token})
                if r.status_code == 429:
                    self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                    WAIT[0] = True
                    WAIT[1] = r.json()["retry_after"]

            for channel in ctx.guild.channels:
                if WAIT[0]:
                    time.sleep(WAIT[1])
                    WAIT[0] = False
                if thread == "n":
                    send(channel.id)
                else:
                    threading.Thread(target=send, args=(channel.id,)).start()
                time.sleep(int(delay))

        @self.bot.command()
        async def deleteroles(ctx, delay=2, thread="n"):
            await ctx.message.delete()
            WAIT = [False, 0]

            def send(id):
                api = "https://discord.com/api/v9/guilds/{}/roles/{}".format(ctx.guild.id, id)
                r = requests.delete(api, headers={"authorization": self.token})
                if r.status_code == 429:
                    self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                    WAIT[0] = True
                    WAIT[1] = r.json()["retry_after"]

            for role in ctx.guild.roles:
                if WAIT[0]:
                    time.sleep(WAIT[1])
                    WAIT[0] = False
                if thread == "n":
                    send(role.id)
                else:
                    threading.Thread(target=send, args=(role.id,)).start()
                time.sleep(int(delay))

            
        @self.bot.command()
        async def massping(ctx, loops=5, delay=1, perline=3, mode=1):
            await ctx.message.delete()
            def Get_Members(id):
                headers = {"Authorization": self.token}
                api     = "https://discord.com/api/v9/channels/{}/messages?limit=100".format(id)
                response = requests.get(api, headers=headers)
                if response.status_code != 200:
                    return []
                response = response.json()
                members  = []

                for member in response:
                    if member["author"]["id"] not in members:
                        members.append(member["author"]["id"])

                return members
            if mode == 1:
                members = Get_Members(ctx.channel.id)
            else:
                members = []
                for channel in ctx.guild.channels:
                    for member in Get_Members(channel.id):
                        if member not in members:
                            members.append(member)
            for _ in range(loops):
                message = []
                for member in members:
                    message.append(f"<@{member}>")
                    if len(message) == perline:
                        await ctx.send("😘 " + " ".join(message) + " - [" + self.general.randomnstring(16) + "]")
                        message = []
                if message:
                    await ctx.send("😘 " + " ".join(message) + " - [" + self.general.randomnstring(16) + "]")
                    message = []
                time.sleep(delay)

        @self.bot.command()
        async def webraid(ctx, channelname="raided-by-invictus", message="@everyone RAIDED BY INVICTUS", channelamount=20, messageamount=30):
            await ctx.message.delete()
            def webhook(hook):
                avatar = "https://cdn.discordapp.com/avatars/{}/{}.png".format(ctx.author.id, ctx.author.avatar)
                for i in range(int(messageamount)):
                    data = {"content" : message, "avatar_url" : avatar}
                    r = requests.post(hook, json=data)
                    if r.status_code != 204:
                        r = requests.post(hook, json=data)
                        if r.status_code == 429:
                            self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                            time.sleep(r.json()["retry_after"] + 1)
            def removechannel(id):
                headers = {"authorization": self.token}
                api = "https://discord.com/api/v9/channels/{}".format(id)
                requests.delete(api, headers=headers)
            def createchannel():
                headers = {"authorization": self.token}
                channelapi = "https://discord.com/api/v9/guilds/{}/channels".format(ctx.guild.id)
                data = {"name": channelname, "type": 0}
                r = requests.post(channelapi, headers=headers, json=data)
                while r.status_code != 201:
                    r = requests.post(channelapi, headers=headers, json=data)
                    if r.status_code == 429:
                        self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                        time.sleep(r.json()["retry_after"] + 1)
                chanid = r.json()["id"]

                webhookapi = "https://discord.com/api/v9/channels/{}/webhooks".format(chanid)
                data = {"name": ctx.author.name}
                r = requests.post(webhookapi, headers=headers, json=data)
                while r.status_code != 200:
                    r = requests.post(webhookapi, headers=headers, json=data)
                    if r.status_code == 429:
                        self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                        time.sleep(r.json()["retry_after"] + 1)

                
                threading.Thread(target=webhook, args=(r.json()["url"],)).start()

            for channel in ctx.guild.channels:
                threading.Thread(target=removechannel, args=(channel.id,)).start()

            for i in range(int(channelamount)):
                createchannel()

        @self.bot.command()
        async def gcspam(ctx, target, name="invictus > all", count=10, delay=2):
            await ctx.message.delete()
            def create(id):
                api = "https://discord.com/api/v10/users/@me/channels"
                data = {"recipients":[f"{self.bot.user.id}", f"{id}"]}
                r = requests.post(api, headers={"authorization": self.token}, json=data)
                print("[CREATE] " + str(r.status_code))
                while r.status_code != 200:
                    r = requests.post(api, headers={"authorization": self.token}, json=data)
                    if r.status_code == 429:
                        self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                        time.sleep(r.json()["retry_after"] + 1)
                id = r.json()["id"]

                rename(id)
            def rename(id):
                api = "https://discord.com/api/v9/channels/{}".format(id)
                data = {"name": name}
                r = requests.patch(api, headers={"authorization": self.token}, json=data)
                print("[RENAME] " + str(r.status_code))
                while r.status_code != 200:
                    r = requests.patch(api, headers={"authorization": self.token}, json=data)
                    if r.status_code == 429:
                        self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                        time.sleep(r.json()["retry_after"] + 1)
                leave(id)

            def leave(id):
                api = "https://discord.com/api/v9/channels/{}?silent=true".format(id)
                r = requests.delete(api, headers={"authorization": self.token})
                print("[LEAVE] " + str(r.status_code))
                while r.status_code != 200:
                    r = requests.delete(api, headers={"authorization": self.token})
                    if r.status_code == 429:
                        self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                        time.sleep(r.json()["retry_after"] + 1)

            for i in range(int(count)):
                create(target)
                time.sleep(int(delay))

        @self.bot.command()
        async def callspam(ctx, target, count=10, delay=2):
            await ctx.message.delete()
            def apiinit():
                api = "https://discord.com/api/v9/channels/{}/call/ring".format(target)
                headers = {"authorization": self.token}
                r = requests.post(api, headers=headers)
            def wsinit():
                ws = websocket.WebSocket()
                ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
                ws.send(json.dumps({"op": 2, "d": {"token": self.token, "properties": {"$os": "windows", "$browser": "Discord", "$device": "desktop"}}}))
                ws.send(json.dumps({"op": 4, "d": {"guild_id": None, "channel_id": ctx.channel.id, "self_mute": False, "self_deaf": False}}))
                ws.close()

            for i in range(int(count)):
                apiinit()
                wsinit()
                time.sleep(int(delay))



        # Troll commands

        @self.bot.command()
        async def vcspam(ctx, channel, count=10, delay=2):
            await ctx.message.delete()
            def join():
                ws = websocket.WebSocket()
                ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
                ws.send(json.dumps({"op": 2, "d": {"token": self.token, "properties": {"$os": "windows", "$browser": "Discord", "$device": "desktop"}}}))
                ws.send(json.dumps({"op": 4, "d": {"guild_id": ctx.guild.id, "channel_id": channel, "self_mute": False, "self_deaf": False}}))
                ws.close()

            for i in range(int(count)):
                join()
                time.sleep(int(delay))
        @self.bot.command()
        async def ippuller(ctx, id):
            await ctx.message.delete()
            def lookup(ip):
                url = "http://ip-api.com/json/{}".format(ip)
                r = requests.get(url)
                if r.status_code == 200:
                    data = r.json()
                    country = data["country"]
                    city    = data["city"]
                    zip     = data["zip"]
                    isp     = data["isp"]
                    lat     = data["lat"]
                    lon     = data["lon"]

                    loc = "{}, {}, {}, {}, {} : {}".format(country, city, zip, isp, lat, lon)

                    return loc


            cache = json.loads(open("Assets/IPcache.json", "r").read())
            if str(id) in cache:
                ip = cache[str(id)]["ip"]
                loc = cache[str(id)]["location"]
                await ctx.send("<@{}> ".format(id) + ip + " " + loc + " 😎")
            else:
                ip = ".".join(str(random.randint(1, 255)) for i in range(4))
                loc = lookup(ip)
                cache[id] = {"ip": ip, "location": loc}
                open("Assets/IPcache.json", "w").write(json.dumps(cache))

                await ctx.send("<@{}> ".format(id) + ip + " " + loc + " 😎")

        # Fun commands  

        @self.bot.command()
        async def gayrate(ctx, user: discord.User = None):
            await ctx.message.delete()
            percent = random.randint(0, 100)
            message = self.output("Gayrate", f"{user.name} is {str(percent)}% gay\n")

            await ctx.send(message)

        @self.bot.command()
        async def ghostspam(ctx, user: discord.User = None, count=10, delay=2):
            await ctx.message.delete()
            mention = user.mention

            for i in range(int(count)):
                message = await ctx.send(mention)
                await message.delete()
                time.sleep(int(delay))

        @self.bot.command()
        async def massreact(ctx, messageid, channelid, delay=2):
            await ctx.message.delete()
            self.massr.react(messageid, channelid, delay)

        
        # Utility commands

        @self.bot.command()
        async def iplookup(ctx, ip):
            await ctx.message.delete()
            url = "http://ip-api.com/json/{}".format(ip)
            r = requests.get(url)
            message = ""
            for key, value in r.json().items():
                message += "{}: {}\n".format(key.title(), value)
            await ctx.send(self.output("IP Lookup", self.output2.funny_line(message)))

        @self.bot.command()
        async def portscan(ctx, ip):
            await ctx.message.delete()
            ports = [(21, "ftp"), (22, "ssh"), (23, "telnet"), (25, "smtp"), (53, "dns"), (80, "http"), (110, "pop3"), (443, "https")]
            message = ""
            padding = self.general.basic_padding(ports)
            for port, name in ports:
                s = socket.socket()
                s.settimeout(0.5)
                result = s.connect_ex((ip, port))
                if result == 0:
                    while len(name) < padding:
                        name += " "
                    message += "{}: {}\n".format(name, port)
            await ctx.send(self.output("Port Scan", self.output2.funny_line(message)))

        @self.bot.command()
        async def phonenumber(ctx, number):
            await ctx.message.delete()
            number = phonenumbers.parse(number)
            carier = carrier.name_for_number(number, "en")
            region = geocoder.description_for_number(number, "en")
            message = "Carrier: {}\nRegion : {}".format(carier, region)
            await ctx.send(self.output("Phone Number", message))

        @self.bot.command()
        async def lastcommand(ctx):
            await ctx.message.delete()
            await ctx.send(self.output("Last Command", self.lastcommand))

        @self.bot.command()
        async def selfdestruct(ctx, msgcount=100, delay=2):
            await ctx.message.delete()
            for mesasge in await ctx.channel.history(limit=msgcount).flatten():
                time.sleep(delay)
                if ctx.author.id == mesasge.author.id:
                    if mesasge.id != ctx.message.id:
                        await mesasge.delete()

        @self.bot.command()
        async def ping(ctx):
            await ctx.message.delete()
            self.logging.Success("Pong!")
            self.logging.Error("Pong!")
            self.logging.Info("Pong!")
            await ctx.send(self.output("Test", "Mode"))

        @self.bot.command()
        async def restart(ctx):
            await ctx.message.delete()
            subprocess.run(["python", __file__])
            print("Restarting...")
            exit()


        @self.bot.command()
        async def searchmsg(ctx, id, mode="messages", upload="n"):
            await ctx.message.delete()
            username = id
            if mode == "messages":
                messages = self.database.messageloggerget(username)
            elif mode == "deleted":
                messages = self.database.deletedloggerget(username)
            message = ""
            for msg in messages:
                message += "[{}] [{}] {}\n".format(msg[1], msg[3], msg[2])

            with open("Assets/Logs/{}.txt".format(username), "w") as f:
                f.write(message)
            
            if upload == "y":
                await ctx.send(file=discord.File("Assets/Logs/{}.txt".format(username)))
                return

            def split(message):
                msgs = []
                while len(message) > 1000:
                    msgs.append(message[:1000])
                    message = message[1000:]
                msgs.append(message)

                return msgs
            

            if len(list(message)) > 2000:
                msgs = split(message)

                for msg in msgs:
                    await ctx.send(self.output("Search Message", self.output2.funny_line(msg)))
                    time.sleep(2)
                return
            await ctx.send(self.output("Search Message", self.output2.funny_line(message)))

        @self.bot.command()
        async def cmdinfo(ctx, cmd):
            await ctx.message.delete()
            description, params, example = self.search.get(cmd)
            message = ""
            maxparam = max([len(param[0]) for param in params]) if params else 0
            for param in params:
                message += "{} : {}\n".format(param[0].ljust(maxparam), param[1])
            await ctx.send(self.output("Command Info", f"Description: {description}\n\n{message}\nExample: {example}\n"))

        @self.bot.command()
        async def whois(ctx, id):
            await ctx.message.delete()
            api = "https://discord.com/api/v9/users/{}/profile".format(id)
            headers = {"authorization": self.token}

            response = requests.get(api, headers=headers)

            if response.status_code == 200:
                msg = "Basic Information:\n\n"
                basic = ""
                for key, value in response.json().get("user").items():
                    if key != "bio":
                        basic += "{}: {}\n".format(key.title(), value) 

                msg += basic

                connected = ""
                for account in response.json().get("connected_accounts"):
                    connected += "{}: {}\n".format(account["type"].title(), account["name"])
                if connected:
                    msg += "\nConnected Accounts:\n\n"
                    msg += connected

                await ctx.send(self.output("Whois", self.output2.funny_line(msg)))


            else:
                return
        

        @self.bot.command()
        async def cmdcount(ctx):
            await ctx.message.delete()
            await ctx.send(self.output("Command Count", str(len(self.bot.commands)) + "\n"))

        @self.bot.command()
        async def scrape(ctx, channelid=""):
            await ctx.message.delete()
            x = 0
            if not channelid:
                channelid = ctx.channel.id

            headers = {"authorization": self.token}
            api = "https://discord.com/api/v9/channels/{}/messages?limit=100".format(channelid)
            
            params = {}

            while True:
                def dump(data):
                    file_path = "Scrapes/{}.txt".format(channelid)
                    with open(file_path, "a", encoding="utf-8") as f:
                        for message in data:
                            msg = "[{}]\t[{}]: {}\n".format(message["timestamp"], message["author"]["username"], message["content"])
                            f.write(msg)
                r = requests.get(api, headers=headers, params=params)

                if r.status_code == 429:
                    time.sleep(r.json()["retry_after"] + 5)
                elif r.status_code != 200:
                    return

                data = r.json()
                if not data:
                    break

                dump(data)
                params['before'] = data[-1]['id']

        @self.bot.command()
        async def reversedns(ctx, ip):
            await ctx.message.delete()
            s = socket.gethostbyaddr(ip)

            await ctx.send(self.output("Reversedns", s[0]))

        @self.bot.command()
        async def addpresence(ctx, name, id, state="", largeimagekey="", largeimagetext="", smallimagekey="", smallimagetext=""):
            await ctx.message.delete()
            self.presence.addpres(name, id, state, largeimagekey, largeimagetext, smallimagekey, smallimagetext)

        @self.bot.command()
        async def createpresence(ctx, name, state="", largeimagekeypath=None, largeimagetext=None, smallimagekeypath=None, smallimagetext=None):
            await ctx.message.delete()
            self.presence.altadd(name, state, largeimagekeypath, largeimagetext, smallimagekeypath, smallimagetext)

        @self.bot.command()
        async def loadpresence(ctx, name):
            await ctx.message.delete()
            threading.Thread(target=self.presence.pres, args=(name,)).start()

        @self.bot.command()
        async def stoppresence(ctx):
            await ctx.message.delete()
            self.presence.stoppres()
        
        @self.bot.command()
        async def listpres(ctx):
            await ctx.message.delete()
            profiles = self.presence.listpres()

            await ctx.send(self.output("List Presence", "\n".join(profiles)))

        @self.bot.command()
        async def spoofmobile(ctx):
            await ctx.message.delete()
            global last_heartbeat_ack, heartbeat_interval, ws
            
            last_heartbeat_ack = False
            heartbeat_interval = 0
            ws = None
            dcws = "wss://gateway.discord.gg/?v=9&encoding=json"
            
            def payload():
                return json.dumps({
                    "op": 2,
                    "d": {
                        "token": self.token,
                        "properties": {
                            "$os": "iOS",
                            "$browser": "Discord iOS",
                            "$device": "Discord iOS"
                        }
                    }
                })
            
            def heartbeat():
                global last_heartbeat_ack, heartbeat_interval
                while True:
                    if heartbeat_interval:
                        time.sleep(heartbeat_interval / 1000)
                        if not last_heartbeat_ack:
                            self.logging.Info("Heartbeat not acknowledged, reconnecting...")
                            ws.send(json.dumps({"op": 1, "d": None}))
                        last_heartbeat_ack = False
                        ws.send(json.dumps({"op": 1, "d": None}))

            def on_message(ws, message):
                global last_heartbeat_ack, heartbeat_interval
                data = json.loads(message)
                if data['op'] == 10:  # Hello
                    heartbeat_interval = data['d']['heartbeat_interval']
                    threading.Thread(target=heartbeat).start()
                    ws.send(payload())
                elif data['op'] == 11:
                    last_heartbeat_ack = True
            
            def on_error(ws, error):
                self.logging.Error(error)
            
            def on_close(ws, close_status_code, close_msg):
                self.logging.Info("Connection closed")
                connect()
            
            def on_open(ws):
                self.logging.Info("Spoofing mobile device...")

            def connect():
                global ws
                ws = websocket.WebSocketApp(dcws,
                                            on_message=on_message,
                                            on_error=on_error,
                                            on_close=on_close,
                                            on_open=on_open)
                
                ws.run_forever()

            connect()
        
        @self.bot.command()
        async def setupnotifs(ctx):
            await ctx.message.delete()
            self.events.setup(ctx.guild.id)


        @self.bot.command()
        async def checkhooks(ctx):
            await ctx.message.delete()
            self.events.checkhooks()

        @self.bot.command()
        async def listscripts(ctx):
            await ctx.message.delete()
            message = ""
            for script in self.scripts:
                message += "[{}] {}".format(str(self.scripts.index(script) + 1), script) + "\n"
            await ctx.send(self.output("Scripts", self.output2.funny_line(message)))

        @self.bot.command()
        async def isfemboy(ctx, userid):
            api = "https://discord.com/api/v9/users/{}/profile".format(userid)
            score = 0
            flags = [">.<", "^-^", "^_^", ">w<", ":c", "c:", ":p", ":3", "only-my.space", "femboy", ":flag_cz:", ":flag_pl:", "they/them"]
            possible = len(flags)

            r = requests.get(api, headers=self.sessionheaders)

            if r.status_code == 200:
                data = r.json()
                user = []
                user.append(data.get("user", {}).get("username", ""))
                user.append(data.get("user", {}).get("global_name", ""))
                user.append(data.get("user", {}).get("bio", ""))
                user.append(data.get("user", {}).get("pronouns", ""))
                
                for account in data.get("connected_accounts", []):
                    user.append(account.get("name", ""))
                
                for item in user:
                    for flag in flags:
                        if flag in item:
                            score += 1
                            break

            await ctx.send("Score: {}/{}".format(score, str(possible)))

        # NSFW
        @self.bot.command()
        async def r34(ctx, search):
            await ctx.message.delete()
            api = "https://api.r34.app/booru/rule34.xxx/posts?baseEndpoint=rule34.xxx&tags={}".format(search)

            r = self.session.get(api)

            if r.status_code == 200:
                data = r.json()
                files = data["data"]
                section = random.choice(files)
                link = section.get("high_res_file", "").get("url", "")

                await ctx.send("**[**Rule34 - {}**]** {}".format(search, link))
        @self.bot.command()
        async def pornhub(ctx, search):
            await ctx.message.delete()
            urls = []
            searchurl = "https://www.pornhub.com/video/search?search={}".format(search.replace(" ", "+").lower())

            headers = {"User-Agent" : self.spoof.useragent()}

            page = self.session.get(searchurl, headers=headers)
            soup = BeautifulSoup(page.text, 'html.parser')

            a = soup.find_all("a", href=True)
            for i in a:
                if "/view_video.php?viewkey=" in i["href"]:
                    urls.append("https://www.pornhub.com{}".format(i["href"]))

            
            lastpage = int(soup.find_all("li", class_="page_number")[-1].text)

            if lastpage >= 10:
                lastpage = 10

            for i in range(1, lastpage):
                page = self.session.get("https://www.pornhub.com/video/search?search={}&page={}".format(search.replace(" ", "+").lower(), i))
                soup = BeautifulSoup(page.text, 'html.parser')

                a = soup.find_all("a", href=True)
                for i in a:
                    if "/view_video.php?viewkey=" in i["href"]:
                        urls.append("https://www.pornhub.com{}".format(i["href"]))

            chosenone = random.choice(urls)
            await ctx.send("[**[**PornHub - {} - ({}/{})**]**]({})".format(search, str(urls.index(chosenone) + 1), str(len(urls)), chosenone))

        @self.bot.command()
        async def pornhubmodel(ctx, search):
            await ctx.message.delete()
            urls = []
            searchurl = "https://www.pornhub.com/model/{}/videos".format(search.replace(" ", "-").lower())

            headers = {"User-Agent" : self.spoof.useragent()}

            page = self.session.get(searchurl, headers=headers)
            soup = BeautifulSoup(page.text, 'html.parser')

            a = soup.find_all("a", href=True)
            for i in a:
                if "/view_video.php?viewkey=" in i["href"]:
                    urls.append("https://www.pornhub.com{}".format(i["href"]))

            lastpage = int(soup.find_all("li", class_="page_number")[-1].text)

            if lastpage >= 10:
                lastpage = 10


            for i in range(1, lastpage):
                page = self.session.get("https://www.pornhub.com/model/{}/videos?page={}".format(search.replace(" ", "-").lower(), i))
                soup = BeautifulSoup(page.text, 'html.parser')

                a = soup.find_all("a", href=True)
                for i in a:
                    if "/view_video.php?viewkey=" in i["href"]:
                        urls.append("https://www.pornhub.com{}".format(i["href"]))
            chosenone = random.choice(urls)
            await ctx.send("[**[**PornHub - {} - ({}/{})**]**]({})".format(search, str(urls.index(chosenone) + 1), str(len(urls)), chosenone))

        @self.bot.command()
        async def xvideos(ctx, search):
            await ctx.message.delete()
            urls = []
            searchurl = "https://www.xvideos.com/?k={}".format(search.replace(" ", "+"))

            page = self.session.get(searchurl)
            soup = BeautifulSoup(page.text, 'html.parser')

            a = soup.find_all("a", href=True)
            for i in a:
                if "/video." in i["href"]:
                    urls.append("https://www.xvideos.com{}".format(i["href"]))

            lastpage = int(soup.find("a", class_="last-page").text)
            if lastpage >= 10:
                lastpage = 10
            
            for i in range(1, lastpage):
                page = self.session.get("https://www.xvideos.com/?k={}&page={}".format(search.replace(" ", "+"), i))
                soup = BeautifulSoup(page.text, 'html.parser')


                a = soup.find_all("a", href=True)
                for i in a:
                    if "/video." in i["href"]:
                        urls.append("https://www.xvideos.com{}".format(i["href"]))
            chosenone = random.choice(urls)
            await ctx.send("[**[**Xvideos - {} - ({}/{})**]**]({})".format(search, str(urls.index(chosenone) + 1), str(len(urls)), chosenone))

        @self.bot.command()
        async def gelbooru(ctx, search):
            await ctx.message.delete()
            api = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags={}".format(search)
            params = {"api_key" : self.gelkey, "user_id" : self.userid, "tags" : search, "json" : 1}
            
            r = self.session.get(api, params=params)

            if r.status_code == 200:
                data = r.json()

                post = random.choice(data.get("post", ""))
                file = post.get("file_url", "").replace("\\", "")

                await ctx.send("**[**Gelbooru - {}**]** {}".format(search, file))

        @self.bot.command()
        async def status(ctx, status):
            await ctx.message.delete()
            await self.bot.change_presence(activity=discord.Game(name=status))


        # Crypto

        @self.bot.command()
        async def rot(ctx, string, mode="encode", shift=13):
            await ctx.message.delete()
            result = self.crypto.rot(string, mode, shift)
            await ctx.send(self.output("Rot{}".format(str(shift)), "Result: {}".format(result)))

        @self.bot.command()
        async def b64(ctx, string, mode="encode"):
            await ctx.message.delete()
            result = self.crypto.b64(string, mode)
            await ctx.send(self.output("Base64", "Result: {}".format(result)))



        # Other
        @self.bot.command()
        async def credits(ctx):
            await ctx.message.delete()
            message = """Developed primarily by /jwe0   - https://github.com/jwe0
Aided by my goo friend neebooo - https://github.com/neebooo

I made this to test my skill as a developer when tasked with a large project.
""" 
            await ctx.send(self.output("Credits", message))

    
    def _help(self, section, cmds, page=1):
        return self.output("{} / Cmds: ({}) / Page: ({}/{})".format(section, str(cmds[1]), str(page), str(cmds[2])), self.general.help_format(cmds[0]))


    def run(self):
        Colors.white
        # Load config
        self.logging.Info("Loading config...")
        self.token, self.prefix, self.nitro, self.messagel, antitokenlog, autologout, userpass, tcrypt, self.gelkey, self.userid, self.give, press = self.general.load_config()
        if self.general.checktoken(self.token) == False:
            self.logging.Error("Invalid token!")
            input("[>] Press enter to exit.")
            exit()
        # Initalize discord.py
        self.logging.Info("Setting up the bot...")
        self.bot = commands.Bot(command_prefix=self.prefix, self_bot=True)
        self.bot.remove_command("help")
        self.logging.Info("Initializing...")
        self.initalize()
        # Setup anti token logger
        if antitokenlog:
            self.logging.Info("Setting up anti token logger...")
            self.anti = AntiTokenLog(self.token, autologout, userpass, tcrypt)
            self.anti.getclients()
            threading.Thread(target=self.anti.getrecent).start()
        # Load other configs
        self.logging.Info("Loading other configs...")
        self.givesettings  = self.general.load_givesniper_settings()
        self.nitrosettings = self.general.load_nitrosniper_settings()
        # Setup mass react
        self.logging.Info("Setting up mass react... ")
        self.massr = MassReact(self.token)
        self.massr.init()
        # Create session headers
        self.logging.Info("Loading session headers...")
        self.sessionheaders = self.spoof.headers(self.token)
        # Load custom scripts
        self.logging.Info("Loading scripts...")
        for file in os.listdir("Scripts"):
            if file.endswith(".py"):
                exec(open("Scripts/{}".format(file), "r").read())
                self.scripts.append(file.split(".py")[0])
        # Setup pypresence
        if press:
            self.logging.Info("Setting up pypresence...")
            self.presence = Presence(self.token)
            threading.Thread(target=self.presence.pres).start()
        # Run
        self.logging.Info("Running bot...")
        self.bot.run(self.token, bot=False)


if __name__ == "__main__":
    initalize = Init()
    bot = Bot()
    initalize.init()
    bot.run()
