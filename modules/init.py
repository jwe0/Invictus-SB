import os, json,sqlite3
from modules.general import General

class Init:
    def __init__(self):
        self.general      = General()
        self.footer       = ""
        self.footlink     = ""
        self.footlinktext = ""

    def assets(self):
        if not os.path.exists("Assets"):
            os.mkdir("Assets")

    def msglogs(self):
        if not os.path.exists("Assets/Logs"):
            os.mkdir("Assets/Logs")

    def ipcache(self):
        if not os.path.exists("Assets/IPcache.json"):
            open("Assets/IPcache.json", "w").write("{}")

    def scripts(self):
        if not os.path.exists("Scripts"):
            os.mkdir("Scripts")
        if not os.path.exists("Scripts/example.py"):
            with open("Scripts/example.py", "w") as f:
                content = """import random
@self.bot.command()
async def example(ctx):
    await ctx.send(str(random.randint(1, 200)))"""
                f.write(content)

    def scrapes(self):
        if not os.path.exists("Scrapes"):
            os.mkdir("Scrapes")
        if not os.path.exists("Scrapes/Messages"):
            os.mkdir("Scrapes/Messages")
        if not os.path.exists("Scrapes/Members"):
            os.mkdir("Scrapes/Members")
        if not os.path.exists("Scrapes/Stickers"):
            os.mkdir("Scrapes/Stickers")
        if not os.path.exists("Scrapes/Emojis"):
            os.mkdir("Scrapes/Emojis")

    def settings(self):
        if not os.path.exists("Assets/Settings"):
            os.mkdir("Assets/Settings")

        if not os.path.exists("Assets/Settings/givesniper.json"):
            config = {
                "delay" : 1
            }

            with open("Assets/Settings/givesniper.json", "w") as f:
                json.dump(config, f, indent=4)

        if not os.path.exists("Assets/Settings/nitrosniper.json"):
            config = {
                "delay" : 1,
                "autoredeem" : True
            }

            with open("Assets/Settings/nitrosniper.json", "w") as f:
                json.dump(config, f, indent=4)

        if not os.path.exists("Assets/Settings/massreact.json"):
            config = {
                "emojis" : []
            }

            with open("Assets/Settings/massreact.json", "w") as f:
                json.dump(config, f, indent=4)

        if not os.path.exists("Assets/Presence.json"):
            config = {}

            with open("Assets/Presence.json", "w") as f:
                json.dump(config, f, indent=4)

        if not os.path.exists("Assets/Settings/webhook.json"):
            config = {
                "Author": "Invictus",
                "Color": 16711680
            }

            with open("Assets/Settings/webhook.json", "w") as f:
                json.dump(config, f, indent=4)

        if not os.path.exists("Assets/Settings/Cache.json"):
            config = {
                "Logons" : 1,
                "Uptime" : 0
            }

            with open("Assets/Settings/Cache.json", "w") as f:
                json.dump(config, f, indent=4)
        if not os.path.exists("Assets/Settings/footer.json"):
            config = {
                "Footer" : self.footer,
                "Linktext" : self.footlinktext,
                "Link" : self.footlink
            }

            with open("Assets/Settings/Footer.json", "w") as f:
                json.dump(config, f, indent=4)
        # Credits to nighty for the idea of custom themes
        if not os.path.exists("Assets/Settings/Style.json"):
            # Thx to ryz for this theme
            config = {
                "Demo" : {
                    "CMDStart": "> -# `",
                    "CMDEnd": "` ",
                    "CMDSplit": "»",
                    "ColumnStart" : "- ",
                    "ColumnEnd": " -",
                    "ColumnSplit": "|",
                    "Footer": "```Invictus SB```",
                    "Header": "```{}```",
                    "Align" : False
                }
            }

            with open("Assets/Settings/Style.json", "w") as f:
                json.dump(config, f, indent=4)

    def config(self):
        if not os.path.exists("Assets/Config.json"):
            self.general.clear()
            self.general.art()
            with open("Assets/Config.json", "w") as f:
                output_modes = ["codeblock", "table", "block"]
                print("[+] General Settings\n")

                token  = input("[>] User token     : ")
                prefix = input("[>] Command prefix : ")
                output = input("[>] Output mode    : ")
                while output not in output_modes:
                    print("[*] {}".format(", ".join(output_modes)))
                    output = input("[!] Invalid output mode. Try again: ")

                print("\n[+] Modules\n")

                customfooter = input("[>] Custom footer? : ")
                if customfooter.lower() == "y":
                    self.footer = input("[>] Enter footer: ")
                    self.footlink = input("[>] Enter footer link: ")
                    self.footlinktext = input("[>] Enter footer link text: ")

                nitro  = input("[>] Nitro sniper?  : ")
                msglog = input("[>] Log messages?  : ")
                tcrypt = input("[>] Encrypt token? : ")
                if tcrypt.lower() == "y":
                    tpass = input("[>] Enter encryption password: ")
                    token = self.general.tcrypt(token, tpass)
                givesniper = input("[>] GiveSniper?     : ")
                custompres = input("[>] Custom presence? : ")
                antitl = input("[>] Anti tokenlog? : ")
                autolo = input("[>] Auto logout?   : ")
                if autolo.lower() == "y":
                    userpass = input("[>] Enter account password: ") 
                    if tcrypt.lower() == "y":
                        userpass = self.general.tcrypt(userpass, tpass)

                print("\n[+] Keys\n")
                    
                gelkey   = input("[>] Enter gelbooru API key: ")
                if gelkey:
                    userid = input("[>] Enter gelbooru user ID: ")

                json.dump({"Token": token, 
                           "Prefix": prefix if prefix else ".", 
                           "Output": output.lower() if output else "block", 
                           "Modules": {"nitro": True if nitro.lower() == "y" else False, 
                                       "msglog": True if msglog.lower() == "y" else False, 
                                       "antitokenlog": True if antitl.lower() == "y" else False, 
                                       "autologout": True if autolo.lower() == "y" else False, 
                                       "givesniper": True if givesniper.lower() == "y" else False, 
                                       "custompresence": True if custompres.lower() == "y" else False,
                                       "customfooter": True if customfooter.lower() == "y" else False}, 
                            "Keys" : {"gelboorukey": gelkey if gelkey else None, 
                                      "gelbooruid": userid if gelkey else None}, 
                            "TCrypt": True if tcrypt.lower() == "y" else False, 
                            "Account": {"password": userpass} if autolo.lower() == "y" else {}
                        }, f, indent=4)
                if custompres.lower() == "y":
                    self.presinit()


                
    def presinit(self):
        print("\n[+] Custom presence\n")
        custompres = input("[>] Custom presence? : ")
        if custompres.lower() == "y":
            clientid = input("[>] Enter client ID: ")
            clientms = input("[>] Enter presence message: ")
            clientli = input("[>] Enter large image key: ")
            if clientli:
                clientlit = input("[>] Enter large image text: ")
            clientsi = input("[>] Enter small image key: ")
            if clientsi:
                clientsit = input("[>] Enter small image text: ")

            cb = input("[>] Buttons? : ")
            if cb.lower() == "y":
                buttons = []
                print("[*] Enter !q to quit buttons")
                clientbt = input("[>] Enter button label: ")
                clientbu = input("[>] Enter button url: ")
                while clientbt != "!q":
                    buttons.append({"label": clientbt, "url": clientbu})
                    clientbt = input("[>] Enter button label: ")
                    clientbu = input("[>] Enter button url: ")


        with open("Assets/Presence.json", "w") as f:
            presence_data = {
                "Presence": {
                    "Default" : {
                        "ClientID": clientid if custompres.lower() == "y" else "",
                        "State": clientms if custompres.lower() == "y" else "Invictus selfbot best",
                        "LargeImageKey": clientli if custompres.lower() == "y" else "",
                        "LargeImageText": clientlit if custompres.lower() == "y" else "",
                        "SmallImageKey": clientsi if custompres.lower() == "y" else "",
                        "SmallImageText": clientsit if custompres.lower() == "y" else "",
                        "Buttons" : buttons if cb.lower() == "y" else []
                    }
                }
            }
            json.dump(presence_data, f, indent=4)

    def initalizesql(self):
        if not os.path.exists("Databases"):
            os.mkdir("Databases")
        
        if not os.path.exists("Databases/messages.db"):
            conn = sqlite3.connect("Databases/messages.db")
            c = conn.cursor()
            c.execute("CREATE TABLE messages (userid TEXT, username TEXT, message TEXT, time TEXT)")
            conn.commit()
            conn.close()
        
        if not os.path.exists("Databases/deleted.db"):
            conn = sqlite3.connect("Databases/deleted.db")
            c = conn.cursor()
            c.execute("CREATE TABLE messages (userid TEXT, username TEXT, message TEXT, time TEXT)")
            conn.commit()
            conn.close()

    def sites(self):
        if not os.path.exists("Assets/Sites.json"):
            data = {
                "GitHub": {
                    "url": "https://www.github.com/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Twitter": {
                    "url": "https://twitter.com/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "LinkedIn": {
                    "url": "https://www.linkedin.com/in/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Wikipedia": {
                    "url": "https://en.wikipedia.org/wiki/User:{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Ogusers": {
                    "url": "https://ogusers.gg/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Tumblr": {
                    "url": "https://{}.tumblr.com/",
                    "type": "status-code",
                    "check-value": 200
                },
                "Vimeo": {
                    "url": "https://vimeo.com/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Spotify": {
                    "url": "https://open.spotify.com/user/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "SoundCloud": {
                    "url": "https://soundcloud.com/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "DeviantART": {
                    "url": "https://{}.deviantart.com",
                    "type": "status-code",
                    "check-value": 200
                },
                "MyAnimeList": {
                    "url": "https://myanimelist.net/profile/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "BitBucket": {
                    "url": "https://bitbucket.org/{}/",
                    "type": "status-code",
                    "check-value": 200
                },
                "Quora": {
                    "url": "https://www.quora.com/profile/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Dev.to": {
                    "url": "https://dev.to/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Slideshare": {
                    "url": "https://slideshare.net/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "SlideShare": {
                    "url": "https://slides.com/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "9GAG": {
                    "url": "https://www.9gag.com/u/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Archive of Our Own": {
                    "url": "https://archiveofourown.org/users/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "BuzzFeed": {
                    "url": "https://buzzfeed.com/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Dribbble": {
                    "url": "https://dribbble.com/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Etsy": {
                    "url": "https://www.etsy.com/shop/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "IMDb": {
                    "url": "https://www.imdb.com/user/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Kickstarter": {
                    "url": "https://www.kickstarter.com/profile/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Minecraft": {
                    "url": "https://api.mojang.com/users/profiles/minecraft/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Meetup": {
                    "url": "https://www.meetup.com/members/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Patreon": {
                    "url": "https://www.patreon.com/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Product Hunt": {
                    "url": "https://www.producthunt.com/@{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Shopify": {
                    "url": "https://{}.myshopify.com",
                    "type": "status-code",
                    "check-value": 200
                },
                "Stack Exchange": {
                    "url": "https://stackexchange.com/users/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Repl.it": {
                    "url": "https://replit.com/@{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Pika.net": {
                    "url": "https://pika-network.net/members/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Feds.lol": {
                    "url": "https://feds.lol/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Guns.lol": {
                    "url": "https://guns.lol/{}",
                    "type": "page-content",
                    "check-value": "This user is not claimed"
                },
                "Ez-bio": {
                    "url": "https://e-z.bio/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Hypixel.net": {
                    "url": "https://hypixel.net/members/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Pornhub users": {
                    "url": "https://www.pornhub.com/users/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "RedTube": {
                    "url": "https://www.redtube.com/users/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Chaturbate": {
                    "url": "https://chaturbate.com/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Snapchat": {
                    "url": "https://www.snapchat.com/add/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "8Tracks" : {
                    "url" : "https://8tracks.com/{}",
                    "type" : "site-content",
                    "check-value" : "This page has vanished"
                },
                "All my links" : {
                    "url" : "https://allmylinks.com/{}",
                    "type" : "title-content",
                    "check-value" : "Not Found"
                },
                "Soloto": {
                    "url": "https://solo.to/{}",
                    "type": "status-code",
                    "check-value": 200
                },
                "Onlymyspace" : {
                    "url" : "https://only-my.space/{}",
                    "type" : "status-code",
                    "check-value" : 200
                },
                "LinkTree" : {
                    "url" : "https://linktr.ee/{}",
                    "type" : "title-content",
                    "check-value" : "Page Not Found"
                },
                "Ezbio" : {
                    "url" : "https://e-z.bio/{}",
                    "type" : "site-content",
                    "check-value" : "Page not found"
                }
            }

            with open("Assets/Sites.json", "w") as f:
                json.dump(data, f, indent=4)

    def eventloggerinit(self):
        if not os.path.exists("Assets/Events.json"):
            with open("Assets/Events.json", "w") as f:
                jsondata = {
                    "Guild Join"  : {"status" : False, "name" : "Guild Join",  "webhooks" : []},
                    "Guild Leave" : {"status" : False, "name" : "Guild Leave", "webhooks" : []},
                    "Bans"        : {"status" : False, "name" : "Bans",        "webhooks" : []},
                    "Giveaways"   : {"status" : False, "name" : "Giveaways",   "webhooks" : []},
                    "Nitros"      : {"status" : False, "name" : "Nitros",      "webhooks" : []},
                    "Friends"     : {"status" : False, "name" : "Friends",     "webhooks" : []},
                }
                json.dump(jsondata, f, indent=4)

    def temp(self):
        if not os.path.exists("Assets/Temp"):
            os.mkdir("Assets/Temp")



    def init(self):
        self.config()
        self.assets()
        self.ipcache()
        self.msglogs()
        self.settings()
        self.scripts()
        self.scrapes()
        self.initalizesql()
        self.eventloggerinit()
        self.sites()
        self.temp()
