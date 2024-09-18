import json

from typing import Dict, List


class EntryParam:
    def __init__(
        self,
        task_id,
        project_path,
        file_report_path,
        collectors,
        context,
        test_selectors,
    ):
        # type: (str, str, str, List[str], Dict[str, str], List[str]) -> None
        self.TaskId = task_id
        self.ProjectPath = project_path
        self.FileReportPath = file_report_path
        self.Collectors = collectors
        self.Context = context
        self.TestSelectors = test_selectors


def load_param_entry(entry_path):
    # type: (str) -> EntryParam
    with open(entry_path, "r") as f:
        raw = json.load(f)

        return EntryParam(
            raw.get("TaskId"),
            raw.get("ProjectPath"),
            raw.get("FileReportPath"),
            raw.get("Collectors"),
            raw.get("Context"),
            raw.get("TestSelectors"),
        )
