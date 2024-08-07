# coding=utf-8

import io
import json
import logging
import os
import shutil
import tempfile
import threading
from datetime import datetime, timedelta

from testsolar_testtool_sdk.model.load import LoadResult, LoadError
from testsolar_testtool_sdk.model.testresult import ResultType, LogLevel, TestCase
from testsolar_testtool_sdk.model.testresult import (
    TestResult,
    TestCaseStep,
    TestCaseAssertError,
    TestCaseLog,
    TestCaseRuntimeError,
    Attachment,
    AttachmentType,
)
from testsolar_testtool_sdk.pipe_reader import read_result, deserialize_data
from testsolar_testtool_sdk.reporter import (
    convert_to_json,
    PipeReporter,
    FileReporter,
    BaseReporter,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_random_unicode(length):
    # type: (int) -> str
    return "文件不存在:파일 つかりません"


def generate_demo_load_result():
    # type: () -> LoadResult
    r = LoadResult([], [])  # type: LoadResult

    for x in range(10):
        r.Tests.append(TestCase("mumu/mu.py/test_case_name_%d_p1" % x, {"tag": "P1"}))

    for x in range(5):
        r.LoadErrors.append(
            LoadError(
                name="load error %s" % x,
                message="""
文件读取失败。可能的原因包括：文件不存在、文件损坏、
不正确的编码方式或其他未知错误。请检查文件路径和内容的正确性，
确保文件具有正确的编码格式。如果问题仍然存在，可能需要尝试其他解决方法

"en": "File not found. Please check the file path and try again.",
"zh": "文件未找到。请检查文件路径，然后重试。",
"ja": "ファイルが見つかりません。ファイルパスを確認して、もう一度試してください。",
"ko": "파일을 찾을 수 없습니다. 파일 경로를 확인하고 다시 시도하십시오.",
"it": "File non trovato. Controlla il percorso del file e riprova.",
"ar": "الملف غير موجود. يرجى التحقق من مسار الملف والمحاولة مرة أخرى.",
"th": "ไม่พบไฟล์ โปรดตรวจสอบเส้นทางไฟล์และลองอีกครั้ง",
        """,
            )
        )
    return r


def generate_test_result(index):
    # type: (int) -> TestResult
    start = datetime.utcnow() - timedelta(seconds=40)  # type: datetime
    _tr = TestResult(
        TestCase("mumu/mu.py/test_case_name_%s_p1" % index, {}),
        start,
        ResultType.SUCCEED,
        "ファイルが見つかりません。ファイルパスを確認して、もう一度試してください。",
        datetime.utcnow(),
        [generate_testcase_step() for x in range(10)],
    )

    return _tr


def generate_testcase_log():
    # type: () -> TestCaseLog
    start = datetime.utcnow() - timedelta(seconds=15)  # type: datetime

    return TestCaseLog(
        start,
        LogLevel.INFO,
        "采集器：coll-imrv6szb当前状态为0，预期状态为1，状态不一致（0:处理中,1:正常） -> %s"
        % get_random_unicode(20),
        TestCaseAssertError("AAA", "BBB", "AAA is not BBB"),
        None,
        [],
    )


def generate_testcase_step():
    # type: () -> TestCaseStep
    start = datetime.utcnow() - timedelta(seconds=10)  # type: datetime
    return TestCaseStep(
        start,
        get_random_unicode(100),
        ResultType.SUCCEED,
        datetime.utcnow(),
        [generate_testcase_log() for x in range(10)],
    )


def test_report_load_result_by_pipe():
    # type: () -> None
    # 创建一个Reporter实例
    pipe_io = io.BytesIO()
    reporter = PipeReporter(pipe_io=pipe_io)
    # 创建一个LoadResult实例
    load_result = generate_demo_load_result()

    # 调用report_load_result方法
    reporter.report_load_result(load_result)

    # 检查管道中的魔数
    pipe_io.seek(0)

    loaded = read_result(pipe_io)
    assert len(loaded.get("LoadErrors")) == len(load_result.LoadErrors)
    assert len(loaded.get("Tests")) == len(load_result.Tests)
    assert loaded.get("LoadErrors")[0].get("name") == load_result.LoadErrors[
        0
    ].name.decode("utf-8")
    assert loaded.get("LoadErrors")[0].get("message") == load_result.LoadErrors[
        0
    ].message.decode("utf-8")


def test_report_load_result_by_file():
    # type: () -> None
    # 创建一个Reporter实例
    tmp_dir = tempfile.mkdtemp()
    try:
        reporter = FileReporter(tmp_dir)
        # 创建一个LoadResult实例
        load_result = generate_demo_load_result()

        # 调用report_load_result方法
        reporter.report_load_result(load_result)

        with open(os.path.join(tmp_dir, "result.json"), "r") as f:
            loaded = deserialize_data(f.read())
            assert len(loaded.get("LoadErrors")) == len(load_result.LoadErrors)
            assert len(loaded.get("Tests")) == len(load_result.Tests)
            assert loaded.get("LoadErrors")[0].get("name") == load_result.LoadErrors[
                0
            ].name.decode("utf-8")
            assert loaded.get("LoadErrors")[0].get("message") == load_result.LoadErrors[
                0
            ].message.decode("utf-8")
    finally:
        shutil.rmtree(tmp_dir)


def send_test_result(reporter, index=0):
    # type: (BaseReporter, int) -> None
    test_results = []
    run_case_result = generate_test_result(index)
    test_results.append(run_case_result)
    reporter.report_case_result(run_case_result)


def test_datetime_formatted():
    run_case_result = generate_test_result(0)
    data = convert_to_json(run_case_result)
    tr = json.loads(data)
    assert tr["StartTime"].endswith("Z")
    assert tr["EndTime"].endswith("Z")

    assert tr["Steps"][0]["StartTime"].endswith("Z")
    assert tr["Steps"][0]["EndTime"].endswith("Z")

    assert tr["Steps"][0]["Logs"][0]["Time"].endswith("Z")


def test_report_run_case_result_with_pipe():
    threads = []
    # 创建一个Reporter实例
    pipe_io = io.BytesIO()
    reporter = PipeReporter(pipe_io=pipe_io)
    # 创建五个LoadResult实例并发调用report_run_case_result方法
    for i in range(5):
        # 创建线程
        t = threading.Thread(target=send_test_result, args=(reporter,))
        # 将线程添加到线程列表
        threads.append(t)
        # 启动线程
        t.start()

    for t in threads:
        t.join()

    # 检查管道中的数据，确保每个用例的魔数和数据长度还有数据正确
    pipe_io.seek(0)
    r1 = read_result(pipe_io)
    assert r1.get("ResultType") == ResultType.SUCCEED
    r2 = read_result(pipe_io)
    assert r2.get("ResultType") == ResultType.SUCCEED
    r3 = read_result(pipe_io)
    assert r3.get("ResultType") == ResultType.SUCCEED
    r4 = read_result(pipe_io)
    assert r4.get("ResultType") == ResultType.SUCCEED
    r5 = read_result(pipe_io)
    assert r5.get("ResultType") == ResultType.SUCCEED


def test_report_run_case_result_with_file():
    threads = []
    # 创建一个Reporter实例
    tmp_dir = tempfile.mkdtemp()
    try:
        reporter = FileReporter(tmp_dir)
        # 创建五个LoadResult实例并发调用report_run_case_result方法
        for i in range(5):
            # 创建线程
            t = threading.Thread(target=send_test_result, args=(reporter, i))
            # 将线程添加到线程列表
            threads.append(t)
            # 启动线程
            t.start()

        for t in threads:
            t.join()

        # 检查生成的文件是否符合要求
        for dirpath, _, filenames in os.walk(tmp_dir):
            assert len(filenames) == 5

            for filename in filenames:
                with open(os.path.join(dirpath, filename), "r") as f:
                    tr = deserialize_data(f.read())

                    assert tr.get("ResultType") == ResultType.SUCCEED
    finally:
        shutil.rmtree(tmp_dir)


def test_convert_to_json_with_custom_encoder():
    tr = TestResult(
        TestCase("mumu/mu.py/test_case_name_%s_p1", {"tag": "bbb"}),
        datetime.utcnow(),
        ResultType.SUCCEED,
        "ファイルが見つかりません",
        datetime.utcnow(),
        [
            TestCaseStep(
                start_time=datetime.utcnow(),
                title="hello world",
                result_type=ResultType.SUCCEED,
                end_time=datetime.utcnow(),
                logs=[
                    TestCaseLog(
                        time=datetime.utcnow(),
                        level=LogLevel.INFO,
                        content="hello world 1",
                        assert_error=TestCaseAssertError(
                            "AAA", "BBB", "AAA is not BBB"
                        ),
                        runtime_error=TestCaseRuntimeError("AAA", "BBB"),
                        attachments=[
                            Attachment(
                                name="attachment 1",
                                attachment_type=AttachmentType.URL,
                                url="https://example.com",
                            )
                        ],
                    )
                ],
            )
        ],
    )

    re = json.loads(convert_to_json(tr))

    assert len(re["Steps"]) == 1
    assert re["Steps"][0]["Logs"][0]["RuntimeError"]["Summary"] == "AAA"
