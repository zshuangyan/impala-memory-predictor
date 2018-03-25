from redis import StrictRedis
import pickle
from .settings import RedisConstants


class RedisClient:
    _redis_client = StrictRedis(RedisConstants.HOST, RedisConstants.PORT)

    @classmethod
    def get(cls, name):
        return pickle.loads(cls._redis_client.get(name))

    @classmethod
    def set(cls, name, value):
        cls._redis_client.set(name, pickle.dumps(value))


