import logging
from datetime import datetime
import os

LOG_DIR = 'housing_logs'


CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

os.makedirs(LOG_DIR, exist_ok=  True)

LOG_FILE = f"log_{CURRENT_TIME_STAMP}.log"

log_file_path = os.path.join(LOG_DIR, LOG_FILE)

logging.basicConfig(filename= log_file_path,
                    filemode="w",
                    level=logging.INFO,
                    format='[%(asctime)s]^;%(levelname)s^;%(lineno)d^;%(filename)s^;%(funcName)s()^;%(message)s')