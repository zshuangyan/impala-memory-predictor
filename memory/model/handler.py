import logging
from ..model_handler import ModelBuildHandler
from ..constants import ModelStatus
from .task import Task


class ModelHandler(ModelBuildHandler):
    def post(self):
        start_day = self.data['start_day']
        end_day = self.data['end_day']
        generate_feature = self.data.get('generate_feature', True)
        cross_validate = self.data.get('cross_validate', True)
        self.write({"error_code": 0})
        self.finish()
        try:
            Task(start_day, end_day).run(generate_feature, cross_validate)
        except Exception as err:
            logging.exception(err)
            self.model_status = ModelStatus.FAILED
        else:
            self.model_status = ModelStatus.FINISHED
