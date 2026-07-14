import sys
from config.paths_config import Config_path
from config.paths_config import Raw_file_path
import os
import pandas as pd
from google.cloud import storage 
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from utils.common_functions import read_yaml
from config.paths_config import * 
logger=get_logger(__name__)

class DataIngestion:
    def __init__(self,config):
      self.config=config["data_ingestion"]
      self.bucket_name=self.config["bucket_name"]
      self.bucket_file_name=self.config["bucket_file_name"]
      self.train_test_split_ratio=self.config["train_ratio"]
      
      os.makedirs(RAW_DIR,exist_ok=True)

      logger.info(f"data ingestion is started with {self.bucket_name} and {self.bucket_file_name}")

    def download_csv_from_gcp(self):
        
        try:
            client=storage.Client()
            bucket=client.bucket(self.bucket_name)
            blob=bucket.blob(self.bucket_file_name)
            blob.download_to_filename(Raw_file_path)
            logger.info(f"csv file is downloaded from {self.bucket_name} and {self.bucket_file_name}")
        except Exception as e:
            logger.error(f"data ingestion is failed {e}")
            raise CustomException("failed to download the data",sys)

    def split_data(self):
        try:
            data=pd.read_csv(Raw_file_path)
            train_data,test_data=train_test_split(data,test_size=1-self.train_test_split_ratio,random_state=42)
            
            train_data.to_csv(Train_file_path,index=False)
            test_data.to_csv(Test_file_path,index=False)
            
            logger.info(f"data is split into train and test")
        except Exception as e:
            logger.error(f"data ingestion is failed {e}")
            raise CustomException("failed to split the data",sys)

    def run(self):
        try:  
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("data ingestion is completed")
        except CustomException as ce:
            logger.error(f"data ingestion is failed {ce}")
        finally:
            logger.info("data ingestion is completed")


if __name__=="__main__":
  data_ingestion=DataIngestion(read_yaml(Config_path))

  data_ingestion.run()
        
        