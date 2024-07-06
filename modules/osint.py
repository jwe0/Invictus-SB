import requests, json, threading
from bs4 import BeautifulSoup
from modules.spoof import Spoof



class OSINT:
    def __init__(self):
        self.spoof = Spoof()
        self.links = {}
        self.heads = {}
        
        self.total = 0
        self.currt = 0

    def usernameosint(self, username):
        results = []
        def check(url, type, code):
            r = requests.get(url, headers=self.heads)
            try:
                if type == "status-code":
                    if r.status_code == int(code):
                        results.append(url)
                elif type == "site-content":
                    soup = BeautifulSoup(r.text, "html.parser")
                    if code in soup.text:
                        results.append(url)
                elif type == "title-content":
                    soup = BeautifulSoup(r.text, "html.parser")
                    title = soup.find("title").text
                    if code in title:
                        results.append(url)
            except:
                pass
            self.currt += 1
            
        self.total = len(self.links) - 1

        for site in self.links:
            url  = self.links[site]["url"].format(username)
            type = self.links[site]["type"]
            code = self.links[site]["check-value"]
            threading.Thread(target=check, args=(url, type, code)).start()

        while self.currt != self.total:
            pass

        self.currt = 0
        self.total = 0
        return results
        
        

    def makeheaders(self):
        self.heads["User-Agent"] = self.spoof.useragent()

    def init(self):
        with open("Assets/Sites.json", "r") as f:
            self.links = json.load(f)