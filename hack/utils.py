import os
import random
import time

from os import getenv
from pathlib import Path
from typing import Any, Dict, Union
from hashlib import md5, sha1
from ruamel.yaml import safe_load

from hack.trafarets import config_trafaret


def get_env(name: str) -> str:
    env = getenv(name)
    if env:
        return env
    raise RuntimeError(f'{name} not set')


def get_config(path: Union[str, Path]) -> Dict[str, Any]:
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
