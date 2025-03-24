import os

################### Data ingestion #################
RAW_DIR = 'artifacts/raw'
CONFIG_PATH = 'config/config.yaml'


################# Data Processing #################

Processed_dir = 'artifacts/processed'
AnimeList_csv = 'artifacts/raw/animelist.csv'
Anime_csv = "artifacts/raw/anime.csv"
Anime_synopsis = 'artifacts/raw/anime_with_synopsis.csv'

X_train_array_path = os.path.join(Processed_dir,"X_train_array.pkl")
X_test_array_path = os.path.join(Processed_dir,"X_test_array.pkl")
y_train_path = os.path.join(Processed_dir,"y_train.pkl")
y_test_path = os.path.join(Processed_dir,"y_test.pkl")
RATING_DF = os.path.join(Processed_dir,"rating_df.csv")

RATING_DF = os.path.join(Processed_dir,"rating_df.csv")
DF = os.path.join(Processed_dir,"anime_df.csv")
SYNOPSIS_DF = os.path.join(Processed_dir,"synopsis_df.csv")

USER2USER_ENCODED = "artifacts/processed/user2user_encoded.pkl"
USER2USER_DECODED = "artifacts/processed/user2user_decoded.pkl"

ANIME2ANIME_ENCODED = "artifacts/processed/anime2anime_encoded.pkl"
ANIME2ANIME_DECODED = "artifacts/processed/anime2anime_decoded.pkl"


##################Model Training #################
CHECKPOINT_FILE_PATH = "artifacts/model_checkpoint/weights.weights.h5"
MODEL_DIR = "artifacts/model"
WEIGHT_DIR = "artifacts/weights"
MODEL_PATH = os.path.join(MODEL_DIR,"model.h5")
ANIME_WEIGHT_PATH = os.path.join(WEIGHT_DIR,"anime_weights.pkl")
USER_WEIGHT_PATH = os.path.join(WEIGHT_DIR,"user_weights.pkl")