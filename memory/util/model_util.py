from functools import lru_cache
from sklearn.externals import joblib
import os
import logging
from ..model.settings import MODEL_DIR


def load_model(model_path):
    logging.info("loading model %s" % model_path)
    return joblib.load(model_path)


@lru_cache(maxsize=2)
def get_model(model_path):
    return load_model(model_path)


class ModelFactory:
    @staticmethod
    def get_model(model_name, use_cache=True):
        model_path = os.path.join(MODEL_DIR, model_name)
        if use_cache:
            return get_model(model_path)
        else:
            return load_model(model_path)

    @staticmethod
    def prepare_model():
        for model_name in os.listdir(MODEL_DIR):
            ModelFactory.get_model(model_name)