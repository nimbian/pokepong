import logging
import os
from distutils.util import strtobool
from ConfigParser import ConfigParser

# Load the software configuration
config = ConfigParser()
config.readfp(open('config.ini'))
env = 'dev'

def get_env_var_or_config(section, key):
    env_var = os.getenv(key.upper().replace('-', '_'))
    if env_var:
        return env_var
    else:
        return config.get(section, key)

_cfg = lambda k: get_env_var_or_config(env, k)
_cfgi = lambda k: int(_cfg(k))
_cfgb = lambda k: strtobool(_cfg(k)) == 1
