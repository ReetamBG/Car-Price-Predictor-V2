from src.components.data_ingestion import DataIngestor
from src.components.data_transformation import DataTransformer
from src.components.model_training import ModelTrainer

train_data_path, test_data_path = DataIngestor().initiate_data_ingestion()
X_train, y_train, X_test, y_test = DataTransformer().initiate_data_transformation(train_data_path, test_data_path)
ModelTrainer().initiate_model_training(X_train, y_train, X_test, y_test)