import os

DATA_DIR = 'data'

TEMP_DIR = os.path.join(DATA_DIR, 'temp')
DB_DIR = os.path.join(DATA_DIR, 'db')
LOG_FILE_PATH = os.path.join(DATA_DIR, 'orz_bot.log')

LOGGING_CHANNEL = 834966915474653215

ALL_DIRS = (attrib_value for attrib_name, attrib_value in list(globals().items())
            if attrib_name.endswith('DIR'))