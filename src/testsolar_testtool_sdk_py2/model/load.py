from typing import List

from testsolar_testtool_sdk_py2.model.testresult import TestCase


class LoadError:
    def __init__(self, name, message):
        # type: (str, str) -> None
        self.name = name
        self.message = message


class LoadResult:
    def __init__(self, tests, load_errors):
        # type: (List[TestCase], List[LoadError]) -> None
        self.Tests = tests
        self.LoadErrors = load_errors

    def merge(self, other):
        # type: (LoadResult) -> None
        self.Tests.extend(other.Tests)
        self.LoadErrors.extend(other.LoadErrors)
