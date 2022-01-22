from pathlib import Path
from hack.utils import get_env, get_config

PROJECT_PATH = Path(__file__).parent.parent

STATIC_PATH = PROJECT_PATH / 'build'

INDEX_PATH = STATIC_PATH / 'index.html'

CONFIG = get_config(PROJECT_PATH / get_env('BACKEND_CONFIG_PATH'))
