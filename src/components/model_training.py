import os
from dataclasses import dataclass
import yaml
import importlib

import numpy as np
import pandas as pd

from src.exceptions import CustomException
from src.logger import logging
from src.utils import evaluate_model, tune_model, save_object


@dataclass
class ModelTrainingConfig:
    model_object_path: str = os.path.join("artifacts", "model.pkl")
    models_and_params_path: str = os.path.join("configs", "models_and_params.yaml")     # for storing the models and parameters to be evaluated 

class ModelTrainer:
    def __init__(self):
        self.config = ModelTrainingConfig()

    # load models and hyperparameter configs
    def get_models_and_params(self):
        try:
            logging.info("Models and parameters being loaded")
            with open(self.config.models_and_params_path, "rt") as file:
                config = yaml.safe_load(file)
                
                models = {}
                for model_name, model_config in config["models"].items():
                    module_name, class_name = model_config["class"].rsplit(".", 1)
                    module = importlib.import_module(module_name)
                    model_class = getattr(module, class_name)
                    model_object = model_class()
                    model_params = model_config["params"]

                    model_details = {
                        "model_object": model_object,
                        "model_params": model_params
                    }

                    models[model_name] = model_details

                logging.info("Models and parameters loaded")
                
                return models
                    
        except Exception as e:
            logging.exception(e)
            raise CustomException(e)

    def initiate_model_training(self, X_train, y_train, X_test, y_test):
        logging.info("Model training initiated")
        try:
            models = self.get_models_and_params()

            performace_metrics = {}
            for model_name, model_details in models.items():
                r2_score = evaluate_model(
                    model_details["model_object"],
                    X_train, 
                    y_train, 
                    X_test, 
                    y_test)
                
                performace_metrics[model_name] = r2_score
            
            # finding the best model
            best_model = max(performace_metrics, key=performace_metrics.get)   

            # hyperparameter tuning the best model
            logging.info(f"Tuning best model: {best_model}")
            best_tuned_model = tune_model(
                model = models[best_model]["model_object"],
                params = models[best_model]["model_params"],
                X_train=X_train,
                y_train=y_train
            )

            save_object(best_tuned_model, self.config.model_object_path)
            logging.info("Model training successfull")
            
        except Exception as e:
            logging.exception(e)
            raise CustomException(e)
