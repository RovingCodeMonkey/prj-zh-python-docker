import datetime
import json
import uuid
from typing import Any

from starlette.responses import Response

from app import config


def to_camel_case(snake_str: str) -> str:
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def validate_uuid(uuid_str: str) -> bool:
    try:
        uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False


class BaseConfig:
    alias_generator = to_camel_case
    allow_population_by_field_name = True


class Encoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        else:
            return super(Encoder, self).default(obj)


class JSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        args = {}
        if config.settings.development:
            args["indent"] = 4

        return json.dumps(
            content,
            cls=Encoder,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
            **args,  # type: ignore
        ).encode("utf-8")
