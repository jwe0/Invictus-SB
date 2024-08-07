import json
import time
import threading
import websocket

# Credits go to nrxlvyy for this module. Thanks bro.


class Utils:
    @staticmethod
    def rangeCorrector(ranges):
        if [0, 99] not in ranges:
            ranges.insert(0, [0, 99])
        return ranges

    @staticmethod
    def getRanges(index, multiplier, memberCount):
        initialNum = int(index * multiplier)
        rangesList = [[initialNum, initialNum + 99]]
        if memberCount > initialNum + 99:
            rangesList.append([initialNum + 100, initialNum + 199])
        return Utils.rangeCorrector(rangesList)

    @staticmethod
    def parseGuildMemberListUpdate(response):
        memberdata = {
            "guild_id": response["d"]["guild_id"],
            "types": [],
            "locations": [],
            "updates": []
        }

        for chunk in response['d']['ops']:
            memberdata['types'].append(chunk['op'])
            if chunk['op'] in ('SYNC', 'INVALIDATE'):
                memberdata['locations'].append(chunk['range'])
                if chunk['op'] == 'SYNC':
                    memberdata['updates'].append(chunk['items'])
                else:
                    memberdata['updates'].append([])
            elif chunk['op'] in ('INSERT', 'UPDATE', 'DELETE'):
                memberdata['locations'].append(chunk['index'])
                if chunk['op'] == 'DELETE':
                    memberdata['updates'].append([])
                else:
                    memberdata['updates'].append(chunk['item'])

        return memberdata

class DiscordSocket(websocket.WebSocketApp):
    def __init__(self, token, guild_id, channel_id):
        self.token = token
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.socket_headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
        }

        super().__init__("wss://gateway.discord.gg/?encoding=json&v=9",
                         header=self.socket_headers,
                         on_open=self.sock_open,
                         on_message=self.sock_message,
                         on_close=self.sock_close
                         )

        self.endScraping = False

        self.guilds = {}
        self.members = set()

        self.ranges = [[0, 0]]
        self.lastRange = 0
        self.packets_recv = 0

    def run(self):
        self.run_forever()
        return list(self.members)

    def scrapeUsers(self):
        if not self.endScraping:
            payload = {
                "op": 14,
                "d": {
                    "guild_id": self.guild_id,
                    "typing": True,
                    "activities": True,
                    "threads": True,
                    "channels": {
                        self.channel_id: self.ranges
                    }
                }
            }
            self.send(json.dumps(payload))

    def sock_open(self, ws):
        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "capabilities": 125,
                "properties": {
                    "os": "Windows",
                    "browser": "Firefox",
                    "device": "",
                    "system_locale": "it-IT",
                    "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
                    "browser_version": "94.0",
                    "os_version": "10",
                    "referrer": "",
                    "referring_domain": "",
                    "referrer_current": "",
                    "referring_domain_current": "",
                    "release_channel": "stable",
                    "client_build_number": 103981,
                    "client_event_source": None
                },
                "presence": {
                    "status": "online",
                    "since": 0,
                    "activities": [],
                    "afk": False
                },
                "compress": False,
                "client_state": {
                    "guild_hashes": {},
                    "highest_last_message_id": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1,
                    "user_settings_version": -1
                }
            }
        }
        self.send(json.dumps(payload))

    def heartbeatThread(self, interval):
        try:
            while not self.endScraping:
                self.send(json.dumps({"op": 1, "d": self.packets_recv}))
                time.sleep(interval)
        except Exception as e:
            print(f"Heartbeat thread error: {e}")

    def sock_message(self, ws, message):
        decoded = json.loads(message)

        if decoded is None:
            return

        if decoded["op"] != 11:
            self.packets_recv += 1

        if decoded["op"] == 10:
            threading.Thread(target=self.heartbeatThread, args=(
                decoded["d"]["heartbeat_interval"] / 1000, ), daemon=True).start()

        if decoded["t"] == "READY":
            for guild in decoded["d"]["guilds"]:
                self.guilds[guild["id"]] = {"member_count": guild["member_count"]}

        if decoded["t"] == "READY_SUPPLEMENTAL":
            self.ranges = Utils.getRanges(0, 100, self.guilds[self.guild_id]["member_count"])
            self.scrapeUsers()

        elif decoded["t"] == "GUILD_MEMBER_LIST_UPDATE":
            parsed = Utils.parseGuildMemberListUpdate(decoded)

            if parsed['guild_id'] == self.guild_id and ('SYNC' in parsed['types'] or 'UPDATE' in parsed['types']):
                for elem, index in enumerate(parsed["types"]):
                    if index == "SYNC":
                        if len(parsed['updates'][elem]) == 0:
                            self.endScraping = True
                            break

                        for item in parsed["updates"][elem]:
                            if "member" in item:
                                mem = item["member"]
                                if not mem["user"].get("bot"):
                                    self.members.add(mem["user"]["id"])

                    elif index == "UPDATE":
                        for item in parsed["updates"][elem]:
                            if "member" in item:
                                mem = item["member"]
                                if not mem["user"].get("bot"):
                                    self.members.add(mem["user"]["id"])

                    self.lastRange += 1
                    self.ranges = Utils.getRanges(self.lastRange, 100, self.guilds[self.guild_id]["member_count"])
                    time.sleep(0.45)
                    self.scrapeUsers()

            if self.endScraping:
                self.close()

    def sock_close(self, ws, close_code, close_msg):
        pass