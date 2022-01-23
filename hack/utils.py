import os
import random
import re
import time
from hashlib import md5, sha1
from os import getenv
from pathlib import Path
import typing as t

from ruamel.yaml import safe_load

from hack.trafarets import config_trafaret


def get_env(name: str) -> str:
    env = getenv(name)
    if env:
        return env
    raise RuntimeError(f'{name} not set')


def get_config(path: t.Union[str, Path]) -> t.Dict[str, t.Any]:
    with open(str(path)) as stream:
        config = safe_load(stream.read())
        config_trafaret.check(config)
        return config


def gen_id() -> str:
    """Generate random id"""
    vars_ = (time.time(), id({}), random.random(), os.getpid())
    return sha1(
        bytes(
            md5(bytes(''.join(map(str, vars_)), 'utf-8')).hexdigest(), 'utf-8'
        )
    ).hexdigest()


def to_camel_case(snake_str: str) -> str:
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_snake_case(camel_str: str) -> str:
    name_re = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name_re).lower()


def _convert_dict(data: t.Any, transform_func: t.Callable) -> t.Any:
    result = {}
    for key in data:
        new_key = transform_func(key)
        if isinstance(data[key], dict):
            result[new_key] = _convert_dict(data[key], transform_func)
        elif isinstance(data[key], list):
            result[new_key] = _convert_list(data[key], transform_func)
        else:
            result[new_key] = data[key]
    return result


def _convert_list(data: t.Any, transform_func: t.Callable) -> t.Any:
    result = []
    for el in data:
        if isinstance(el, list):
            result.append(_convert_list(el, transform_func))
        elif isinstance(el, dict):
            result.append(_convert_dict(el, transform_func))
        else:
            result.append(el)
    return result


def transform_dict_keys(
    data_dict: t.Dict[str, t.Any], transform_func: t.Callable
) -> t.Optional[t.Dict[str, t.Any]]:
    if isinstance(data_dict, dict):
        return _convert_dict(data_dict, transform_func=transform_func)

    raise ValueError('Data must be Dict instance')
