import inspect
from pprint import pprint


def add_location(data):
    # data["package"] = __package__
    # data["file"] = __file__
    # data["frame"] = inspect.getframeinfo(inspect.currentframe())
    frame = inspect.currentframe().f_back.f_back.f_back
    data["lineno"] = frame.f_lineno
    data["filename"] = frame.f_code.co_filename
    return data


def add_time(data):
    return data