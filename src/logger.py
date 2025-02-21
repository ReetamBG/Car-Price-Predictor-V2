import logging
import os
from datetime import datetime as dt

# LOG_FILE = f"{dt.now().strftime('%m-%d-%Y %H_%M_%S')}.log"
LOG_FILE = "logs.log"      # storing it in a single file for now
LOGS_PATH = "logs"
LOG_FILE_PATH = os.path.join(LOGS_PATH, LOG_FILE)

os.makedirs(LOGS_PATH, exist_ok=True)

logging.basicConfig(
    filename = LOG_FILE_PATH,       # file path where logs will be saved
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
)


# Testing 
if __name__ == "__main__":
    logging.info("Test Logging")