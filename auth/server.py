from flask import Flask


class Server:
    def __init__(self, name):
        self.http = Flask(name)
