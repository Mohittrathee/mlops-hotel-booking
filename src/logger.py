import logging
import os
from datetime import datetime

Logs_Dir="logs"
os.makedirs(name=Logs_Dir, exist_ok=True)

Log_file=os.path.join(Logs_Dir,f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

logging.basicConfig(
    filename=Log_file,
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def get_logger(name):
    logger=logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger