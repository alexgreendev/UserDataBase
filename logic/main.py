from router import Router
from src.controllers.config import Config
from server import Server
from src.controllers.db import DB
from src.models.users import Users


def main():
    config = Config()
    db = DB()
    error, engine = db.connect(**config.get_section("data_base"))

    if not error:
        Users.init_model(db.metadata)
        db.metadata.create_all(engine)

        session = db.session
        new_user = Users(name="admin", password="password", access_level=3)
        session.add(new_user)
        session.commit()
        
        http_server = Server(__name__).http
        Router(http_server)
        host, port = config.get_section("http_server").values()
        http_server.run(host, port)
    else:
        raise error


if __name__ == '__main__':
    main()
