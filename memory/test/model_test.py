import unittest
import os
import shutil
from .constants import UrlConstants
from .common import ToolBoxAPIWrapper
from ..error import ErrorCode
from ..model import constants, settings
from ..constants import ModelStatus, MODEL_STATUS
from ..redis_client import RedisClient

start_day = '20180101'
end_day = '20180103'


def check_model_exists():
    """check models specified in model.constants all exist"""
    for g in constants.MODEL_GROUP:
        model_path = os.path.join(settings.MODEL_DIR, g['name'])
        if not os.path.exists(model_path):
            return False
    return True


def remove_models():
    """clear all models in model dir"""
    if os.path.exists(settings.MODEL_DIR):
        shutil.rmtree(settings.MODEL_DIR)


class ModelTest(unittest.TestCase):
    def test_model_build_should_not_ok_when_no_start_day(self):
        params = {
            'end_day': end_day
        }
        status_code, json_data = ToolBoxAPIWrapper.query_memory(
            UrlConstants.MEMORY_MODEL_BUILD_TEMPLATE, params)
        self.assertTrue(status_code == 400)
        self.assertTrue(json_data['error_code'] == ErrorCode.PARAMETER_ERROR)

    def test_model_build_should_not_ok_when_no_end_day(self):
        params = {
            'start_day': start_day
        }
        status_code, json_data = ToolBoxAPIWrapper.query_memory(
            UrlConstants.MEMORY_MODEL_BUILD_TEMPLATE, params)
        self.assertTrue(status_code == 400)
        self.assertTrue(json_data['error_code'] == ErrorCode.PARAMETER_ERROR)

    def test_model_build_should_not_ok_when_day_format_wrong(self):
        params = {
            'start_day': "2018-01-01",
            'end_day': "2018-01-03"
        }
        status_code, json_data = ToolBoxAPIWrapper.query_memory(
            UrlConstants.MEMORY_MODEL_BUILD_TEMPLATE, params)
        self.assertTrue(status_code == 400)
        self.assertTrue(json_data['error_code'] == ErrorCode.PARAMETER_ERROR)

    def test_model_build_should_not_ok_when_current_model_status_is_running(self):
        params = {
            'start_day': start_day,
            'end_day': end_day
        }
        RedisClient.set(MODEL_STATUS, ModelStatus.RUNNING)
        status_code, josn_data = ToolBoxAPIWrapper.query_memory(
            UrlConstants.MEMORY_MODEL_BUILD_TEMPLATE, params)
        self.assertTrue(status_code == 200)
        self.assertTrue(josn_data['error_code'] == ErrorCode.FAILURE)

    def test_model_build_should_ok_when_current_model_status_is_finished(self):
        params = {
            'start_day': start_day,
            'end_day': end_day
        }
        RedisClient.set(MODEL_STATUS, ModelStatus.FINISHED)
        status_code, json_data = ToolBoxAPIWrapper.query_memory(
            UrlConstants.MEMORY_MODEL_BUILD_TEMPLATE, params)
        self.assertTrue(status_code == 200)
        self.assertTrue(json_data['error_code'] == ErrorCode.SUCCESS)

    def test_model_build_should_ok_when_current_model_status_is_failed(self):
        params = {
            'start_day': start_day,
            'end_day': end_day
        }
        RedisClient.set(MODEL_STATUS, ModelStatus.FINISHED)
        status_code, json_data = ToolBoxAPIWrapper.query_memory(
            UrlConstants.MEMORY_MODEL_BUILD_TEMPLATE, params)
        self.assertTrue(status_code == 200)
        self.assertTrue(json_data['error_code'] == ErrorCode.SUCCESS)

if __name__ == "__main__":
    unittest.main()


