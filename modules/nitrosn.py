import time, tls_client
from modules.spoof import Spoof
from modules.logging import Logging
from modules.general import General

class NitroSniper:
    def __init__(self, token) -> None:
        self.token   = token
        self.logging = Logging()
        self.spoof   = Spoof()
        self.general = General()
        self.session = tls_client.Session()
        self.setting = {}

    def redeem(self, codeid):
        api = f"https://discord.com/api/v9/entitlements/gift-codes/{codeid}/redeem"
        headers = self.spoof.headers(self.token)
        r = self.session.post(api, headers=headers)
        if r.status_code == 200:
            self.logging.Info(f"Redeemed nitro code: {codeid}")
        else:
            self.logging.Error(f"Failed to redeem nitro code: {codeid}")


    def detect(self, message):
        if "discord.gift/" in message.content:
            codeid = message.content.split("/")[-1]
            if len(codeid) >= 16:
                self.logging.Info(f"Found nitro code: {codeid}")
            time.sleep(self.setting["delay"])
            if self.setting["autoredeem"]:
                self.redeem(codeid)

    def init(self):
        self.setting = self.general.load_nitrosniper_settings()

