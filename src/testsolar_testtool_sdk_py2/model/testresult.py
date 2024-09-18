from datetime import datetime

from enum import Enum
from typing import List, Optional, Dict


class TestCase:
    __test__ = False

    def __init__(self, name, attributes):
        # type: (str, Dict[str,str]) -> None
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
        # type: (str, str, str) -> None
        self.Expect = expected
        self.Actual = actual
        self.Message = message


class TestCaseRuntimeError:
    __test__ = False

    def __init__(self, summary, detail):
        # type: (str, str) -> None
        self.Summary = summary
        self.Detail = detail


class Attachment:
    def __init__(self, name, url, attachment_type):
        # type: (str, str, AttachmentType) -> None
        self.Name = name
        self.Url = url
        self.AttachmentType = attachment_type


class TestCaseLog:
    __test__ = False

    def __init__(
            self,
            time,
            level,
            content,
            assert_error=None,
            runtime_error=None,
            attachments=None,
    ):
        # type: (datetime, LogLevel, str, Optional[TestCaseAssertError], Optional[TestCaseRuntimeError], Optional[List[Attachment]]) -> None
        self.Time = time
        self.Level = level
        self.Content = content
        self.AssertError = assert_error
        self.RuntimeError = runtime_error
        self.Attachments = attachments

    def is_error(self):
        # type: () -> bool
        """
        Checks if the log is an error
        """
        return self.Level in [
            LogLevel.ERROR,
        ]


class TestCaseStep:
    __test__ = False

    def __init__(self, start_time, title, result_type, end_time=None, logs=None):
        # type:(datetime, str, ResultType, Optional[datetime], Optional[List[TestCaseLog]]) -> None
        self.StartTime = start_time
        self.Title = title
        self.ResultType = result_type
        self.EndTime = end_time
        self.Logs = logs


class TestResult:
    __test__ = False

    def __init__(self, test, start_time, result_type, message, end_time=None, steps=None):
        # type: (TestCase, datetime, ResultType, str, Optional[datetime], Optional[List[TestCaseStep]]) -> None
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


def convert_to_datetime(raw):
    # type:(Optional[str]) -> Optional[datetime]
    if raw:
        return datetime.strptime(raw, "%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        return None


def convert_to_test_result(raw):
    # type: (Dict) -> TestResult
    tr = TestResult(
        test=TestCase(
            name=raw["Test"]["Name"],
            attributes=raw["Test"]["Attributes"],
        ),
        start_time=convert_to_datetime(raw["StartTime"]),
        result_type=raw["ResultType"],
        message=raw["Message"],
        end_time=convert_to_datetime(raw.get("EndTime")),
    )

    tr.Steps = convert_to_steps(raw)

    return tr


def convert_to_steps(raw):
    # type: (Dict) -> List[TestCaseStep]
    ret = []
    if "Steps" in raw:
        for rawStep in raw["Steps"]:
            step = TestCaseStep(
                start_time=convert_to_datetime(rawStep["StartTime"]),
                title=rawStep["Title"],
                result_type=rawStep["ResultType"],
                end_time=convert_to_datetime(rawStep.get("EndTime")),
            )
            if "Logs" in rawStep:
                step.Logs = convert_to_logs(rawStep)

            ret.append(step)

    return ret


def convert_to_logs(raw):
    # type: (Dict) -> List[TestCaseLog]
    ret = []
    for rawLog in raw["Logs"]:
        log = TestCaseLog(
            time=convert_to_datetime(rawLog["Time"]),
            level=rawLog["Level"],
            content=rawLog["Content"],
            assert_error=convert_to_assert_error(rawLog),
            runtime_error=convert_to_runtime_error(rawLog),
            attachments=convert_to_attachments(rawLog),
        )

        ret.append(log)

    return ret


def convert_to_assert_error(raw):
    # type:(Dict) -> Optional[TestCaseAssertError]
    assert_error = raw.get("AssertError")
    if assert_error:
        return TestCaseAssertError(
            expected=assert_error["Expect"],
            actual=assert_error["Actual"],
            message=assert_error["Message"],
        )
    else:
        return None


def convert_to_runtime_error(raw):
    # type:(Dict) -> Optional[TestCaseRuntimeError]
    runtime_error = raw.get("RuntimeError")
    if runtime_error:
        return TestCaseRuntimeError(
            summary=runtime_error["Summary"],
            detail=runtime_error["Detail"],
        )
    else:
        return None


def convert_to_attachments(raw):
    # type: (Dict) -> List[Attachment]
    ret = []

    attachments = raw.get("Attachments")
    if attachments:
        for attachment in attachments:
            ret.append(Attachment(name=attachment["Name"], url=attachment["Url"], attachment_type=attachment["AttachmentType"]))

    return ret
