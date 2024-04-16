# coding=utf-8
from datetime import datetime

from testsolar_testtool_sdk.model.load import LoadResult, LoadError
from testsolar_testtool_sdk.model.testresult import TestCase

import simplejson


class DateTimeEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return _format_datetime(obj)
        elif isinstance(obj, LoadResult):
            return obj.__dict__
        elif isinstance(obj, LoadError):
            return obj.__dict__
        elif isinstance(obj, TestCase):
            return obj.__dict__
        else:
            return super(DateTimeEncoder, self).default(obj)


def _format_datetime(t):
    # type: (datetime) -> str
    return t.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
