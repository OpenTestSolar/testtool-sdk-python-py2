# coding=utf-8
from datetime import datetime

import jsonpickle


class DateTimeHandler(jsonpickle.handlers.BaseHandler):
    def flatten(self, obj, data):
        if isinstance(obj, datetime):
            return _format_datetime(obj)
        else:
            return jsonpickle.encode(self, data)

    def restore(self, obj):
        # 提供反序列化的方法
        return datetime.strptime(obj, '%Y-%m-%dT%H:%M:%S.%f')


def _format_datetime(t):
    # type: (datetime) -> str
    return t.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
