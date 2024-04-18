from testsolar_testtool_sdk.decoder import decode_env_value


def test_decode_env_value():
    re = decode_env_value("AABB")
    assert re == "AABB"

    re = decode_env_value("b64://aGVsbG8=")
    assert re == "hello"
