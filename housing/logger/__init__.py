import logging
from datetime import datetime
import os
import pandas as pd

LOG_DIR = 'housing_logs'


CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

os.makedirs(LOG_DIR, exist_ok=  True)

LOG_FILE = f"log_{CURRENT_TIME_STAMP}.log"

log_file_path = os.path.join(LOG_DIR, LOG_FILE)

logging.basicConfig(filename= log_file_path,
                    filemode="w",
                    level=logging.INFO,
                    format='[%(asctime)s]^;%(levelname)s^;%(lineno)d^;%(filename)s^;%(funcName)s()^;%(message)s')

def get_log_dataframe(filepath):
    data = []
    with open(filepath) as log_file:
        for line in log_file.readlines():
            data.append(line.split("^;"))
    
    log_df = pd.DataFrame(data=data)
    
    columns = ["Timestamp", "Log Level", "line_number", "file_name", "function_name", "message"]
    
    log_df.columns = columns
    
    log_df["log_message"] = log_df['Timestamp'].astype(str) + ":$" + log_df["message"]
    
    return log_df[["log_message"]]