class AccessController:

    methods = dict()

    @classmethod
    def add_method(cls, name: str, level: int):
        cls.methods[name] = level
        return cls

    @classmethod
    def is_access_allow(cls, method: str, level: int):
        return method in cls.methods and cls.methods[method] <= level
