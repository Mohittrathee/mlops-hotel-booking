import os
import sys
import numpy as np
import pandas as pd
import joblib
import mlflow
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import f1_score,accuracy_score,precision_score,recall_score
import lightgbm as lgb
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from scipy.stats import randint,uniform
from utils.common_functions import read_yaml,data_load

logger=get_logger(__name__)

class ModelTraining:
    def __init__(self,train_path,test_path,model_output_path):
        self.train_path=train_path
        self.test_path=test_path
        self.model_output_path=model_output_path

        self.param_list=LIGHTGM_PARAMS
        self.random_search_params=RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            logger.info(f"loading the data from{self.train_path}")
            train_df=data_load(self.train_path)

            logger.info(f"loading test data from the {self.test_path}")
            test_df=data_load(self.test_path)

            X_train=train_df.drop(columns=["booking_status"])
            Y_train=train_df["booking_status"]

            X_test=test_df.drop(columns=["booking_status"])
            Y_test=test_df["booking_status"]

            logger.info("data splitted successfully")

            return X_train,Y_train,X_test,Y_test

        except Exception as e:
            logger.error(f"error while splitting the data {e}")
            raise CustomException("failed to load data", sys)

    def train_lgbm(self,X_train,Y_train):
        try:
            logger.info(f"we started training the lgbm")
            lgbm_model=lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])

            logger.info(f"starting hyperparameter tuning")
            
            random_search=RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.param_list,
                n_iter=self.random_search_params["n_iter"],
                random_state=self.random_search_params["random_state"],
                n_jobs=self.random_search_params["n_jobs"],
                scoring=self.random_search_params["scoring"],
                cv=self.random_search_params["cv"],
                verbose=self.random_search_params["verbose"],

            )

            logger.info(f"starting our model training")

            random_search.fit(X_train,Y_train)
            
            logger.info(f"hyperparameter tuning completed")

            best_params = random_search.best_params_
            best_model = random_search.best_estimator_

            return best_model, best_params

        except Exception as e:
            logger.info(f"error while training the model {e}")
            raise CustomException("failed to train the model", sys)

    def eval_model(self,X_test,y_test,model):
        try:
            logger.info(f"starting the evaluation of the model")

            y_pred=model.predict(X_test)

            accuracy=accuracy_score(y_test,y_pred)
            f1=f1_score(y_test,y_pred)
            precision=precision_score(y_test,y_pred)
            recall=recall_score(y_test,y_pred)

            logger.info(f"accuracy of the model={accuracy}")
            logger.info(f"f1Score of the model ={f1}")
            logger.info(f"precision score of the model={precision}")
            logger.info(f"recall score of the model={recall}")

            return{
                "accuracy":accuracy,
                "f1_score":f1,
                "precision":precision,
                "recall":recall
            }

        except Exception as e:
            logger.info(f"error while eval the data{e}")
            raise CustomException("failed to evaluate the data", sys)

    def saving_model(self,model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            logger.info(f"saving the model")
            joblib.dump(model,self.model_output_path)

            logger.info(f"model is saved to the {self.model_output_path}")

        except Exception as e:
            logger.info(f"error while saving the model {e}")
            raise CustomException("failed to save the model", sys)

    def run(self):
        try:
            with mlflow.start_run():
                logger.info(f"we have started training pipeline")
                logger.info(f"we have initialiased mlflow experimentation")

                logger.info(f"logging testing and training datasets to mlflow")

                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                X_train,y_train,X_test,y_test=self.load_and_split_data()
                bestModel, bestParams=self.train_lgbm(X_train,y_train)
                metrics=self.eval_model(X_test,y_test,bestModel)
                self.saving_model(bestModel)

                logger.info(f"logging the model in the mlflow")
                mlflow.log_artifact(self.model_output_path)

                logger.info(f"logging the parameters and metrics in the mlflow")
                mlflow.log_params(bestParams)
                mlflow.log_metrics(metrics)

        except Exception as e:
            logger.info(f"error while starting the pipeline {e}")
            raise CustomException("failed to start the pipeline", sys)

if __name__=="__main__":
    trainer = modelTraining(PROCESSED_TRAIN_DATA_PATH,PROCESSED_TEST_DATA_PATH,MODEL_OUTPUT_PATH)
    trainer.run()

