from testsolar_testtool_sdk_py2.model.load import LoadResult, LoadError
from testsolar_testtool_sdk_py2.model.testresult import TestCase


def test_load_result_merge():
    load_result = LoadResult(tests=[], load_errors=[])

    load_result_new = LoadResult(
        tests=[TestCase(name="Hello", attributes={})],
        load_errors=[
            LoadError(name="Hello", message="Hello world"),
        ],
    )

    assert len(load_result.Tests) == 0
    assert len(load_result.LoadErrors) == 0

    load_result.merge(load_result_new)

    assert len(load_result.Tests) == 1
    assert len(load_result.LoadErrors) == 1
