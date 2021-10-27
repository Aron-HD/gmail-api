import logging
import yaml

from logging.config import dictConfig
from pathlib import Path

# create log directory if it doesn't exist
try:
    Path('logs').mkdir(parents=True)
except FileExistsError:
    pass

# read in config for logging
with open('logging.yml') as fin:
    config = yaml.safe_load(fin)

dictConfig(config)

print('ran __init__')
