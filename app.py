from src.mlproject.components.data_ingestion import DataIngestion
from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
import sys
from src.mlproject.common_function import read_yaml
from config.path_config import *
from src.mlproject.components.data_preprocessing import DataProcessor
from src.mlproject.components.data_trainer import ModelTraining

if __name__=='__main__':
    try:
        # data_ingestion  = DataIngestion(read_yaml(CONFIG_PATH))
        # data_ingestion.run() 

        # data_processor  = DataProcessor(AnimeList_csv,Processed_dir)
        # data_processor.run()
        model_trainer = ModelTraining(Processed_dir)
        model_trainer.run()

    except Exception as e:
        raise CustomException(e,sys)
