from testsolar_testtool_sdk_py2.decoder import decode_env_value


def test_decode_env_value():
    re = decode_env_value("AABB")
    assert re == "AABB"

    re = decode_env_value("b64://aGVsbG8=")
    assert re == "hello"

    re = decode_env_value("b64://uf893uf9")
    assert re == "b64://uf893uf9"
