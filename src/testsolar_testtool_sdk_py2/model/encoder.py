# coding=utf-8
from datetime import datetime

import simplejson

from testsolar_testtool_sdk_py2.model.load import LoadResult, LoadError
from testsolar_testtool_sdk_py2.model.testresult import (
    TestCase,
    TestResult,
    TestCaseStep,
    TestCaseLog,
    TestCaseAssertError,
    TestCaseRuntimeError,
    Attachment,
)


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
        elif isinstance(obj, TestResult):
            return obj.__dict__
        elif isinstance(obj, TestCaseStep):
            return obj.__dict__
        elif isinstance(obj, TestCaseLog):
            return obj.__dict__
        elif isinstance(obj, TestCaseAssertError):
            return obj.__dict__
        elif isinstance(obj, TestCaseRuntimeError):
            return obj.__dict__
        elif isinstance(obj, Attachment):
            return obj.__dict__
        else:
            return super(DateTimeEncoder, self).default(obj)


def _format_datetime(t):
    # type: (datetime) -> str
    return t.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
