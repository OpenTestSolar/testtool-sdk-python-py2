# coding=utf-8
import hashlib
import io
import logging
import os
import struct
from abc import ABCMeta, abstractmethod

import portalocker
import simplejson
from typing import Optional, BinaryIO, Any

from testsolar_testtool_sdk.model.encoder import DateTimeEncoder
from testsolar_testtool_sdk.model.load import LoadResult
from testsolar_testtool_sdk.model.testresult import TestResult

# 跟TestSolar uniSDK约定的管道上报魔数，避免乱序导致后续数据全部无法上报
MAGIC_NUMBER = 0x1234ABCD

# 跟TestSolar uniSDK约定的管道上报文件描述符号
PIPE_WRITER = 3


class BaseReporter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def report_load_result(self, load_result):
        # type: (LoadResult) ->None
        pass

    @abstractmethod
    def report_case_result(self, case_result):
        # type: (TestResult) -> None
        pass


class Reporter(BaseReporter):
    def __init__(self, pipe_io=None):
        # type: (Optional[BinaryIO]) -> None
        """
        初始化报告工具类
        :param pipe_io: 可选的管道，用于测试
        """
        home = os.path.expanduser("~")
        self.lock_file = os.path.join(home, "testsolar_reporter.lock")

        if pipe_io:
            self.pipe_io = pipe_io
        else:
            self.pipe_io = os.fdopen(PIPE_WRITER, "wb")

    def report_load_result(self, load_result):
        # type: (LoadResult) -> None
        with portalocker.Lock(self.lock_file, timeout=60):
            self._send_json(load_result)

    def report_case_result(self, case_result):
        # type: (TestResult) -> None
        with portalocker.Lock(self.lock_file, timeout=60):
            self._send_json(case_result)

    def _send_json(self, result):
        # type: (Any) -> None
        data = convert_to_json(result)
        data_bytes = data.encode("utf-8")
        length = len(data_bytes)

        # 将魔数写入管道
        self.pipe_io.write(struct.pack("<I", MAGIC_NUMBER))

        # 将 JSON 数据的长度写入管道
        self.pipe_io.write(struct.pack("<I", length))

        # 将 JSON 数据本身写入管道
        self.pipe_io.write(data_bytes)

        logging.debug("Sending {%s} bytes to pipe {%s}" % (length, PIPE_WRITER))

        self.pipe_io.flush()


PipeReporter = Reporter


class FileReporter(BaseReporter):
    def __init__(self, report_path):
        # type: (str) -> None
        self.report_path = report_path

    def report_load_result(self, load_result):
        # type: (LoadResult) ->None
        out_file = os.path.join(self.report_path, "result.json")
        logging.debug("Writing load results to {}".format(out_file))
        with io.open(out_file, "w", encoding="utf-8") as f:
            data = convert_to_json(load_result, pretty=True)
            f.write(data)

    def report_case_result(self, case_result):
        # type: (TestResult) -> None
        retry_id = case_result.Test.Attributes.get("retry", "0")
        filename = (
            hashlib.md5(
                "{}.{}".format(case_result.Test.Name, retry_id).encode("utf-8")
            ).hexdigest()
            + ".json"
        )
        out_file = os.path.join(self.report_path, filename)

        logging.debug(
            "Writing case [{}] results to {}".format(
                "{}.{}".format(case_result.Test.Name, retry_id), out_file
            )
        )

        with io.open(out_file, "w", encoding="utf-8") as f:
            data = convert_to_json(case_result, pretty=True)
            f.write(data)


def convert_to_json(result, pretty=False):
    # type: (Any, bool) -> str
    if pretty:
        return simplejson.dumps(
            result, cls=DateTimeEncoder, indent=2, ensure_ascii=False
        )
    else:
        return simplejson.dumps(result, cls=DateTimeEncoder, ensure_ascii=False)
