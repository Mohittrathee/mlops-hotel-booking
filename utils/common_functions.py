import os
import sys
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

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
      raise CustomException('failed to read yaml file',sys)

def data_load(path):
  try:
    log.info("data is loading")
    return pd.read_csv(path)
  except Exception as e:
    log.error(f"error while loading the data")
    raise CustomException(f"error in data loading", sys)


