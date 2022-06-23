import configparser
import logging
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

logger_name = config['logger']['Name']

logger = logging.getLogger(logger_name)
logging.basicConfig()
logger.setLevel(logging.INFO)