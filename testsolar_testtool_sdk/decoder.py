import base64
import logging


def decode_env_value(value):
    # type: (str) -> str
    if value.startswith("b64://"):
        try:
            value = base64.b64decode(value[6:]).decode()
        except Exception as e:
            logging.warning("Invalid base64 string: %s, err: %s" % (value, e))
    return value
