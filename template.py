import os
from pathlib import Path
import logging

logging.basicConfig(level = logging.INFO)
project_name = 'mlproject'

file = [
    f"src/__init__.py",
    f"src/{project_name}/logger.py",
    f"src/{project_name}/exception.py",
    f"src/{project_name}/utils.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/components/data_ingestion.py",
    f"src/{project_name}/components/data_transformation.py",
    f"src/{project_name}/components/data_monitering.py",
    f"src/{project_name}/components/data_trainer.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/pipeline/training_pipeline.py",
    f"src/{project_name}/pipeline/predict_pipeline.py"
]


for filepath in file:
    filepath = Path(filepath)
    filedir,filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir,exist_ok = True)
        logging.info(f'Directory is successfully created of {filedir}')

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath,'w') as f:
            pass
            logging.info(f'{filename} is created')
    
    else:
        logging.info(f"{filename} is already created")

    
