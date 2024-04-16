from datetime import datetime
from enum import Enum

from typing import List, Optional, Dict


class TestCase:
    __test__ = False

    def __init__(self, name, attributes):
        # type: (unicode, Dict[unicode,unicode]) -> None
        self.Name = name
        self.Attributes = attributes


class ResultType(str, Enum):
    UNKNOWN = "UNKNOWN"
    SUCCEED = "SUCCEED"
    FAILED = "FAILED"
    LOAD_FAILED = "LOAD_FAILED"
    IGNORED = "IGNORED"
    RUNNING = "RUNNING"
    WAITING = "WAITING"


class LogLevel(str, Enum):
    TRACE = "VERBOSE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARNNING"
    ERROR = "ERROR"


class AttachmentType(str, Enum):
    FILE = "FILE"
    URL = "URL"
    IFRAME = "IFRAME"


class TestCaseAssertError:
    __test__ = False

    def __init__(self, expected, actual, message):
        # type: (unicode, unicode, unicode) -> None
        self.Expect = expected
        self.Actual = actual
        self.Message = message


class TestCaseRuntimeError:
    __test__ = False

    def __init__(self, summary, detail):
        # type: (unicode, unicode) -> None
        self.Summary = summary
        self.Detail = detail


class Attachment:
    def __init__(self, name, url, attachment_type):
        # type: (unicode, unicode, AttachmentType) -> None
        self.Name = name
        self.Url = url
        self.AttachmentType = attachment_type


class TestCaseLog:
    __test__ = False

    def __init__(self, time, level, content, assert_error, runtime_error, attachments):
        # type: (datetime, LogLevel, unicode, Optional[TestCaseAssertError], Optional[TestCaseRuntimeError], List[Attachment]) -> None
        self.Time = time
        self.Level = level
        self.Content = content
        self.AssertError = assert_error
        self.RuntimeError = runtime_error
        self.Attachments = attachments


class TestCaseStep:
    __test__ = False

    def __init__(self, start_time, title, result_type, end_time, logs):
        # type:(datetime, unicode, ResultType, datetime, List[TestCaseLog]) -> None
        self.StartTime = start_time
        self.Title = title
        self.ResultType = result_type
        self.EndTime = end_time
        self.Logs = logs


class TestResult:
    __test__ = False

    def __init__(self, test, start_time, result_type, message, end_time, steps):
        # type: (TestCase, datetime, ResultType, unicode, Optional[datetime], List[TestCaseStep]) -> None
        self.Test = test
        self.StartTime = start_time
        self.ResultType = result_type
        self.Message = message
        self.EndTime = end_time
        self.Steps = steps

    def is_final(self):
        # type: () -> bool
        return self.ResultType in [
            ResultType.SUCCEED,
            ResultType.FAILED,
            ResultType.IGNORED,
            ResultType.LOAD_FAILED,
            ResultType.UNKNOWN,
        ]
