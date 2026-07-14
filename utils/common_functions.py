import os
import pandas
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml
from io import StringIO

log=get_logger(__name__)

def read_yaml(file_path):
    try:
      if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")
      with open(file_path,"r")as yaml_file:
        config=yaml.safe_load(yaml_file)
      
      log.info("YAML file loaded successfully")
      return config

    except Exception as e:
      log.error(f"error while reading yaml file")
      raise CustomException('failed to read yaml file',e)

