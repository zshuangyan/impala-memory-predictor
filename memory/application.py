import tornado.web

from .url import url
from .redis_client import RedisClient
from .constants import ModelStatus, MODEL_STATUS
from .util import ModelFactory


class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        self.models = ModelFactory.prepare_model()
        RedisClient.set(MODEL_STATUS, ModelStatus.FINISHED)
        super(Application, self).__init__(*args, **kwargs)

application = Application(
    handlers=url,
    autoreload=True
)
