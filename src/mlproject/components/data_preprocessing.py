import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
import sys
from config.path_config import *

class DataProcessor:
    def __init__(self,input_file,output_dir):
        self.input_file = input_file
        self.output_dir = output_dir
        self.rating_df = None
        self.anime_df = None
        self.X_train_array = None
        self.X_test_array = None
        self.y_train = None
        self.y_test = None
        self.X_train = None
        self.y_train = None

        self.user2user_encoded = {}
        self.user2user_decoded = {}
        self.anime2anime_encoded = {}
        self.anime2anime_decoded = {}

        os.makedirs(self.output_dir,exist_ok=True)
        logging.info("DataProcessing Intialized")

    def load_data(self,usecols):
        try:
            self.rating_df = pd.read_csv(self.input_file,low_memory=True,usecols=usecols)
            logging.info("data loaded succcessfully")
        except Exception as e:
            raise CustomException(e,sys)
        
    def filter_user(self):
        try:
            n_rating = self.rating_df['user_id'].value_counts()
            self.rating_df  = self.rating_df[self.rating_df['user_id'].isin(n_rating[n_rating>=400].index)].copy()
        except Exception as e:
            raise CustomException(e,sys)
        
    def scale_rating(self):
        try:
            min_rating = min(self.rating_df['rating'])
            max_rating = max(self.rating_df['rating'])
            self.rating_df['rating'] = self.rating_df['rating'].apply(lambda x:(x-min_rating)/(max_rating-min_rating)).values.astype(np.float64)
            logging.info("scalling done for processing")
        except Exception as e:
            raise CustomException(e,sys)
        
    def encoded_data(self):
        try:
            ## encoding for user_id
            user_ids = self.rating_df['user_id'].unique().tolist()
            self.user2user_encoded  = {x:i for i,x in enumerate(user_ids)}
            self.user2user_decoded  = {i:x for i,x in enumerate(user_ids)}
            self.rating_df['user'] = self.rating_df['user_id'].map(self.user2user_encoded)

            ## encoding for anime_id

            anime_ids = self.rating_df['anime_id'].unique().tolist()
            self.anime2anime_encoded  = {x:i for i,x in enumerate(anime_ids)}
            self.anime2anime_decoded  = {i:x for i,x in enumerate(anime_ids)}
            self.rating_df['anime'] = self.rating_df['anime_id'].map(self.anime2anime_encoded)
        
            logging.info("encoding done for User and anime")

        except Exception as e:
            raise CustomException(e,sys)
        
    def Split_data(self,test_size=1000):
        try:
            self.rating_df = self.rating_df.sample(frac = 1,random_state = 43).reset_index(drop=True)
            X = self.rating_df[['user','anime']].values
            y = self.rating_df['rating']
            train_indices = self.rating_df.shape[0] - test_size

            self.X_train, self.X_test, self.y_train, self.y_test = (
                                X[:train_indices],
                                X[train_indices:],
                                y[:train_indices],
                                y[train_indices:])
            
            self.X_train_array = [self.X_train[:,0],self.X_train[:,1]]
            self.X_test_array = [self.X_test[:,0],self.X_test[:,1]]

            logging.info("data splitted sucessfully")

        
        except Exception as e:
            raise CustomException(e,sys)
        
    def save_object(self):
        try:
            artifacts = {
                'user2user_encoded':self.user2user_encoded,
                'user2user_decoded':self.user2user_decoded,
                'anime2anime_encoded':self.anime2anime_encoded,
                'anime2anime_decoded':self.anime2anime_decoded
            }
            for name,data in artifacts.items():
                joblib.dump(data,os.path.join(self.output_dir,f"{name}.pkl"))
                logging.info(f"{name} saved successfully in processed directory")

            joblib.dump(self.X_train_array,X_train_array_path)
            joblib.dump(self.X_test_array,X_test_array_path)
            joblib.dump(self.y_train,y_train_path)
            joblib.dump(self.y_test,y_test_path)

            self.rating_df.to_csv(RATING_DF,index=False)
            logging.info(" All the files are successfully saved now")

        except Exception as e:
            raise CustomException(e,sys)
        
    def process_anime_data(self):
        try:
            df = pd.read_csv(Anime_csv)
            cols = ["MAL_ID","Name","Genres","sypnopsis"]
            synopsis_df = pd.read_csv(Anime_synopsis,usecols=cols)
            df = df.replace("Unknown",np.nan)

            def getAnimeName(anime_id):
                    try:
                        name = df[df['anime_id'] == anime_id].eng_version.values[0]
                        if name is np.nan:
                            name = df[df['anime_id'] == anime_id].Name.values[0]
                    except:
                        print("Error")
                    return name
            df["anime_id"] = df["MAL_ID"]
            df["eng_version"] = df["English name"]
            df["eng_version"] = df['anime_id'].apply(lambda x:getAnimeName(x))
            df.sort_values(by=["Score"],
               inplace=True,
               ascending=False,
               kind="quicksort",
               na_position="last")
            df = df[["anime_id" , "eng_version","Score","Genres","Episodes","Type","Premiered","Members"]]

            df.to_csv(DF,index = False)
            synopsis_df.to_csv(SYNOPSIS_DF,index=False)
            logging.info("df and syopsis save successfully")

        except Exception as e:
            raise CustomException(e,sys)
        
    def run(self):
        try:
            self.load_data(usecols=['user_id','anime_id','rating'])
            self.filter_user()
            self.scale_rating()
            self.encoded_data()
            self.Split_data()
            self.save_object()
            self.process_anime_data()

            logging.info("Data Processing pipelien run sucessfully")
        except CustomException as e:
            raise CustomException(e,sys)





        


