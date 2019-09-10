import asyncio
# import json
# import time

from aiohttp import ClientSession, client_exceptions
from asyncio import Semaphore, ensure_future, gather, run

# from merge_lists import merge_lists


# noinspection PyUnresolvedReferences
class MultipleAsyncRequests:

    def __new__(cls):
        cls.urls = []
        cls.semaphore = 10
        cls.http_ok = []
        return cls

    @classmethod
    def add_url(cls, url):
        cls.urls.append(url)
        return cls

    @classmethod
    def add_status_ok(cls, http_ok):
        cls.http_ok.append(http_ok)
        return cls

    @classmethod
    def set_connection_limit(cls, limit):
        asyncio.set_event_loop(asyncio.new_event_loop())
        cls.semaphore = Semaphore(limit)
        return cls

    @classmethod
    def request(cls) -> list:
        return run(cls.__scrape())

    @classmethod
    async def __scrape(cls):
        tasks = list()
        async with ClientSession() as session:
            for url in cls.urls:
                task = ensure_future(cls.__scrape_bounded(url, cls.semaphore, session))
                tasks.append(task)
            result = await gather(*tasks)
        return result

    @classmethod
    async def __scrape_bounded(cls, url, sem, session):
        async with sem:
            return await cls.__scrape_one(url, session)

    @classmethod
    async def __scrape_one(cls, url, session):
        try:
            async with session.get(url) as response:
                content = await response.read()
        except client_exceptions.ClientConnectorError:
            return None
        if response.status not in cls.http_ok:
            return None
        return content



# if __name__ == '__main__':
#     iter = 1000
#     while iter:
#         res = MultipleAsyncRequests(). \
#             add_url('http://localhost:7000/remote-servers/one.json'). \
#             add_url('http://localhost:7000/remote-servers/two.json'). \
#             add_url('http://localhost:7000/remote-servers/three.json'). \
#             add_status_ok(200). \
#             set_connection_limit(1000). \
#             request()
#         users_arrs = [json.loads(arr.decode()) for arr in res]
#         users = merge_lists(users_arrs)
#         print(sorted(users, key=lambda i: i['id']))
#         print(len(users))
#         iter -= 1
