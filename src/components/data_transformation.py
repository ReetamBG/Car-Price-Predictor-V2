import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from src.exceptions import CustomException
from src.logger import logging
from src.utils import FrequencyEncoder, save_object, load_object


@dataclass 
class DataTransformationConfig:     # Configurations for Data Transformation component
    preprocessor_object_file_path: str = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformer:
    def __init__(self):
        self.config = DataTransformationConfig()


    def get_data_preprocessor_object(self):
        try:
            numerical_features = [
                "vehicle_age", 
                "km_driven", 
                "mileage", 
                "engine", 
                "max_power", 
                "seats"
            ]
            
            categorical_features = [
                "seller_type",
                "fuel_type",
                "transmission_type",
            ]

            numerical_features_pipeline = Pipeline([
                ("imputer", SimpleImputer(strategy="mean")),
                ("scaler", StandardScaler())
            ])

            categorical_features_pipeline = Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder())
            ])

            preprocessor = ColumnTransformer([
                ("numerical_feature_transforms", numerical_features_pipeline, numerical_features),
                ("categorical_feature_transforms", categorical_features_pipeline, categorical_features),
                ("car_name_transform", FrequencyEncoder, "car_name")
            ])

            logging.info("Preprocessor object created")

            return preprocessor

        except Exception as e:
            raise CustomException(e)
        

    def initiate_data_transformation(self, train_data_path, test_data_path):
        logging.info("Data transformation process started")
        try:
            train_data = pd.read_csv(train_data_path)
            test_data = pd.read_csv(test_data_path)

            preprocessor = self.get_data_preprocessor_object()
            
            X_train = train_data.drop(columns=["brand", "model", "selling_price"])
            X_test = test_data.drop(columns=["brand", "model", "selling_price"])
            y_train = train_data["selling_price"]
            y_test = test_data["selling_price"]

            X_train_transformed = preprocessor.fit_transform(X_train)
            X_test_transformed = preprocessor.transform(X_test)
            logging.info("Preprocessor object fitted")

            save_object(preprocessor, self.config.preprocessor_object_file_path)
            logging.info("Preprocessor object saved")
            logging.info("Data transformation completed successfully")

            return (
                X_train_transformed,
                y_train,
                X_test_transformed, 
                y_test
            )

        except Exception as e:
            logging.exception(e)
            raise CustomException(e)
        


        