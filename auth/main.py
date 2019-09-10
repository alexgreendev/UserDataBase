from router import Router
from src.controllers.access_controller import AccessController
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

        AccessController(). \
            add_method("GET", 1). \
            add_method("PATCH", 2). \
            add_method("PUT", 3). \
            add_method("POST", 3). \
            add_method("DELETE", 3)

        http_server = Server(__name__).http
        Router(http_server)
        host, port = config.get_section("http_server").values()
        http_server.run(host, port)
    else:
        raise error


if __name__ == '__main__':
    main()
