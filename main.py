import discord, requests, socket, threading, phonenumbers, time, subprocess, websocket, json, random, tls_client, os, socket, cairosvg, string, base64
import modules.wsmemberscrape
from phonenumbers import carrier
from pystyle import Center
from phonenumbers import geocoder
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageDraw, ImageFont
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
from modules.osint import OSINT

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
        self.osint    = OSINT()
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
        self.foot     = False
        self.session  = tls_client.Session()


        # Storing values
        self.lastcommand = ""
        self.cmds        = json.loads(open("modules/Dependencies/cmds.json").read())
        self.sessionheaders = ""
        self.nitrosettings  = {}
        self.givesettings   = {}
        self.footer         = {}
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
            try:
                await ctx.message.delete()
            except:
                pass
            self.logging.Error(str(error))

        @self.bot.event
        async def on_message(message):
            await self.bot.process_commands(message)
            if self.messagel:
                self.database.messageloggeradd(message.author.id, message.author.name, self.general.removespecial(message.content), message.created_at.strftime("%Y-%m-%d - %H:%M:%S"))
            if self.foot:
                if message.author == self.bot.user:
                    footer_title = self.footer.get("Footer", "")
                    footer_link  = self.footer.get("Link", "")
                    footer_text  = self.footer.get("Linktext", "")
                    content = f"{message.content}\n-# {footer_title} · [{footer_text}](<{footer_link}>)"
                    try:
                        await message.edit(content=content)
                    except:
                        pass
        @self.bot.event
        async def on_message_delete(message):
            if self.messagel:
                self.database.deletedloggeradd(message.author.id, message.author.name,self.general.removespecial(message.content), message.created_at.strftime("%Y-%m-%d - %H:%M:%S"))
                


        @self.bot.command()
        async def help(ctx):
            await ctx.message.delete()
            options = [
                {"name": "raid", "description": "Commands for raiding", "params": [["PAGE", "(Page number)"]], "section": "raid", "page": 1},
                {"name": "troll", "description": "Commands for trolling", "params": [["PAGE", "(Page number)"]], "section": "troll", "page": 1},
                {"name": "fun", "description": "Commands for fun", "params": [["PAGE", "(Page number)"]], "section": "fun", "page": 1},
                {"name": "utilities", "description": "Commands for utility", "params": [["PAGE", "(Page number)"]], "section": "utilities", "page": 1},
                {"name": "nsfw", "description": "Commands for NSFW", "params": [["PAGE", "(Page number)"]], "section": "nsfw", "page": 1},
                {"name": "crypto", "description": "Commands for cryptography", "params": [["PAGE", "(Page number)"]], "section": "crypto", "page": 1},
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
                self.logging.Info("Created channel: " + str(id))
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
                self.logging.Info("Renamed channel: " + str(id))
                while r.status_code != 200:
                    r = requests.patch(api, headers={"authorization": self.token}, json=data)
                    if r.status_code == 429:
                        self.logging.Error("Request throttled waiting {}".format(str(r.json()["retry_after"])))
                        time.sleep(r.json()["retry_after"] + 1)
                leave(id)

            def leave(id):
                api = "https://discord.com/api/v9/channels/{}?silent=true".format(id)
                r = requests.delete(api, headers={"authorization": self.token})
                self.logging.Info("Left channel: " + str(id))
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

        @self.bot.command()
        async def pollspam(ctx, question="What is the best free selfbot?", uanswers="Invictus,Invictus,Invictus,Invictus,Invictus", count=10, delay=2, thread="n"):
            await ctx.message.delete()
            answers = []
            user_answers = uanswers.split(",")
            for answer in user_answers:
                answers.append({
                    "poll_media": {
                        "text": answer,
                        "emoji": {
                            "name": "💀"
                        }
                    }
                })
            api = "https://discord.com/api/v9/channels/{}/messages".format(ctx.channel.id)
            data = {
                "content" : "",
                "flags"   : 0,
                "poll": {
                    "question": {"text": question},
                    "answers": answers,
                    "allow_multiselect": True,
                    "duration": 336,
                    "layout_type": 1
                    }
                }
            def create():
                r = self.session.post(api, headers=self.sessionheaders, json=data)

            for i in range(int(count)):
                create() if thread.lower() == "n" else threading.Thread(target=create).start()
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

        @self.bot.command()
        async def blockflood(ctx, loops=5):
            await ctx.message.delete()
            msg = "`" * 2000
            for i in range(int(loops)):
                await ctx.send(msg)

        @self.bot.command()
        async def tweet(ctx, user: discord.User = None, message=""):
            await ctx.message.delete()
            if user == None:
                return
            def create_fake_tweet(username, handle, content, profile_image_path, output_image_path):
                replies = random.randint(0, 100000)
                retweets = random.randint(0, 100000)
                likes = random.randint(0, 100000)
                views = random.randint(0, 100000)
                bookmarks = random.randint(0, 100000)
                chrome_options = Options()
                chrome_options.add_argument('--headless') 
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')

                driver = webdriver.Chrome(options=chrome_options)

                driver.set_window_size(1920, 1080) 

                driver.get("https://invictus-sb.netlify.app/tweet?avatar={}&username={}&handle={}&content={}&replies={}&retweets={}&likes={}&timestamp=today&views={}&bookmarks={}".format(profile_image_path, username, handle, content, replies, retweets, likes, views, bookmarks))

                screenshot_path = "Assets/Temp/screenshot.png"
                driver.save_screenshot(screenshot_path)

                driver.quit()

                with Image.open(screenshot_path) as img:
                    left = 690
                    upper = 440
                    right = 1230
                    lower = 635
                    cropped_img = img.crop((left, upper, right, lower))
                    cropped_img.save(output_image_path)

            def down_av(id, av):
                url = "https://cdn.discordapp.com/avatars/{}/{}?size=1024".format(id, av)
                return url

            def remove():
                os.remove("Assets/Temp/tweet.png")
                os.remove("Assets/Temp/screenshot.png")
            
            def get_info(id):
                api = "https://discord.com/api/v9/users/{}".format(id)
                r = self.session.get(api, headers=self.sessionheaders)
                if r.status_code == 200:
                    data = r.json()
                    usernam = data.get("username")
                    globaln = data.get("global_name")
                    avatar  = data.get("avatar")
                    avatar = down_av(id, avatar)
                    return usernam, globaln, avatar
            info = get_info(user.id)
            create_fake_tweet(username=info[0], handle=info[1], content=message, profile_image_path=info[2], output_image_path="Assets/Temp/tweet.png")
            await ctx.send(file=discord.File("Assets/Temp/tweet.png"))
            remove()

        @self.bot.command()
        async def hubcomment(ctx, user: discord.User = None, message=""):
            await ctx.message.delete()

            if user == None:
                return
            def create_fake_tweet(username, handle, content, profile_image_path, output_image_path):
                likes = random.randint(0, 1000)
                chrome_options = Options()
                chrome_options.add_argument('--headless') 
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')

                driver = webdriver.Chrome(options=chrome_options)

                driver.set_window_size(1920, 1080) 
                url = "https://invictus-sb.netlify.app/pornhub?username={}&content={}&timestamp={}&likes={}".format(username, content, "today", likes)
                driver.get(url)

                screenshot_path = "Assets/Temp/screenshot.png"
                driver.save_screenshot(screenshot_path)

                driver.quit()

                with Image.open(screenshot_path) as img:
                    left = 460
                    upper = 23
                    right = 930
                    lower = 150
                    cropped_img = img.crop((left, upper, right, lower))
                    cropped_img.save("Assets/Temp/pornhub.png")

            def down_av(id, av):
                url = "https://cdn.discordapp.com/avatars/{}/{}?size=1024".format(id, av)
                return url
            def remove():
                os.remove("Assets/Temp/pornhub.png")
                os.remove("Assets/Temp/screenshot.png")
            
            def get_info(id):
                api = "https://discord.com/api/v9/users/{}".format(id)
                r = self.session.get(api, headers=self.sessionheaders)
                if r.status_code == 200:
                    data = r.json()
                    usernam = data.get("username")
                    globaln = data.get("global_name")
                    avatar  = data.get("avatar")
                    avatar = down_av(id, avatar)
                    return usernam, globaln, avatar
            info = get_info(user.id)
            create_fake_tweet(username=info[0], handle=info[1], content=message, profile_image_path=info[2], output_image_path="Assets/Temp/pornhub.png")
            await ctx.send(file=discord.File("Assets/Temp/pornhub.png"))
            remove()



            

        # Fun commands  

        @self.bot.command()
        async def gayrate(ctx, user: discord.User = None):
            await ctx.message.delete()
            percent = random.randint(0, 100) # [("User", [user.mention]), ("Rate", [str(percent) + "%"])]
            message = self.output("Gayrate", "User: " + user.mention + "\nRate: " + str(percent) + "%")
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

        @self.bot.command()
        async def phlogo(ctx, start, end):
            await ctx.message.delete()
            api = "https://logohub.appspot.com/{}-{}".format(start, end)
            r = requests.get(api)
            svg = r.content
            with open("Assets/Temp/temp.svg", "wb") as f:
                f.write(svg)
            cairosvg.svg2png(url="Assets/Temp/temp.svg", write_to="Assets/Temp/temp.png")
            await ctx.send(file=discord.File("Assets/Temp/temp.png"))
            os.remove("Assets/Temp/temp.png")
            os.remove("Assets/Temp/temp.svg")

        @self.bot.command()
        async def pethttpcat(ctx, code):
            await ctx.message.delete()
            r = requests.get("https://http.cat/{}".format(code))
            with open("Assets/Temp/temp.png", "wb") as f:
                f.write(r.content)
            await ctx.send(file=discord.File("Assets/Temp/temp.png"))
            os.remove("Assets/Temp/temp.png")

        @self.bot.command()
        async def sethype(ctx, house="bravery"):
            await ctx.message.delete()
            houses  = {
                "bravery" : 1,
                "brilliance" : 2,
                "balance" : 3
            }
            data = {"house_id" : houses[house]}
            api = "https://discord.com/api/v9/hypesquad/online"
            r = self.session.post(api, headers=self.sessionheaders, json=data)

        @self.bot.command()
        async def tokengrab(ctx, id=""):
            await ctx.message.delete()
            if not id:
                self.logging.error("No ID provided")
                return
            token = base64.b64encode(id.encode()).decode().rstrip("=")

            await ctx.send(self.output("Token Grab", token))
            

        
        # Utility commands

        @self.bot.command()
        async def iplookup(ctx, ip):
            await ctx.message.delete()
            url = "http://ip-api.com/json/{}".format(ip)
            r = requests.get(url)
            data = r.json()

            table = [("Key", [str(key).title() for key in data.keys()]), ("Value", [str(value) for value in data.values()])]
            await ctx.send(self.output("IP Lookup", table))

        @self.bot.command()
        async def portscan(ctx, ip):
            await ctx.message.delete()
            ports = [(21, "ftp"), (22, "ssh"), (23, "telnet"), (25, "smtp"), (53, "dns"), (80, "http"), (110, "pop3"), (443, "https")]
            padding = self.general.basic_padding(ports)
            openx = []
            namex = []
            for port, name in ports:
                s = socket.socket()
                s.settimeout(0.5)
                result = s.connect_ex((ip, port))
                if result == 0:
                    while len(name) < padding:
                        name += " "
                    openx.append(str(port))
                    namex.append(name)
            result = [("Port", openx), ("Name", namex)]
            await ctx.send(self.output("Port Scan", result))

        @self.bot.command()
        async def phonenumber(ctx, number):
            await ctx.message.delete()
            number = phonenumbers.parse(number)
            carier = carrier.name_for_number(number, "en")
            region = geocoder.description_for_number(number, "en")
            message = "Carrier: {}\nRegion : {}".format(carier, region)
            await ctx.send(self.output("Phone Number", [("Carrier", [carier]), ("Region", [region])]))

        @self.bot.command()
        async def lastcommand(ctx):
            await ctx.message.delete()
            await ctx.send(self.output("Last Command", [("Command", [self.lastcommand])]))

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
            await ctx.send(self.output("Test", [("Ping", ["Pong"])]))

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
            nparams = []
            for param in params:
                nparams.append(param[0] + " : " + param[1])
            param = "\n".join(nparams)
            await ctx.send(self.output("Command Info", "Description: {}\n\n{}\n\nExample: {}".format(description, param, example)))

        @self.bot.command()
        async def whois(ctx, id):
            await ctx.message.delete()
            api = "https://discord.com/api/v9/users/{}/profile".format(id)
            headers = {"authorization": self.token}

            response = requests.get(api, headers=headers)
            keys = []
            vals = []
            if response.status_code == 200:
                keys.append("User info")
                vals.append("-" * 20)
                for key, value in response.json().get("user").items():
                    if key != "bio":
                        keys.append(str(key).title())
                        vals.append(str(value))
                if "connected_accounts" in response.json().get("user"):
                    keys.append("Connected Accounts")
                    vals.append("-" * 20)
                    for account in response.json().get("connected_accounts"):
                        keys.append(str(account.get("type").title()))
                        vals.append(account.get("name"))
                if "badges" in response.json():
                    keys.append("Badges")
                    vals.append("-" * 20)
                    for badge in response.json().get("badges"):
                        keys.append(badge.get("description"))
                        vals.append("None")
                if len(keys) > 0:
                    table = [("Key", keys), ("Value", vals)]
                else:
                    table = [("Error", "No user found with that ID")]
                await ctx.send(self.output("Whois", table))
            else:
                return
        

        @self.bot.command()
        async def cmdcount(ctx):
            await ctx.message.delete()
            await ctx.send(self.output("Command Count", [("Count", [str(len(self.bot.commands))])]))

        @self.bot.command()
        async def scrape(ctx, channelid=""):
            await ctx.message.delete()
            x = 0
            channelid = channelid if channelid else ctx.channel.id
            headers = {"authorization": self.token}
            api = "https://discord.com/api/v9/channels/{}/messages?limit=100".format(channelid)
            params = {}
            while True:
                def dump(data):
                    file_path = "Scrapes/Messages/{}.txt".format(channelid)
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

            await ctx.send(self.output("Reversedns", [("IP", [ip]), ("Host", [s[0]])]))

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

            await ctx.send(self.output("List Presence", [("Profiles", profiles)]))

        @self.bot.command()
        async def spoof(ctx, device):
            await ctx.message.delete()
            global last_heartbeat_ack, heartbeat_interval, ws
            vals = []
            
            last_heartbeat_ack = False
            heartbeat_interval = 0
            ws = None
            dcws = "wss://gateway.discord.gg/?v=9&encoding=json"
            if device == "mobile":
                vals.append("iOS")
                vals.append("Discord iOS")
                vals.append("iOS")
            elif device == "pc":
                vals.append("Windows")
                vals.append("Discord")
                vals.append("Windows")
            elif device == "browser":
                vals.append("Linux")
                vals.append("Discord Browser")
                vals.append("Linux")
            elif device == "console":
                vals.append("Xbox")
                vals.append("Xbox")
                vals.append("Console")

            
            def payload():
                return json.dumps({
                    "op": 2,
                    "d": {
                        "token": self.token,
                        "properties": {
                            "$os": vals[0],
                            "$browser": vals[1],
                            "$device": vals[2]
                        },
                        "presence": {
                            "status": "online",
                            "activities": [],
                            "afk": False
                        },
                        "intents": 513
                    }
                })
            
            def heartbeat():
                global last_heartbeat_ack, heartbeat_interval
                while True:
                    if heartbeat_interval:
                        time.sleep(heartbeat_interval / 1000)
                        ws.send(json.dumps({"op": 1, "d": "null"}))

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
                self.logging.Info("Spoofing {} device...".format(device))

            def connect():
                global ws
                ws = websocket.WebSocketApp(dcws,
                                            on_message=on_message,
                                            on_error=on_error,
                                            on_close=on_close,
                                            on_open=on_open)
                
                ws.run_forever()

            threading.Thread(target=connect).start()
        
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
            message = []
            for command in self.scripts:
                message.append(command)
            await ctx.send(self.output("Scripts", [("Scripts", message)]))

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

        @self.bot.command()
        async def upload(ctx, url):
            await ctx.message.delete()
            if os.path.exists(url):
                await ctx.send(file=discord.File(url))
            else:
                await ctx.send(url)

        @self.bot.command()
        async def username(ctx, username):
            await ctx.message.delete()
            results = self.osint.usernameosint(username)
            await ctx.send(self.output("Username Search", [("Results", results)]))

        @self.bot.command()
        async def webping(ctx, url):
            await ctx.message.delete()
            ping = self.general.ping(url)
            await ctx.send(self.output("Web Ping", [("Ping", [ping + "ms"])]))

        @self.bot.command()
        async def domainwhois(ctx, domain):
            await ctx.message.delete()
            result = self.osint.domainwhois(domain)
            await ctx.send(self.output("Domain Whois", [("Results", [result])]))

        @self.bot.command()
        async def search(ctx, command):
            await ctx.message.delete()
            pcmds = []
            pdesc = []
            pcsec = []
            pcexm = []
            pcpge = []
            for cmd in self.cmds:
                if command in cmd:
                    pcmds.append(cmd)
                    pdesc.append(self.cmds[cmd]["description"])
                    pcsec.append(self.cmds[cmd]["section"])
                    pcexm.append(self.cmds[cmd]["example"])
                    pcpge.append(str(self.cmds[cmd]["page"]))
            if len(pcmds) != 0:
                possibles = [("Command", pcmds), ("Description", pdesc), ("Section", pcsec), ("Page", pcpge), ("Example", pcexm)]
            else:
                possibles = [("Command", ["None found"])]
            await ctx.send(self.output("Search", possibles))

        @self.bot.command()
        async def serverbots(ctx):
            await ctx.message.delete()
            #https://discord.com/api/v9/applications/public?application_ids=235148962103951360
            api = "https://discord.com/api/v9/guilds/{}/application-command-index".format(ctx.guild.id)
            r = requests.get(api, headers=self.sessionheaders)
            bots = []
            botids = []
            if r.status_code == 200:
                apps = r.json().get("applications")
                for app in apps:
                    bots.append(app.get("name"))
                    botids.append(app.get("id"))
            if len(bots) != 0:
                table = [("Bots", bots), ("IDs", botids)]
            else:
                table = [("Bots", ["None found"])]
            await ctx.send(self.output("Server Bots", table))

        @self.bot.command()
        async def scrapemembers(ctx, guildid="", thread="n"):
            await ctx.message.delete()
            guildid  = ctx.guild.id if guildid == "" else guildid
            guildname = self.general.guildid_name(guildid)
            channels = []
            members  = []
            prog = 0
            channelapi = "https://discord.com/api/v9/guilds/{}/channels".format(guildid)
            messageapi = "https://discord.com/api/v9/channels/{}/messages?limit=100"
            def dump(message):
                with open("Scrapes/Members/{}.txt".format(str(guildname)), "w") as f:
                    f.write(message + "\n")
            def get_messages(id):
                nonlocal prog
                message_r = requests.get(messageapi.format(channel), headers=self.sessionheaders)
                while message_r.status_code == 429:
                    self.logging.Error("Request throttled waiting {}".format(str(message_r.json()["retry_after"])))
                    time.sleep(message_r.json()["retry_after"])
                    message_r = requests.get(messageapi.format(channel), headers=self.sessionheaders)
                for message in message_r.json():
                    if "author" in message:
                        id = message.get("author", {}).get("id")
                        if id not in members:
                            members.append(message.get("author", {}).get("id"))
                prog += 1
            self.logging.Info("Dumping members...")
            channel_r = requests.get(channelapi, headers=self.sessionheaders)
            for channel in channel_r.json():
                if channel.get("type") == 0:
                    channels.append(channel.get("id"))
            for channel in channels:
                get_messages(channel) if thread != "y" else threading.Thread(target=get_messages, args=(channel,)).start()
            while prog != len(channels) -1:
                pass
            dump("\n".join(members))
            self.logging.Info("Dumped {} members".format(str(len(members))))

        @self.bot.command()
        async def stats(ctx):
            await ctx.message.delete()
            uptime = self.output2.uptime()
            logons = self.output2.logons()
            await ctx.send(self.output("Stats", "Uptime: {}\nLogons: {}".format(uptime, logons)))

        @self.bot.command()
        async def scrapestickers(ctx, guildid="", thread="n"):
            await ctx.message.delete()
            guildid = guildid if guildid else ctx.guild.id
            guildname = self.general.guildid_name(guildid)
            self.logging.Info("Dumping stickers...")
            def check_folder():
                if not os.path.exists("Scrapes/Stickers/{}".format(guildname)):
                    os.makedirs("Scrapes/Stickers/{}".format(guildname))
            def get_stickers(id):
                stickers = []
                api = "https://discord.com/api/v9/guilds/{}/stickers".format(id)
                r = self.session.get(api, headers=self.sessionheaders)
                if r.status_code == 200:
                    for sticker in r.json():
                        stickers.append((sticker.get("name"), sticker.get("id")))
                return stickers
            def download(stickerid, name):
                result = requests.get(url=f"https://media.discordapp.net/stickers/{stickerid}.png")
                with open("Scrapes/Stickers/{}/{}.png".format(guildname, name), "wb") as f:
                    f.write(result.content)
            stickers = get_stickers(guildid)
            check_folder()
            for sticker in stickers:
                download(sticker[1], sticker[0]) if thread != "y" else threading.Thread(target=download, args=(sticker[1], sticker[0])).start()
            self.logging.Info("Dumped {} stickers".format(str(len(stickers))))

        @self.bot.command()
        async def scrapeemojis(ctx, guildid="", thread="n"):
            await ctx.message.delete()
            guildid = guildid if guildid else ctx.guild.id
            guildname = self.general.guildid_name(guildid)
            self.logging.Info("Dumping emojis...")
            def check_folder():
                if not os.path.exists("Scrapes/Emojis/{}".format(guildname)):
                    os.makedirs("Scrapes/Emojis/{}".format(guildname))
            def get_emojis(id):
                emojis = []
                api = "https://discordapp.com/api/v9/guilds/{}/emojis".format(id)
                r = self.session.get(api, headers=self.sessionheaders)
                if r.status_code == 200:
                    for emoji in r.json():
                        emojis.append((emoji.get("name"), emoji.get("id")))
                return emojis
            def download(emojiid, name):
                result = requests.get(url=f"https://media.discordapp.net/emojis/{emojiid}.png")
                with open("Scrapes/Emojis/{}/{}.png".format(guildname, name), "wb") as f:
                    f.write(result.content)
            emojis = get_emojis(guildid)
            check_folder()
            for emoji in emojis:
                download(emoji[1], emoji[0]) if thread != "y" else threading.Thread(target=download, args=(emoji[1], emoji[0])).start()
            self.logging.Info("Dumped {} emojis".format(str(len(emojis))))


        @self.bot.command()
        async def inviteinfo(ctx, code=""):

            if not code:
                self.logging.Info("Please specify a code")
                return
            api = "https://discord.com/api/v10/invites/{}".format(code)
            r = self.session.get(api)

            keys = []
            vals = []

            if r.status_code == 200:
                data = r.json()
                if "guild" in data:
                    keys.append("Guild")
                    vals.append("-" * 20)
                    for key, value in data.get("guild", {}).items():
                        if key not in ("description", "features"):
                            keys.append(key)
                            vals.append(value)
                if "inviter" in data:
                    keys.append("Inviter")
                    vals.append("-" * 20)
                    for key, value in data.get("inviter", {}).items():
                        keys.append(key)
                        vals.append(value)
                if "channel" in data:
                    keys.append("Channel")
                    vals.append("-" * 20)
                    for key, value in data.get("channel", {}).items():
                        keys.append(key)
                        vals.append(value)

                table = [("Key", [str(key).title() for key in keys]), ("Value", [str(value) for value in vals])]
                await ctx.send(self.output("Invite Info", table))

        @self.bot.command()
        async def serverinfo(ctx, id=""):
            guildid = id if id else ctx.guild.id
            api = "https://discord.com/api/v10/guilds/{}".format(guildid)
            r = self.session.get(api, headers=self.sessionheaders)
            keys = []
            vals = []
            if r.status_code == 200:
                data = r.json()
                blacklist = {
                    "icon", "splash", "afk_channel_id", "embed_enabled", "embed_channel_id", "roles",
                    "emojis", "features", "application_id", "widget_enabled", "widget_channel_id",
                    "system_channel_id", "rules_channel_id", "joined_at", "voice_states", "members",
                    "channels", "presences", "max_presences", "max_members", "vanity_url_code", "banner",
                    "premium_tier", "premium_subscription_count", "preferred_locale", "public_updates_channel_id",
                    "max_video_channel_users", "approximate_member_count", "approximate_presence_count",
                    "welcome_screen", "nsfw_level", "premium_progress_bar_enabled", "stickers", "latest_onboarding_question_id"
                }
                keys = []
                vals = []
                for key, value in data.items():
                    if key not in blacklist:
                        keys.append(key)
                        vals.append(value)
                table = [("Key", [str(key).title() for key in keys]), ("Value", [str(value) for value in vals])]
                await ctx.send(self.output("Server Info", table))


        @self.bot.command()
        async def wsmembers(ctx, guild, channel):
            await ctx.message.delete()
            guild = guild if guild else ctx.guild.id
            channel = channel if channel else ctx.channel.id
            mems = modules.wsmemberscrape.DiscordSocket(self.token, guild, channel).run()
            with open("Scrapes/Members/{}.txt".format(guild), "w") as f:
                f.write("\n".join(mems))
    
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
            await ctx.send(self.output("Rot{}".format(str(shift)), [("Rot{}".format(str(shift)), ["Result: {}".format(result)])]))

        @self.bot.command()
        async def b64(ctx, string, mode="encode"):
            await ctx.message.delete()
            result = self.crypto.b64(string, mode)
            await ctx.send(self.output("Base64", [("Base64", ["Result: {}".format(result)])]))

        @self.bot.command()
        async def aes(ctx, string, mode="encode", method="cbc", key=""):
            await ctx.message.delete()
            if len(key) != 16:
                self.logging.Error("Key must be 16 characters")
                return
            if method == "cbc":
                result = self.crypto.aes_cbc(string, key, mode)
            elif method == "ctr":
                result = self.crypto.aes_ctr(string, key, mode)
            elif method == "cfb":
                result = self.crypto.aes_cfb(string, key, mode)
            elif method == "ofb":
                result = self.crypto.aes_ofb(string, key, mode)

            await ctx.send(self.output("AES", [("AES", ["Result: {}".format(result)])]))

        @self.bot.command()
        async def fernet(ctx, string, mode="encode", key=""):
            await ctx.message.delete()
            if len(key) != 32:
                self.logging.Error("Key must be 32 characters")
                return
            result = self.crypto.fernet(string, key, mode)
            await ctx.send(self.output("Fernet", "Result: {}".format(result)))



        # Other
        @self.bot.command()
        async def credits(ctx):
            await ctx.message.delete()
            message = """Developed primarily by /jwe0   - https://github.com/jwe0
Aided by my good friend neebooo - https://github.com/neebooo

I made this to test my skill as a developer when tasked with a large project.

Homepage - https://invictus-sb.netlify.app/
""" 
            await ctx.send(self.output("Credits", message))

        @self.bot.command()
        async def mysqltest(ctx):
            await ctx.message.delete()
            args = [("Column1", ["Value1", "Value2"]), ("Column2", ["Value3", "Value"]), ("Column3", ["Value4", "Value5"])]
            result = self.output2.table(args)
            await ctx.send("```" + result + "```")

        @self.bot.command()
        async def embedtest(ctx):
            title = "".join([random.choice(string.ascii_letters) for _ in range(10)])
            desc = "".join([random.choice(string.ascii_letters) for _ in range(10)])
            author = "".join([random.choice(string.ascii_letters) for _ in range(10)])
            color = "000000"
            thumbnail = "https://i.imgur.com/TuL8lDN.jpeg"
            result = self.output2.embed(title, [("Column1", ["Value1", "Value2"]), ("Column2", ["Value3", "Value"])], author, color, thumbnail)
            await ctx.send(result)

        @self.bot.command()
        async def outputest(ctx):
            args = [("Column1", ["Value1", "Value2"]), ("Column2", ["Value3", "Value"]), ("Column3", ["Value4", "Value5"])]
            print(self.output2.array_to_message(args))
            msg = self.output("Debug", args)
            await ctx.send(msg)

    
    def _help(self, section, cmds, page=1):
        return self.output("{} / Cmds: ({}) / Page: ({}/{})".format(section, str(cmds[1]), str(page), str(cmds[2])), self.general.help_format(cmds[0]))


    def run(self):
        Colors.white
        # Load config
        self.logging.Info("Loading config...")
        self.token, self.prefix, self.nitro, self.messagel, antitokenlog, autologout, userpass, tcrypt, self.gelkey, self.userid, self.give, press, self.foot = self.general.load_config()
        token_check = self.general.checktoken(self.token)
        if token_check[0] == False:
            self.logging.Error("Invalid token!")
            self.logging.Error("Status code: {}".format(token_check[1]))
            self.logging.Error("Json response: {}".format(token_check[2]))
            self.logging.BasicInput("Press enter to exit...")
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
        # Setup osint
        self.logging.Info("Setting up osint...")
        self.osint.init()
        # Setup footer
        if self.foot:
            self.logging.Info("Setting up footer...")
            self.footer = self.general.get_footer()
        # Run
        self.general.update_logons()
        threading.Thread(target=self.general.update_uptime).start()
        self.logging.Info("Running bot...")
        self.bot.run(self.token, bot=False)


if __name__ == "__main__":
    initalize = Init()
    bot = Bot()
    initalize.init()
    bot.run()
