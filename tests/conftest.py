import six


def smart_str(data):
    if isinstance(data, six.binary_type):
        return data.decode("utf-8")
    else:
        return data
