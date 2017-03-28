import os
import sys
from enum import Enum


class Const(Enum):
    DEBUG_MODE = True
    LOCAL_MODE = True

    ASBPATH = os.path.abspath(os.path.dirname(sys.argv[0]))

    LOG_CONFIG_FILE = os.sep.join([ASBPATH, 'conf', 'logger.conf'])
    # LOGGER_NAME = 'prodEnv'
    ONL_LOGGER_NAME = 'onlDevEnv'
    BAT_LOGGER_NAME = 'batDevEnv'

    ORIGINAL_TEMPLATE_WIDTH = 1440
    ORIGINAL_TEMPLATE_HEIGHT = 900


    DB_URL = '127.0.0.1'
    DB_PORT = 9736

