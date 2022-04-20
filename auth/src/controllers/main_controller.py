import datetime
import hashlib
import json
import sys
import traceback
from base64 import b64encode
from inspect import getmembers
from pprint import pprint

import jwt

from src.controllers.access_controller import AccessController
from src.controllers.config import Config
from src.controllers.db import DB
from src.models.users import Users

config = Config()
db = DB()


class MainController:

    @staticmethod
    def authentication(request):
        try:
            token = request.headers.get('authorization')
            secret = config.get_option("jwt", "secret")
            res = jwt.decode(token.encode(), secret, algorithms=['HS256'])
            req_method = request.headers.get("X-Original-Method")
            access_level = int(res["access_level"])
            if AccessController.is_access_allow(req_method, access_level):
                response = dict(success=True)
                return 200, json.dumps(response)
            return 403, json.dumps(dict(success=False))
        except Exception as error:
            traceback.print_exc(file=sys.stdout)
            return 401, json.dumps(dict(success=False))

    @staticmethod
    def login(request):
        data = request.json
        session = db.session
        try:
            name, password = data["name"], data["password"]
            response = dict(success=False)
            user = session.query(Users).filter(Users.name == name).scalar()
            hash_pass = hashlib.sha256(str(password).encode('utf-8')).hexdigest()
            if user and hash_pass == user.password:
                secret = config.get_option("jwt", "secret")
                expire = config.get_option("jwt", "expire")
                token = jwt.encode({
                    'id': user.id,
                    'access_level': user.access_level,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(expire))
                }, secret, algorithm='HS256')
                response = dict(success=True,
                                user=dict(name=user.name, access_level=user.access_level, token=token))
            session.commit()
            return json.dumps(response)
        except Exception as error:
            session.rollback()
            traceback.print_exc(file=sys.stdout)
            return json.dumps(dict(success=False))
