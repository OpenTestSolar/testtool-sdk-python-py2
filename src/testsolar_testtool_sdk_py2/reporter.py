# coding=utf-8
import hashlib
import io
import logging
import os
from abc import ABCMeta, abstractmethod
from typing import Any, Dict

import simplejson

from testsolar_testtool_sdk_py2.model.encoder import DateTimeEncoder
from testsolar_testtool_sdk_py2.model.load import LoadResult
from testsolar_testtool_sdk_py2.model.testresult import TestResult


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
            hashlib.md5("{}.{}".format(case_result.Test.Name, retry_id).encode("utf-8")).hexdigest()
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
        return simplejson.dumps(result, cls=DateTimeEncoder, indent=2, ensure_ascii=False)
    else:
        return simplejson.dumps(result, cls=DateTimeEncoder, ensure_ascii=False)


def deserialize_data(result_data):
    # type: (str) -> Dict[str, Any]

    return simplejson.loads(result_data, encoding="utf-8")
