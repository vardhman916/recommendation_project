import os
import pandas as pd
from google.cloud import storage
from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
from config.path_config import *
import sys
from src.mlproject.common_function import read_yaml

class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_names = self.config["bucket_file_names"]

        os.makedirs(RAW_DIR,exist_ok=True)

        logging.info("Data Ingestion started....")

    def download_csv_from_gcp(self):
        try:

            client = storage.Client() #It is use to allows you to interact with Google Cloud Storage (GCS).
            bucket = client.bucket(self.bucket_name)

            for file_name in self.file_names:
                file_path = os.path.join(RAW_DIR,file_name)

                if file_name == "animelist.csv":
                    blob = bucket.blob(file_name)  # ✅ Reference a file inside the bucket
                    blob.download_to_filename(file_path) # ✅ Download the file to local system

                    data = pd.read_csv(file_path,nrows=5000000)
                    data.to_csv(file_path,index=False)  #Saves only the 5M rows back to the same file, overwriting the original CSV.

                    logging.info("Large file detected only downloading 5M rows")
                else:
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(file_path)

        except Exception as e:
            raise CustomException(e,sys)
        

    def run(self):
        try:
            logging.info("starting data ingestion")
            self.download_csv_from_gcp()
            logging.info("data ingestion completed...")
        
        except Exception as e:
            raise CustomException(e,sys)
        



            
