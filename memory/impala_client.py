import logging

from impala.dbapi import connect
from functools import lru_cache
from .settings import ImpalaConstants
from .error import ImpalaConnectError, ImpalaQueryError


class ImpalaWrapper:
    def __init__(self, host=ImpalaConstants.HOST, port=ImpalaConstants.PORT,
                 user=ImpalaConstants.USER, database=None, sql=None,
                 auth_required=ImpalaConstants.AUTH_REQUIRED):
        self.host = host
        self.port = int(port)
        self.user = user
        self.database = database
        self.sql = "explain %s" % sql
        self.auth_required = auth_required

    @lru_cache(maxsize=2)
    def cursor(self):
        if self.auth_required:
            auth_mechanism = 'GSSAPI'
        else:
            auth_mechanism = 'NOSASL'
        cursor = connect(self.host, self.port,
                         auth_mechanism=auth_mechanism).cursor()
        try:
            cursor.execute("use %s" % self.database)
            cursor.execute("set explain_level=2")
        except Exception as err:
            logging.warning(err)
            raise ImpalaQueryError(message=str(err))
        return cursor

    def explain(self):
        try:
            cursor = self.cursor()
        except Exception as err:
            logging.error(err)
            raise ImpalaConnectError(message=str(err))

        try:
            cursor.execute("use %s" % self.database)
            cursor.execute("set explain_level=2")
            cursor.execute(self.sql)
        except Exception as err:
            logging.warning(err)
            raise ImpalaQueryError(message=str(err))
        else:
            for line in cursor:
                yield line[0]
        finally:
            cursor.close()


