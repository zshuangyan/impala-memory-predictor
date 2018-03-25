import os

from .log_settings import LOGGING

__all__ = ["VERSION", "DATE_FORMAT", "NEED_CERTIFICATE", "KEYTAB_PATH",
           "PRINCIPAL", "ImpalaConstants", "RedisConstants",
           "MODEL_SERVER_PORT", "LOGGING"]
VERSION = "1.0"
DATE_FORMAT = "%Y%m%d"
NEED_CERTIFICATE = True

KEYTAB_PATH = os.path.join(os.path.expanduser("~"), 'dataengineering.keytab')
PRINCIPAL = "dataengineering"


class ImpalaConstants:
    AUTH_REQUIRED = True
    HOST = 'gs-server-1001'
    PORT = 21050
    USER = 'dataengineering'
    VERSION = "2.9.0-cdh5.12.1"


class RedisConstants:
    HOST = 'localhost'
    PORT = 6379

SERVER_PORT = 8889
MODEL_SERVER_HOST = "localhost"
MODEL_SERVER_PORT = 8888