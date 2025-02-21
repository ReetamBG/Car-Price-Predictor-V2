import pandas as pd

from src.logger import logging
from src.exceptions import CustomException
from src.utils import load_object

from src.components.model_training import ModelTrainer
from src.components.data_transformation import DataTransformer

class Predictor:
    def __init__(self):
        model_object_path = ModelTrainer().config.model_object_path
        preprocessor_object_path = DataTransformer().config.preprocessor_object_file_path
        self.model = load_object(model_object_path)
        self.preprocessor = load_object(preprocessor_object_path)


    def get_data_as_df(
            self, car_name, vehicle_age, km_driven, mileage, engine, 
            max_power, seats, seller_type, fuel_type, transmission_type
    ):
        input_data_dict = {
            "car_name": [car_name], 
            "vehicle_age": [vehicle_age], 
            "km_driven": [km_driven], 
            "mileage": [mileage], 
            "engine": [engine], 
            "max_power": [max_power], 
            "seats": [seats], 
            "seller_type": [seller_type], 
            "fuel_type": [fuel_type], 
            "transmission_type": [transmission_type]
        }

        return pd.DataFrame(input_data_dict)
    

    """
    NOTE:
    All those initiate data ingestion, transformation, model training we dont need it here 
    Those stuff is only needed in training and helps to automate the training process using CI/CD
    In prediction we only load the models and objects and predict simply using model.predict() 
    """
    
    def predict(
            self, car_name, vehicle_age, km_driven, mileage, engine, 
            max_power, seats, seller_type, fuel_type, transmission_type
    ):
        try:
            data_df = self.get_data_as_df(
                car_name, vehicle_age, km_driven, mileage, engine, 
                max_power, seats, seller_type, fuel_type, transmission_type
            )

            data_transformed = self.preprocessor.transform(data_df)
            y_pred = self.model.predict(data_transformed)
            print( y_pred)

        except Exception as e:
            raise CustomException(e)
    

if __name__ == "__main__":
    predictor = Predictor()
    predictor.predict(
        car_name="Maruti Alto",
        vehicle_age=15,
        km_driven=120000,
        mileage=5.7,
        engine=796,
        max_power=46.3,
        seats=5,
        seller_type="Individual",
        fuel_type="Petrol",
        transmission_type="Manual"
    )


