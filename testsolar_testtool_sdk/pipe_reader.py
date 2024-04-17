# coding=utf-8

import struct

import simplejson
from typing import BinaryIO, Dict

from testsolar_testtool_sdk.reporter import MAGIC_NUMBER


# 从管道读取测试用例结果，仅供单元测试使用
def read_result(pipe_io):
    # type: (BinaryIO) -> Dict
    result_data = _read_model(pipe_io)

    return simplejson.loads(result_data, encoding=None)


def _read_model(pipe_io):
    # type:(BinaryIO) -> bytes
    magic_number = struct.unpack("<I", pipe_io.read(4))[0]
    assert magic_number == MAGIC_NUMBER, "Magic number does not match %s" % MAGIC_NUMBER

    length = struct.unpack("<I", pipe_io.read(4))[0]

    result_data = pipe_io.read(length)
    return result_data
