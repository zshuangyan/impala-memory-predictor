from tornado import gen
from datetime import datetime
from tornado.escape import json_decode
from json import JSONDecodeError
import logging

from .base_handler import BaseHandler
from .error import ParameterError, ErrorCode
from .response import ModelBuildResponse, ModelStatusResponse
from .settings import DATE_FORMAT
from .constants import ModelStatus, MODEL_STATUS
from .redis_client import RedisClient
from .model_client import ModelClient


def validate(date):
    datetime.strptime(str(date), DATE_FORMAT)


class ModelBaseHandler(BaseHandler):
    @property
    def model_status(self):
        return RedisClient.get(MODEL_STATUS)

    @model_status.setter
    def model_status(self, value):
        RedisClient.set(MODEL_STATUS, value)


class ModelBuildHandler(ModelBaseHandler):
    @gen.coroutine
    def prepare(self):
        try:
            self.data = json_decode(self.request.body)
        except JSONDecodeError:
            raise ParameterError("request.body is not json format")
        try:
            validate(self.data['start_day'])
            validate(self.data['end_day'])
        except (KeyError, ValueError, TypeError) as err:
            raise ParameterError(str(err))

    """
    @api {post} /impala/memory/model_build 模型构建
    @apiName MemoryModel
    @apiDescription 构建内存预测的模型
    @apiParam {string} start_day 提取特征开始日期
    @apiParam {string} end_day 提取特征结束日期
    @apiParam {bool} [generate_feature] 是否生成特征文件，可选参数
    @apiParam {bool} [generate_report] 是否生成交叉验证结果，可选参数
    @apiParamExample Example Usage:
        endpoint http://gdpquerycoordinator.internal.gridsumdissector.com/v1/impala/memory/model

        body:
            {
                "start_day": "20180101",
                "end_day" : "20180121"
            }
    @apiSuccess {int} message 是否开始训练的信息
    @apiSuccess {int} error_code 若成功开始训练，则error_code=0，否则error_code=6
    @apiSuccessExample {json} Success-Response
        HTTP/1.1 200
        {
            "message": "Start building models"
            "error_code": 0
        }
    """
    @gen.coroutine
    def post(self):
        if self.model_status == ModelStatus.RUNNING:
            message = "Models are being built now, try after some time"
            self.write(ModelBuildResponse(error_code=ErrorCode.FAILURE,
                       message=message).get_response())
        else:
            self.model_status = ModelStatus.RUNNING
            self.write(ModelBuildResponse(error_code=ErrorCode.SUCCESS,
                       message="Start building models").get_response())
            self.finish()
            try:
                ModelClient.submit_model_build(self.data)
            except Exception as err:
                logging.exception(err)
                self.model_status = ModelStatus.FAILED


class ModelStatusHandler(ModelBaseHandler):
    @gen.coroutine
    def get(self):
        self.write(ModelStatusResponse(status_code=self.model_status,
                   status_str=self.model_status.phrase).get_response())