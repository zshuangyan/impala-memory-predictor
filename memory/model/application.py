import tornado.web

from .url import url
from ..redis_client import RedisClient
from ..constants import ModelStatus, MODEL_STATUS


class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        RedisClient.set(MODEL_STATUS, ModelStatus.FINISHED)
        super(Application, self).__init__(*args, **kwargs)

application = Application(
    handlers=url,
    autoreload=True
)
