import requests
from .settings import MODEL_SERVER_HOST, MODEL_SERVER_PORT


class ModelClient:
    host = MODEL_SERVER_HOST
    port = MODEL_SERVER_PORT

    @classmethod
    def submit_model_build(cls, params):
        url = "http://%s:%s" % (cls.host, cls.port)
        requests.post(url, json=params)
