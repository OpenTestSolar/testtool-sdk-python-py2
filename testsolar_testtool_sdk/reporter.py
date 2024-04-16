# coding=utf-8

import logging
import os
import struct
from datetime import datetime

import jsonpickle
import portalocker
from typing import Optional, BinaryIO, Any

from testsolar_testtool_sdk.model.encoder import DateTimeHandler
from testsolar_testtool_sdk.model.load import LoadResult
from testsolar_testtool_sdk.model.testresult import TestResult

# 跟TestSolar uniSDK约定的管道上报魔数，避免乱序导致后续数据全部无法上报
MAGIC_NUMBER = 0x1234ABCD

# 跟TestSolar uniSDK约定的管道上报文件描述符号
PIPE_WRITER = 3

jsonpickle.handlers.registry.register(datetime, DateTimeHandler)
jsonpickle.set_encoder_options('json', ensure_ascii=False)


class Reporter:
    def __enter__(self):
        return self

    def __init__(self, pipe_io=None, full_type=False):
        # type: (Optional[BinaryIO], bool) -> None
        """
        初始化报告工具类
        :param pipe_io: 可选的管道，用于测试
        """
        self.lock_file = "/tmp/testsolar_reporter.lock"
        self.full_type = full_type

        if pipe_io:
            self.pipe_io = pipe_io
        else:
            self.pipe_io = os.fdopen(PIPE_WRITER, "wb")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def report_load_result(self, load_result):
        # type: (LoadResult) -> None
        with portalocker.Lock(self.lock_file, timeout=60):
            self._send_json(load_result)

    def report_case_result(self, case_result):
        # type: (TestResult) -> None
        with portalocker.Lock(self.lock_file, timeout=60):
            self._send_json(case_result)

    def close(self):
        if self.pipe_io:
            self.pipe_io.close()

    def _send_json(self, result):
        # type: (Any) -> None
        data = convert_to_json(result, full_type=self.full_type)
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


def convert_to_json(result, full_type):
    # type: (Any, bool) -> str
    if full_type:
        return jsonpickle.encode(result, unpicklable=True)
    else:
        return jsonpickle.encode(result, unpicklable=False)
