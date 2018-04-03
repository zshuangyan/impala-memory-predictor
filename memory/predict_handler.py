from tornado import gen
from http import HTTPStatus

from .predict import get_model, predict
from .error import ErrorCode, MemError, UnKnownError
from .feature import get_features
from .impala_client import ImpalaWrapper
from .response import PredictSuccessResponse
from .util import json_validate
from .base_handler import BaseHandler
from .settings import ImpalaConstants
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor

MEMORY_PREDICT = {
    'type': 'object',
    'properties': {
        'sql': {
            'type': 'string',
            'minLength': 1
        },
        'db': {
            'type': 'string',
            'minLength': 1
        },
        'pool': {'type': 'string'},
    },
    'required': ['sql', 'db']
}


class MemoryPredictHandler(BaseHandler):
    executor = ThreadPoolExecutor()

    """
    @api {post} /impala/memory/predict 预测内存
    @apiName MemoryPredict
    @apiDescription SQL查询内存限制预测
    @apiParam {string} sql 待预测的sql
    @apiParam {string} pool 执行查询的池子
    @apiParamExample Example Usage:
        endpoint http://gdpquerycoordinator.internal.gridsumdissector.com/v1/impala/memory/predict

        body:
            {
                "sql": "select memory_per_node_peak from impala_query_info",
                "pool" : "Prophet",
            }
    @apiSuccess {int} memory_limit 预测出的内存大小
    @apiSuccess {int} error_code 错误码
    @apiSuccessExample {json} Success-Response
        HTTP/1.1 200
        {
            "memory_limit": 5000
            "error_code": 0
        }

    @apiError {string} message 错误信息
    @apiError {int} error_code 错误码
    """
    @gen.coroutine
    @json_validate(MEMORY_PREDICT, ErrorCode.PARAMETER_ERROR)
    def post(self):
        sql = self.data.get('sql')
        db = self.data.get('db')
        pool = self.data.get('pool', 'default')
        pool = "root." + pool if not pool.startswith("root") else pool
        try:
            explain_result = yield self.get_explain_result(db, sql) 
            features = get_features(explain_result, ImpalaConstants.VERSION)
            model = get_model(pool)
            result = predict(model, features)
        except MemError as err:
            self.send_error(status_code=err.status_code,
                            error_message=err.get_error_body())
        except Exception as err:
            unknown_err = UnKnownError(message=str(err))
            self.send_error(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            error_message=unknown_err.get_error_body())
        else:
            self.write(PredictSuccessResponse(result).get_response())

    @run_on_executor
    def get_explain_result(self, db, sql):
        return ImpalaWrapper(database=db, sql=sql).explain()
