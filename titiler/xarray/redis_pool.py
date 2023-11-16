import os

import fakeredis
import redis  # type: ignore

from titiler.xarray.settings import ApiSettings

api_settings = ApiSettings()


class RedisCache:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = redis.ConnectionPool(
                host=api_settings.cache_host, port=6379, db=0
            )
        return cls._instance


def get_redis():
    if os.getenv("TEST_ENVIRONMENT"):
        server = fakeredis.FakeServer()
        # Use fakeredis in a test environment
        return fakeredis.FakeRedis(server=server)

    # Here, we re-use our connection pool
    # not creating a new one
    pool = RedisCache.get_instance()
    return redis.Redis(connection_pool=pool)
