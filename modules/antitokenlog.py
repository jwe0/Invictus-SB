import tls_client, json, time
from modules.spoof import Spoof
from modules.logging import Logging

class AntiTokenLog:
    def __init__(self, token, autologout, userpass):
        self.token    = token
        self.headers  = Spoof().headers(token)
        self.session  = tls_client.Session()
        self.logging  = Logging() 
        self.userpass = userpass
        self.autolo   = autologout
        self.current  = None
        self.currhash = None
        self.used     = []
    

    def getsessions(self):
        hashes = []
        api = "https://discord.com/api/v9/auth/sessions"

        r = self.session.get(api, headers=self.headers)

        for session in r.json().get("user_sessions"):
            hashes.append(session)

        return hashes
    
    def getclient(self):
        hashes = self.getsessions()
        self.current = max(hashes, key=lambda x: x["approx_last_used_time"])
        self.currhash = self.current["id_hash"]

    def logout(self, hash):
        outapi = "https://discord.com/api/v9/auth/sessions/logout"
        data = {"session_id_hashes" : [hash]}
        mfaapi = self.session.post(outapi, headers=self.headers, json=data)

        ticket = mfaapi.json().get("mfa", "").get("ticket")

        finishapi = "https://discord.com/api/v9/mfa/finish"
        data = {"data" : self.userpass, "mfa_type" : "password", "ticket" : ticket}

        finapi = self.session.post(finishapi, headers=self.headers, json=data)

        token = finapi.json().get("token")

        #X-Discord-MFA-Authorization

        nheaders = self.headers
        nheaders["X-Discord-MFA-Authorization"] = token
        data = {"session_id_hashes" : [hash]}

        final = self.session.post(outapi, headers=nheaders, json=data)

        if final.status_code == 200:
            self.logging.Success("[>] Logged out successfully!")


    def getrecent(self):
        def get():
            hashes = self.getsessions()
            currhash = max(hashes, key=lambda x: x["approx_last_used_time"])
            return currhash
            
        while True:
            r = get()
            if self.currhash != r["id_hash"] and r["id_hash"] not in self.used:
                self.logging.Info("[>] New location logged in: {} : {}".format(r["client_info"]["location"], r["client_info"]["os"] + " " + r["client_info"]["platform"]))
                if self.autolo:
                    self.logging.Info("[>] Logging out!")
                    self.logout(r["id_hash"])
                self.used.append(r["id_hash"]) 
            time.sleep(30)



