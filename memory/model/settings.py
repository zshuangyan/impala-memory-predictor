import os
from ..settings import (DATE_FORMAT, VERSION, KEYTAB_PATH, PRINCIPAL,
                        MODEL_SERVER_PORT, ImpalaConstants, NEED_CERTIFICATE)
from .log_settings import LOGGING

__all__ = ["VERSION", "KEYTAB_PATH", "PRINCIPAL", "DATE_FORMAT", "BASE_PATH",
           "MODEL_DIR", "FEATURE_FILE", "RESULT_FILE", "HDFS", "SparkSubmit",
           "LOGGING", "MODEL_SERVER_PORT", "IMPALA_VERSION", "NEED_CERTIFICATE"]

BASE_PATH = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_PATH, "model_dir")
FEATURE_FILE = os.path.join(BASE_PATH, "feature.csv")
RESULT_FILE = os.path.join(BASE_PATH, "result.csv")
IMPALA_VERSION = ImpalaConstants.VERSION


class HDFS:
    FILE_PATTERN = "part-*"
    THREAD_NUM = 10
    LOCAL_PATH = os.path.join(BASE_PATH, "temp_dir")
    REMOTE_PATH = "/user/dataengineering/GDP_query_coordinator/memory/feature/data/"
    NODES = ['http://gs-server-1046:50070', 'http://gs-server-1047:50070']


class SparkSubmit:
    LOCAL = False
    PREFIX = "spark-submit"
    APP = "feature-engineering.jar"
    SPARK_SUBMIT_PARAMS = {
        'class': "com.gridsum.de.impala.Features",
        'master': 'yarn',
        'driver-memory': "10g",
        'executor-memory': "20g",
        "num-executors": 20,
        "executor-cores": 3,
    }