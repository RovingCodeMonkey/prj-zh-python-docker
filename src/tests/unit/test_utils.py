import uuid
from datetime import datetime

import pytest

from app import config, utils


def test_to_camel_case():
    a = "hello_in_there"
    assert utils.to_camel_case(a) == "helloInThere"


def test_encoder():
    enc = utils.Encoder()
    td_to_test = datetime(2020, 1, 1, 12, 1, 1) - datetime(2020, 1, 1, 1, 1, 1)
    uuid_to_test = uuid.uuid4()
    str_to_test = b"hello world"

    assert enc.default(obj=uuid_to_test) == str(uuid_to_test)
    with pytest.raises(TypeError):
        enc.default(obj=td_to_test)
    with pytest.raises(TypeError):
        enc.default(obj=str_to_test)


def test_json_response():
    obj = utils.JSONResponse()
    uuid_to_test = uuid.uuid4()

    dict_to_test = {
        "dt": datetime(2020, 1, 1, 12, 0, 0),
        "numeric": 1.5,
        "str": "hello world",
        "uuid": uuid_to_test,
    }

    rendered = obj.render(content=dict_to_test)
    assert (
        # fmt: off
        rendered == (
            '{\n    "dt":"2020-01-01T12:00:00",\n    "numeric":1.5,\n    '
            '"str":"hello world",\n    '
            f'"uuid":"{uuid_to_test}"\n}}'
        ).encode()
        # fmt: on
    )

    config.settings.development = False
    rendered = obj.render(content=dict_to_test)
    assert (
        # fmt: off
        rendered == (
            '{"dt":"2020-01-01T12:00:00","numeric":1.5,"str":"hello world",'
            f'"uuid":"{uuid_to_test}"}}'
        ).encode()
        # fmt: on
    )
