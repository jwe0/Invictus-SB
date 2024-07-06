import socket, time, threading, random, requests, json
from modules.spoof import Spoof

class Dos:
    def __init__(self):
        self.spoof = Spoof()
        self.headers = {}

    def tcp(self, target, port, thread, delay, duration):
        ""
    def udp(self, target, port, thread, delay, duration):
        ""
    def syn(self, target, port, thread, delay, duration):
        ""
    def post(self, target, port, thread, delay, duration):
        ""
    def get(self, target, port, thread, delay, duration):
        ""
    def patch(self, target, port, thread, delay, duration):
        ""
    def delete(self, target, port, thread, delay, duration):
        ""

    def init(self):
        self.headers["User-Agent"] = self.spoof.useragent()