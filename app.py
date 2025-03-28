from src.mlproject.components.data_ingestion import DataIngestion
from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
import sys
from src.mlproject.common_function import read_yaml
from config.path_config import *
from src.mlproject.components.data_preprocessing import DataProcessor
from src.mlproject.components.data_trainer import ModelTraining
from src.mlproject.helper import *
from src.mlproject.pipeline.predict_pipeline import hybrid_recommendation

if __name__=='__main__':
    try:
        # data_ingestion  = DataIngestion(read_yaml(CONFIG_PATH))
        # data_ingestion.run() 

        # data_processor  = DataProcessor(AnimeList_csv,Processed_dir)
        # data_processor.run()
        # model_trainer = ModelTraining(Processed_dir)
        # model_trainer.run()
        # print(getAnimeFrame(40028,DF))
        # similar_user = find_similar_users(11880,USER_WEIGHT_PATH,USER2USER_ENCODED,USER2USER_DECODED)
        # user_pref = get_user_preferences(11880 ,RATING_DF,DF)
        # print(user_pref)

        print(hybrid_recommendation(11880))




    except Exception as e:
        raise CustomException(e,sys)
