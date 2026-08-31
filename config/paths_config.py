import os

RAW_DIR="artifacts/raw"
RAW_FILE_PATH=os.path.join(RAW_DIR,"raw.csv")
TRAIN_FILE_PATH=os.path.join(RAW_DIR,"train.csv")
TEST_FILE_PATH=os.path.join(RAW_DIR,"test.csv")

CONFIG_PATH="config/config.yaml"

####preprocesssing path######

PROCESSED_DIR="artifacts/preprocessing"
PROCESSED_TRAIN_DATA_PATH=os.path.join(PROCESSED_DIR,"Processed_train.csv")
PROCESSED_TEST_DATA_PATH=os.path.join(PROCESSED_DIR,"Processed_test.csv")

######training and tracking#######
MODEL_OUTPUT_PATH="artifacts/models/lgbm.pkl"