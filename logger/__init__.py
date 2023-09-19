import logging
import os
from datetime import datetime

logs_path = os.path.join(os.getcwd(),'logs')
os.makedirs(logs_path,exist_ok=True)

LOG_FILE_NAME = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_S')}.log"
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE_NAME)


logging.basicConfig(
    # filename=LOG_FILE_PATH,
    format="[%(asctime)s] Line No. %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
)

# Create a file handler
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setLevel(logging.INFO)  # Set the desired log level
file_handler.setFormatter(logging.Formatter('[%(asctime)s] Line No. %(lineno)d %(name)s - %(levelname)s - %(message)s'))

# Create a stream handler (console output)
# stream_handler = logging.StreamHandler()
# stream_handler.setLevel(logging.INFO)  # Set the desired log level
# stream_handler.setFormatter(logging.Formatter('[%(asctime)s] Line No. %(lineno)d %(name)s - %(levelname)s - %(message)s'))

# Get the root logger and add handlers
logger = logging.getLogger()
logger.addHandler(file_handler)
# logger.addHandler(stream_handler)