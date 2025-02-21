import os
import pickle

import numpy as np
import pandas as pd
from sklearn.preprocessing import FunctionTransformer
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_score, GridSearchCV

from src.exceptions import CustomException
from src.logger import logging
    
def get_frequency_counts(X: pd.Series):
    val_counts = X.value_counts()
    return X.apply(lambda item: val_counts[item]).to_frame()        
    # converting to DataFrame cuz sklearn ColumnTransformer and Pipelines transform function 
    # needs to output a 2D numpy array or a dataframe 

# Article on custom sklearn transformers: https://www.andrewvillazon.com/custom-scikit-learn-transformers/
FrequencyEncoder = FunctionTransformer(get_frequency_counts)
        

def save_object(obj, obj_path):
    try:
        DIR_NAME = os.path.dirname(obj_path)
        os.makedirs(DIR_NAME, exist_ok=True)
        with open(obj_path, "wb") as file:
            pickle.dump(obj, file)
    except Exception as e:
        logging.exception(e)
        raise CustomException(e)


def load_object(obj_path):
    try:
        DIR_NAME = os.path.dirname(obj_path)
        os.makedirs(DIR_NAME, exist_ok=True)
        with open(obj_path, "rb") as file:
            return pickle.load(file)
    except Exception as e:
        logging.exception(e)
        raise CustomException(e)
    

def evaluate_model(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    cv_score = cross_val_score(model, X_train, y_train, cv=3, n_jobs=-1)
    r2_score_ = r2_score(y_test, y_pred)
    print(f"""
        Evaluating model: {model}
        R2 Score: {r2_score_}
        Mean Cross Val Score: {cv_score.mean()}
        """)
    return r2_score_


def tune_model(model, params, X_train, y_train):
    print(f"""
        Using model: {model}
        Using param grid: {params}
        """)
    
    gs = GridSearchCV(estimator=model, param_grid=params, cv=3, n_jobs=-1, verbose=1)
    gs.fit(X_train, y_train)

    print(f"""
        Best score: {gs.best_score_}
        Best params: {gs.best_params_}
        Best estimator: {gs.best_estimator_}
        """)


    return gs.best_estimator_
    
