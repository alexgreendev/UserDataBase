import json
import sys
import traceback

from src.controllers.config import Config
from src.controllers.db import DB

from src.libs.merge_lists import merge_lists
from src.libs.multiple_async_requests import MultipleAsyncRequests
from src.models.users import Users

db = DB()
remote_servers = Config().get_section("remote_servers")


class MainController:

    @staticmethod
    def get_users():
        session = db.session
        try:
            users_models = session.query(Users).all()
            users = [dict(id=user.id, name=user.name, access_level=user.access_level) for user in users_models]
            response = dict(success=True, users=users)
            return json.dumps(response)
        except Exception as error:
            session.rollback()
            traceback.print_exc(file=sys.stdout)
            return json.dumps(dict(success=False))

    @staticmethod
    def edit_user(request, user_id):
        data = request.json
        try:
            response = dict(success=False)
            name = data["name"]
            if name:
                session = db.session
                user = session.query(Users).filter(Users.id == user_id).scalar()
                has_name = session.query(Users).filter(Users.name == name).scalar()
                if user and not has_name:
                    db.conn.execute(f"UPDATE users SET name='{name}' WHERE id='{user_id}' LIMIT 1")
                    session.commit()
                    response = dict(success=True)
            return json.dumps(response)
        except Exception as error:
            session.rollback()
            traceback.print_exc(file=sys.stdout)
            return json.dumps(dict(success=False))

    @staticmethod
    def update_user(request, user_id):
        data = request.json
        try:
            response = dict(success=False)
            name, access_level = data["name"]
            if name and access_level:
                session = db.session
                user = session.query(Users).filter(Users.id == user_id).scalar()
                has_name = session.query(Users).filter(Users.name == name).scalar()
                if user and not has_name:
                    db.conn.execute(
                        f"UPDATE users SET name='{name}', access_level='{access_level}' WHERE id='{user_id}' LIMIT 1")
                    session.commit()
                    response = dict(success=True)
            return json.dumps(response)
        except Exception as error:
            session.rollback()
            traceback.print_exc(file=sys.stdout)
            return json.dumps(dict(success=False))

    @staticmethod
    def create_user(request):
        data = request.json
        try:
            name, password, access_level = data["name"], data["password"], data["access_level"]
            session = db.session

            response = dict(success=False)
            user = session.query(Users).filter(Users.name == name).scalar()
            if user is None:
                new_user = Users(name=name, password=password, access_level=access_level)
                session.add(new_user)
                session.commit()
                response = dict(success=True, user=dict(name=name, access_level=access_level))
            return json.dumps(response)
        except Exception as error:
            session.rollback()
            traceback.print_exc(file=sys.stdout)
            return json.dumps(dict(success=False))

    @staticmethod
    def delete_user(user_id):
        session = DB().session
        try:
            response = dict(success=False)
            user = session.query(Users).filter(Users.id == user_id).scalar()
            if user:
                db.conn.execute(f"DELETE FROM users WHERE id='{user_id}' LIMIT 1")
                session.commit()
                response = dict(success=True)
            return json.dumps(response)
        except Exception as error:
            session.rollback()
            traceback.print_exc(file=sys.stdout)
            return json.dumps(dict(success=False))

    @staticmethod
    def get_remote_users():
        try:
            bytes_list = MultipleAsyncRequests(). \
                add_url(remote_servers["one"]). \
                add_url(remote_servers["two"]). \
                add_url(remote_servers["three"]). \
                add_status_ok(200). \
                set_connection_limit(1000). \
                request()
            users_lists = [json.loads(arr.decode()) for arr in bytes_list]
            users = sorted(merge_lists(users_lists), key=lambda i: i['id'])
            return json.dumps(dict(success=True, users=users))
        except Exception as error:
            traceback.print_exc(file=sys.stdout)
            return json.dumps(dict(success=False))
