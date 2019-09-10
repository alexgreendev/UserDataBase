from flask import Response, request

from src.controllers.config import Config
from src.controllers.main_controller import MainController


class Router:
    def __init__(self, server):
        base = Config().get_option("routes", "base")

        @server.route(f"{base}/auth/", methods=("GET",))
        def authentication():
            status, data = MainController.authentication(request)
            return Response(data, status=status, mimetype='application/json')

        @server.route(f"{base}/login/", methods=("POST",))
        def login():
            return Response(MainController.login(request), mimetype='application/json')