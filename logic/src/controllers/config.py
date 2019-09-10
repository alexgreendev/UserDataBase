import configparser


class Config:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
            cls.__path = "config.ini"
            cls.__config = configparser.ConfigParser()

            cls.__config.add_section("data_base")
            cls.__config.set("data_base", "type", "mysql")
            cls.__config.set("data_base", "driver", "mysqldb")
            cls.__config.set("data_base", "user", "root")
            cls.__config.set("data_base", "password", "")
            cls.__config.set("data_base", "host", "database")
            cls.__config.set("data_base", "port", "3306")
            cls.__config.set("data_base", "db_name", "users")

            cls.__config.add_section("http_server")
            cls.__config.set("http_server", "host", "0.0.0.0")
            cls.__config.set("http_server", "port", "7000")

            cls.__config.add_section("routes")
            cls.__config.set("routes", "base", "/api/v1")

            cls.__config.add_section("remote_servers")
            cls.__config.set("remote_servers", "one", "http://front/remote-servers/one.json")
            cls.__config.set("remote_servers", "two", "http://front/remote-servers/two.json")
            cls.__config.set("remote_servers", "three", "http://front/remote-servers/three.json")

            with open(cls.__path, "w") as config_file:
                cls.__config.write(config_file)

        return cls.instance

    def get_section(self, section):
        return dict(self.__config.items(section))

    def get_option(self, section, option):
        return self.__config.get(section, option)
