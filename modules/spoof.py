import random, base64, json
import tls_client

class Spoof:
    def __init__(self):
        self.session = tls_client.Session()
    def useragent(self):
        return random.choice(open("modules/Dependencies/agents.txt").read().splitlines())
    def cookies(self):
        api = "https://canary.discord.com/api/v9/experiments"
        r = self.session.get(api)
        dcfduid  = r.cookies.get("__dcfduid")
        sdcfduid = r.cookies.get("__sdcfduid")
        cfruid   = r.cookies.get("__cfruid")

        return dcfduid, sdcfduid, cfruid
    def xsuperuser(self, agent):
        os = random.choice(["Windows", "Mac OS X", "Linux", "iOS", "Android"])
        browser = random.choice(["Chrome", "Firefox", "Safari", "Edge", "Opera"])

        xsuper = {
            "os": os,
            "browser": browser,
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": agent,
            "browser_version": "116.0",
            "os_version": "10",
            "referrer": "https://e-z.bio/",
            "referring_domain": "e-z.bio",
            "referrer_current": "https://discord.com/",
            "referring_domain_current": "discord.com",
            "release_channel": "stable",
            "client_build_number": 288460,
            "client_event_source": "null",
            "design_id": 0
        }

        super = json.dumps(xsuper)
        return base64.b64encode(super.encode()).decode()

        
    def headers(self, token):
        agent = self.useragent()
        xsuper = self.xsuperuser(agent)
        dcfduid, sdcfduid, cfruid = self.cookies()
        headers = {
            "Host": "discord.com",
            "User-Agent": agent,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Authorization": token,
            "X-Super-Properties": xsuper,
            "X-Discord-Locale": "en-US",
            "X-Discord-Timezone": "Europe/London",
            "X-Debug-Options": "bugReporterEnabled",
            "DNT": "1",
            "Alt-Used": "discord.com",
            "Connection": "keep-alive",
            "Cookie": f"__dcfduid={dcfduid}; __sdcfduid={sdcfduid}; __cfruid={cfruid}; locale=en-US",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers"
        }

        return headers
