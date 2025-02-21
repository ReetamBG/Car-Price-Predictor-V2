import os
import pandas as pd
from dataclasses import dataclass

from sklearn.model_selection import train_test_split

from src.logger import logging 
from src.exceptions import CustomException


@dataclass
class DataIngestionConfig:      # Configurations for the data ingestion component
    base_path: str = "artifacts"
    raw_data_path: str = os.path.join(base_path, "raw_data.csv")
    train_data_path: str = os.path.join(base_path, "train.csv")
    test_data_path: str = os.path.join(base_path, "test.csv")


class DataIngestor:
    def __init__(self, config: DataIngestionConfig = DataIngestionConfig()):
        self.config = config

    def initiate_data_ingestion(self):
        logging.info("Initializing data ingestion process")
        try:
            # Gotta change this to read from database
            data = pd.read_csv(os.path.join("notebooks", "data", "cardekho_dataset.csv"))
            logging.info("Data read successfully")

            os.makedirs(self.config.base_path, exist_ok=True)

            # storing the raw data file
            data.to_csv(self.config.raw_data_path, index=False)  

            # splitting and storing the train and test data
            train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
            train_data.to_csv(self.config.train_data_path, index=False)
            test_data.to_csv(self.config.test_data_path, index=False)

            logging.info("Data Ingestion Successful")

            return (
                self.config.train_data_path,
                self.config.test_data_path
            )

        except Exception as e:
            logging.error(f"Error in Data Ingestion: {e}")
            raise CustomException(e)
        

# Testing 
if __name__ == "__main__":
    train_data_path, test_data_path = DataIngestor().initiate_data_ingestion()
    print(train_data_path, test_data_path)
