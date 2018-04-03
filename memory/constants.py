from enum import IntEnum
MODEL_STATUS = "model_status"


class ModelStatus(IntEnum):
    def __new__(cls, value, phrase):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.phrase = phrase
        return obj

    FINISHED = 0, "Finished"
    RUNNING = 1, "Running"
    FAILED = 2, "Failed"
