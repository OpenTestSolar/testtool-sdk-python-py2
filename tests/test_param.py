import os

from testsolar_testtool_sdk_py2.model.param import load_param_entry


def test_load_param_entry():
    entry_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.json")

    r = load_param_entry(entry_file)

    assert r.TaskId == "afre89u789"
    assert r.ProjectPath == "/test/data/3289"
    assert r.FileReportPath == "/test/data/3289/report"
    assert r.Collectors == ["aa", "bb"]
    assert r.Context == {"aa": "bb"}
    assert r.TestSelectors == ["aaa", "bbb"]
