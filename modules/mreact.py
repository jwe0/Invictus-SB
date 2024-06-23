import tls_client, time
from modules.spoof import Spoof
from modules.logging import Logging
from modules.general import General

class MassReact:
    def __init__(self, token):
        self.token   = token
        self.setting = {}
        self.headers = {}
        self.spoof   = Spoof()
        self.logging = Logging()
        self.general = General()
        self.session = tls_client.Session()

    def send(self, channelid, messageid, emjoi, delay):
        reactapi = f"https://discord.com/api/v9/channels/{channelid}/messages/{messageid}/reactions/{emjoi}/@me"
        r = self.session.put(reactapi, headers=self.headers)
        if r.status_code == 429:
            time.sleep(r.json()["retry_after"] + 0.5)
        time.sleep(int(delay))
        

    def react(self, messageid, channelid, delay):
        for emoji in self.setting["emojis"]:
            self.send(channelid, messageid, emoji, delay)

    def init(self):
        self.setting = self.general.load_massreact_settings()
        self.headers = self.spoof.headers(self.token)