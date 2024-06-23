import discord, requests, socket, threading, phonenumbers, time, subprocess, websocket, json, random, tls_client
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
        self.anti     = None


        # Discord.py things
        self.bot    = None
        self.prefix = ""
        self.token  = ""

        # Modules
        self.nitro    = False
        self.messagel = False
        self.session  = tls_client.Session()

        # Storing values
        self.lastcommand = ""
        self.cmds        = json.loads(open("modules/Dependencies/cmds.json").read())
        self.sessionheaders = ""

        # Api keys
        self.gelkey = ""
        self.userid = ""
        


    def initalize(self):
        @self.bot.event
        async def on_ready():
            self.general.clear()
            self.general.art()
            print(Center.XCenter(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})\n"))

        @self.bot.event
        async def on_command(ctx):
            try:
                await ctx.message.delete()
            except:
                pass
            self.lastcommand = ctx.message.content

        @self.bot.event
        async def on_command_error(ctx, error):
            self.logging.Error(str(error))

        @self.bot.event
        async def on_message(message):
            await self.bot.process_commands(message)
            if self.messagel:
                self.database.messageloggeradd(message.author.id, message.author.name, self.general.removespecial(message.content), message.created_at.strftime("%Y-%m-%d - %H:%M:%S"))
            if message.author != self.bot.user:
                if self.nitro:
                    if "discord.gift/" in message.content:
                        self.logging.Info(f"Found nitro code: {message.content}")


        @self.bot.event
        async def on_message_delete(message):
            if self.messagel:
                self.database.deletedloggeradd(message.author.id, message.author.name,self.general.removespecial(message.content), message.created_at.strftime("%Y-%m-%d - %H:%M:%S"))
                


        @self.bot.command()
        async def help(ctx):
            options = [
                {"name": "raid", "description": "Commands for raiding", "params": [], "section": "raid", "page": 1},
                {"name": "troll", "description": "Commands for trolling", "params": [], "section": "troll", "page": 1},
                {"name": "fun", "description": "Commands for fun", "params": [], "section": "fun", "page": 1},
                {"name": "utilities", "description": "Commands for utility", "params": [], "section": "utilities", "page": 1},
                {"name": "nsfw", "description": "Commands for NSFW", "params": [], "section": "nsfw", "page": 1},
            ]

            message = self.general.help_format(options)
            await ctx.send(self.output("Help", message))

        @self.bot.command()
        async def raid(ctx, page=1):
            cmds = self.search.cmd(page, "raid")
            await ctx.send(self.output("Raid - {}".format(str(cmds[1])), self.general.help_format(cmds[0])))

        @self.bot.command()
        async def troll(ctx, page=1):
            cmds = self.search.cmd(page, "troll")
            await ctx.send(self.output("Troll - {}".format(str(cmds[1])), self.general.help_format(cmds[0])))

        @self.bot.command()
        async def fun(ctx, page=1):
            cmds = self.search.cmd(page, "fun")
            await ctx.send(self.output("Fun - {}".format(str(cmds[1])), self.general.help_format(cmds[0])))

        @self.bot.command()
        async def utilities(ctx, page=1):
            cmds = self.search.cmd(page, "utility")
            await ctx.send(self.output("Utilities - {}".format(str(cmds[1])), self.general.help_format(cmds[0])))

        @self.bot.command()
        async def nsfw(ctx, page=1):
            cmds = self.search.cmd(page, "nsfw")
            await ctx.send(self.output("NSFW - {}".format(str(cmds[1])), self.general.help_format(cmds[0])))

        # Raid commands
        @self.bot.command()
        async def messagespam(ctx, message="INVICTUS ON TOP", count=50, delay=2, thread="n"):
            WAIT = [False, 0]
            api = "https://discord.com/api/v9/channels/{}/messages".format(ctx.channel.id)
            data = {"content": message}
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
                time.sleep(delay)

        @self.bot.command()
        async def pinspam(ctx, count=50, delay=2, thread="n"):
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
        async def massping(ctx, loops=5, delay=1):
            def Get_Members(id):
                headers = {"Authorization": self.token}
                api     = "https://discord.com/api/v9/channels/{}/messages?limit=100".format(id)
                response = requests.get(api, headers=headers).json()
                members  = []

                for member in response:
                    if member["author"]["id"] not in members:
                        members.append(member["author"]["id"])

                return members
            members = Get_Members(ctx.channel.id)
            for _ in range(loops):
                message = []
                for member in members:
                    message.append(f"<@{member}>")
                    if len(message) == 3:
                        await ctx.send(" ".join(message))
                        message = []
                if message:
                    await ctx.send(" ".join(message))
                    message = []
                time.sleep(delay)

        @self.bot.command()
        async def webraid(ctx, channelname="raided-by-invictus", message="@everyone RAIDED BY INVICTUS", channelamount=20, messageamount=30):
            def webhook(hook):
                for i in range(int(messageamount)):
                    data = {"content" : message}
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




        # Troll commands

        @self.bot.command()
        async def vcspam(ctx, channel, count=10, delay=2):
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
            percent = random.randint(0, 100)
            message = self.output("Gayrate", f"{user.name} is {str(percent)}% gay\n")

            await ctx.send(message)

        @self.bot.command()
        async def ghostspam(ctx, user: discord.User = None, count=10, delay=2):
            mention = user.mention

            for i in range(int(count)):
                message = await ctx.send(mention)
                await message.delete()
                time.sleep(int(delay))





        

        # Utility commands

        @self.bot.command()
        async def iplookup(ctx, ip):
            url = "http://ip-api.com/json/{}".format(ip)
            r = requests.get(url)
            message = ""
            for key, value in r.json().items():
                message += "{}: {}\n".format(key.title(), value)
            await ctx.send(self.output("IP Lookup", self.output2.funny_line(message)))

        @self.bot.command()
        async def portscan(ctx, ip):
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
            number = phonenumbers.parse(number)
            carier = carrier.name_for_number(number, "en")
            region = geocoder.description_for_number(number, "en")
            message = "Carrier: {}\nRegion : {}".format(carier, region)
            await ctx.send(self.output("Phone Number", message))

        @self.bot.command()
        async def lastcommand(ctx):
            await ctx.send(self.output("Last Command", self.lastcommand))

        @self.bot.command()
        async def selfdestruct(ctx, msgcount=100, delay=2):
            for mesasge in await ctx.channel.history(limit=msgcount).flatten():
                time.sleep(delay)
                if ctx.author.id == mesasge.author.id:
                    if mesasge.id != ctx.message.id:
                        await mesasge.delete()

                        


        @self.bot.command()
        async def ping(ctx):
            self.logging.Success("Pong!")
            self.logging.Error("Pong!")
            self.logging.Info("Pong!")
            await ctx.send(self.output("Test", "Mode"))

        @self.bot.command()
        async def restart(ctx):
            subprocess.run(["python", __file__])
            print("Restarting...")
            exit()


        @self.bot.command()
        async def searchmsg(ctx, id, mode="messages", upload="n"):
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
            description, params, example = self.search.get(cmd)
            message = ""
            for param in params:
                message += "{}: {}\n".format(param[0], param[1])
            await ctx.send(self.output("Command Info", f"Description: {description}\n\n{message}\nExample: {example}\n"))

        @self.bot.command()
        async def whois(ctx, id):
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
            await ctx.send(self.output("Command Count", str(len(self.bot.commands)) + "\n"))

        # NSFW
        @self.bot.command()
        async def r34(ctx, search):
            api = "https://api.r34.app/booru/rule34.xxx/posts?baseEndpoint=rule34.xxx&tags={}".format(search)

            r = self.session.get(api)

            if r.status_code == 200:
                data = r.json()
                files = data["data"]
                section = random.choice(files)
                link = section.get("high_res_file", "").get("url", "")

                await ctx.send(link)
        @self.bot.command()
        async def pornhub(ctx, search):
            urls = []
            searchurl = "https://www.pornhub.com/video/search?search={}".format(search)

            page = self.session.get(searchurl)
            soup = BeautifulSoup(page.text, 'html.parser')

            a = soup.find_all("a", href=True)
            for i in a:
                if "/view_video.php?viewkey=" in i["href"]:
                    urls.append("https://www.pornhub.com{}".format(i["href"]))

            await ctx.send(random.choice(urls))

        @self.bot.command()
        async def gelbooru(ctx, search):
            api = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags={}".format(search)
            params = {"api_key" : self.gelkey, "user_id" : self.userid, "tags" : search, "json" : 1}
            
            r = self.session.get(api, params=params)

            if r.status_code == 200:
                data = r.json()

                post = random.choice(data.get("post", ""))
                file = post.get("file_url", "").replace("\\", "")

                await ctx.send(file)


        # Other
        @self.bot.command()
        async def credits(ctx):
            message = """Developed primarily by /jwe0   - https://github.com/jwe0
Aided by my goo friend neebooo - https://github.com/neebooo

I made this to test my skill as a developer when tasked with a large project.
""" 
            await ctx.send(self.output("Credits", message))

    



    def run(self):
        Colors.white
        self.logging.Info("[>] Loading config...")
        self.token, self.prefix, self.nitro, self.messagel, antitokenlog, autologout, userpass, tcrypt, self.gelkey, self.userid = self.general.load_config()
        if self.general.checktoken(self.token) == False:
            self.logging.Error("Invalid token!")
        self.logging.Info("[>] Setting up the bot...")
        self.bot = commands.Bot(command_prefix=self.prefix, self_bot=True)
        self.bot.remove_command("help")
        self.logging.Info("[>] Initializing...")
        self.initalize()
        if antitokenlog:
            self.logging.Info("[>] Setting up anti token logger...")
            self.anti = AntiTokenLog(self.token, autologout, userpass, tcrypt)
            self.anti.getclients()
            threading.Thread(target=self.anti.getrecent).start()
        self.logging.Info("[>] Loading session headers...")
        self.sessionheaders = self.spoof.headers(self.token)
        self.logging.Info("[>] Running bot...")
        self.bot.run(self.token, bot=False)


if __name__ == "__main__":
    initalize = Init()
    bot = Bot()
    initalize.init()
    bot.run()
