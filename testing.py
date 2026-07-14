import sys
from src.logger import get_logger
from src.custom_exception import CustomException

logger=get_logger(__name__)

def devide(a,b):
    try:
        result=a/b
    except Exception as e:
        logger.error("Error in division")
        raise CustomException("Error in division",sys)
    return result

if __name__ == "__main__":
    logger.info("Starting the application")
    print(devide(10,2))
    logger.info("Application finished")
