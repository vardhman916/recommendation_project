import os
import pandas
from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
import sys
import yaml
import pandas as pd

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File is not in the given path")
        

        with open(file_path,"r") as yaml_file:
            config = yaml.safe_load(yaml_file)
            logging.info("Succesfully read the yaml file")
            return config
    
    except Exception as e:
        logging.info("Error while reading the yaml file")
        raise CustomException(e,sys)
