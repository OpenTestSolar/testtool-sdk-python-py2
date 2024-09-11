from testsolar_testtool_sdk_py2.model.testresult import (
    TestResult,
    TestCase,
    ResultType,
    TestCaseLog,
    LogLevel,
)
from datetime import datetime


def test_is_final():
    tr = TestResult(
        test=TestCase("aa", {}),
        start_time=datetime.now(),
        result_type=ResultType.FAILED,
        message="Test failed",
        end_time=datetime.now(),
        steps=[],
    )

    assert tr.is_final()


def test_is_not_final():
    tr = TestResult(
        test=TestCase("aa", {}),
        start_time=datetime.now(),
        result_type=ResultType.RUNNING,
        message="Test failed",
        end_time=datetime.now(),
        steps=[],
    )

    assert not tr.is_final()


def test_log_is_not_error():
    log = TestCaseLog(time=datetime.now(), level=LogLevel.WARN, content="")
    assert not log.is_error()


def test_log_is_error():
    log = TestCaseLog(time=datetime.now(), level=LogLevel.ERROR, content="boom!")
    assert log.is_error()
