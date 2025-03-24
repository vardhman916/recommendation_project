import joblib
import numpy as np
import os
import comet_ml
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input,Embedding,Dot,Flatten,Dense,Activation,BatchNormalization
from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
from src.mlproject.common_function import read_yaml
from config.path_config import *
import sys
from tensorflow.keras.callbacks import ModelCheckpoint,LearningRateScheduler,TensorBoard,EarlyStopping
from src.mlproject.components.base_model import BaseModel

class ModelTraining:
    def __init__(self,data_path):
        self.data_path = data_path
        self.model = None
        self.experiment = comet_ml.Experiment(
            api_key="CzX2cRjvvkYTb8X8FC1IzWSaE",
            project_name="recommendation_project",
            workspace = "vardhman916"
        )
        logging.info("Model Training and comet_ml  intialized")

    def load_data(self):
        try:
            X_train_array = joblib.load(X_train_array_path)
            X_test_array = joblib.load(X_test_array_path)
            y_train = joblib.load(y_train_path)
            y_test = joblib.load(y_test_path)

            logging.info("data loaded succesfully for Model Training")
            return X_train_array,X_test_array,y_train,y_test
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def train_model(self):
        try:
            X_train_array,X_test_array,y_train,y_test = self.load_data()

            n_users = len(joblib.load(USER2USER_ENCODED))
            n_anime = len(joblib.load(ANIME2ANIME_ENCODED))

            base_model = BaseModel(config_path = CONFIG_PATH)
            self.model = base_model.RecommenderNet(n_users = n_users,n_anime = n_anime)
            start_lr = 0.0001
            min_lr = 0.0001
            max_lr = 0.00005
            batch_size = 10000
            ramup_epochs = 5
            sustain_epochs = 0
            exp_decay = 0.8

            def lrfn(epoch):
                if epoch<ramup_epochs:
                    return (max_lr-start_lr)/ramup_epochs*epoch + start_lr
                elif epoch<ramup_epochs+sustain_epochs:
                    return max_lr
                else:
                    return (max_lr-min_lr) * exp_decay ** (epoch-ramup_epochs-sustain_epochs)+min_lr

            lr_callback = LearningRateScheduler(lambda epoch:lrfn(epoch) , verbose = 0)
            checkpoint_filepath = CHECKPOINT_FILE_PATH

            model_checkpoint = ModelCheckpoint(filepath = CHECKPOINT_FILE_PATH,save_weights_only=True,monitor = 'val_loss',mode = 'min',save_best_only = True)

            early_stopping = EarlyStopping(patience = 3,monitor = 'val_loss',mode = 'min',restore_best_weights = True)  
            my_callbacks = [model_checkpoint,lr_callback,early_stopping]

            os.makedirs(os.path.dirname(CHECKPOINT_FILE_PATH),exist_ok  = True)
            os.makedirs(MODEL_DIR,exist_ok = True)
            os.makedirs(WEIGHT_DIR,exist_ok = True)

            try:
                history = self.model.fit(
                            x = X_train_array,
                            y = y_train,
                            batch_size = batch_size,
                            epochs = 1,
                            verbose = 2,
                            validation_data = (X_test_array,y_test),
                            callbacks = my_callbacks)
                self.model.load_weights(CHECKPOINT_FILE_PATH)
                logging.info("Model Training Completed...")

                for epoch in range(len(history.history['loss'])):
                    train_loss = history.history["loss"][epoch]
                    val_loss = history.history["val_loss"][epoch]

                    self.experiment.log_metric('train_loss',train_loss,step = epoch)
                    self.experiment.log_metric('val_loss',val_loss,step = epoch)
             
            except Exception as e:
                raise CustomException(e,sys)
            self.save_model_weights()
            
        except Exception as e:
            raise CustomException(e,sys)
        
    def extract_weight(self,name):
        try:
            weight_layer = self.model.get_layer(name)
            weights = weight_layer.get_weights()[0]
            weights = weights/np.linalg.norm(weights,axis = 1).reshape((-1,1))
            return weights
        except Exception as e:
            raise CustomException(e,sys)
        
    def save_model_weights(self):
        try:
            self.model.save(MODEL_PATH)
            logging.info(f"model saved to {MODEL_PATH}")

            user_weights = self.extract_weight('user_embedding')
            anime_weights = self.extract_weight('anime_embedding')

            joblib.dump(user_weights,USER_WEIGHT_PATH)
            joblib.dump(anime_weights,ANIME_WEIGHT_PATH)

            self.experiment.log_asset(MODEL_PATH)
            self.experiment.log_asset(ANIME_WEIGHT_PATH)
            self.experiment.log_asset(USER_WEIGHT_PATH)

            logging.info("user and anime weight saved successfully")

        except Exception as e:
            raise CustomException(e,sys)
        
    def run(self):
        try:
            self.load_data()
            self.train_model()
            self.save_model_weights()

            logging.info("Data Processing pipelien run sucessfully")
        except CustomException as e:
            raise CustomException(e,sys)

        
                
                




