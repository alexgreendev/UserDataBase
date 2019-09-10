from flask import Response, request

from src.controllers.config import Config
from src.controllers.main_controller import MainController


class Router:
    def __init__(self, server):
        base = Config().get_option("routes", "base")

        @server.route(f"{base}/users/", methods=("GET",))
        def get_users():
            return Response(MainController.get_users(), mimetype='application/json')

        @server.route(f"{base}/users/<user_id>", methods=("PATCH",))
        def edit_user(user_id):
            return Response(MainController.edit_user(request, user_id), mimetype='application/json')

        @server.route(f"{base}/users/<user_id>", methods=("PUT",))
        def update_user(user_id):
            return Response(MainController.update_user(request, user_id), mimetype='application/json')

        @server.route(f"{base}/users/", methods=("POST",))
        def create_user():
            return Response(MainController.create_user(request), mimetype='application/json')

        @server.route(f"{base}/users/<user_id>", methods=("DELETE",))
        def delete_user(user_id):
            return Response(MainController.delete_user(user_id), mimetype='application/json')

        @server.route(f"{base}/users/remote/", methods=("GET",))
        def get_remote_users():
            return Response(MainController.get_remote_users(), mimetype='application/json')
