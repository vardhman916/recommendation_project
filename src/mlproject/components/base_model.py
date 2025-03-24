from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input,Embedding,Dot,Flatten,Dense,Activation,BatchNormalization
from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
from src.mlproject.common_function import read_yaml
from config.path_config import *
import sys

class BaseModel:
    def __init__(self,config_path):
        try:
            self.config = read_yaml(config_path)
            logging.info('Loaded config from config.yaml')
        except Exception as e:
            raise CustomException(e,sys)
        
    def RecommenderNet(self,n_users,n_anime):
        try:
            embedding_size = self.config["model"]["embedding"] #means each user and anime (item) will be represented as a 128-dimensional vector.
            user = Input(name = 'user',shape = [1])
            user_embedding = Embedding(name = 'user_embedding',input_dim=n_users,output_dim = embedding_size)(user)
            anime = Input(name = 'anime',shape = [1])
            anime_embedding = Embedding(name = 'anime_embedding',input_dim = n_anime,output_dim = embedding_size)(anime)
            '''user_id = 3 → [0.1, -0.3, ..., 0.7] (128 values)
            anime_id = 5 → [0.5, -0.1, ..., -0.4] (128 values)'''


            x = Dot(name = "dot_product",normalize = True,axes = 2)([user_embedding,anime_embedding])
            # it give the similarity between 
            
            x = Flatten()(x)

            x = Dense(1,kernel_initializer='he_normal')(x)
            x = BatchNormalization()(x)
            x = Activation("sigmoid")(x)
            model = Model(inputs = [user,anime],outputs = x)
            model.compile(
                loss = self.config["model"]["loss"],
                metrics = self.config["model"]["metrics"],
                optimizer = self.config["model"]["optimizer"])
            return model
        
        except Exception as e:
            raise CustomException(e,sys)
