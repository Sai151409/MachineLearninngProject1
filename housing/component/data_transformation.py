from housing.entity.config_entity import DataTransformationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact,\
DataTransformationArtifact
from housing.logger import logging
from housing.exception import HousingException
import os, sys
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pandas as pd
from housing.util.util import read_yaml_file

COLUMN_TOTAL_ROOMS = "total_rooms"
COLUMN_TOTAL_BEDROOMS = "total_bedrooms"
COLUMN_POPULATION = "population"
COLUMN_HOUSEHOLDS = "households"


# longitude : float
# latitude : float
# housing_median_age : float
# total_rooms : float
# total_bedrooms : float
# population : float
# households : float
# median_income : float
# median_house_value : float
# ocean_proximity : category
# income_cat : float

class FeatureGenerator(BaseEstimator, TransformerMixin):
    
    def __init__(self, add_bedrooms_per_room=True,
                 total_rooms_ix = 3,
                 total_bedrooms_ix = 4,
                 population_ix = 5,
                 households_ix = 6, columns = None):
        """
        FeatureGenerator Intialization
        add_bedroom_per_room : bool
        total_rooms_ix : int index number of total rooms column
        total_bedrooms_ix : int index number of total bedrooms column
        population_ix : int index number of population column
        households_ix : int index number of household column
        """
        try:
            self.columns = columns
            if self.columns is not None:
                total_rooms_ix = self.columns.index(COLUMN_TOTAL_ROOMS)
                total_bedrooms_ix = self.columns.index(COLUMN_TOTAL_BEDROOMS)
                population_ix = self.columns.index(COLUMN_POPULATION)
                households_ix = self.columns.index(COLUMN_HOUSEHOLDS)
            
            self.add_bedrooms_per_room = add_bedrooms_per_room
            self.total_rooms_ix = total_rooms_ix
            self.total_bedrooms_ix = total_bedrooms_ix
            self.population_ix = population_ix
            self.households_ix = households_ix
        except Exception as e:
            raise HousingException(e, sys) from e
        
    def fit(self, X, y = None):
        return self
    
    def transform(self, X, y = None):
        try:
            room_per_household = X[:, self.total_rooms_ix] / \
                X[:, self.households_ix]
            population_per_household = X[:, self.population_ix] / \
                X[:, self.households_ix]
            
            if self.add_bedrooms_per_room :
                bedrooms_per_room = X[:, self.total_bedrooms_ix] / \
                    X[:, self.total_rooms_ix]
                generated_feature = np.c_[X, room_per_household, population_per_household, bedrooms_per_room]
            
            else:
                generated_feature = np.c_[X, room_per_household, population_per_household]
        
            return generated_feature
        except Exception as e:
            raise HousingException(e, sys) from e
        

class DataTransformation:
    
    def __init__(self, data_transformation_config : DataTransformationConfig,
                 data_ingestion_artifact : DataIngestionArtifact,
                 data_validation_artifact : DataValidationArtifact):
        try:
            
            logging.info(f"{'>' * 20} Data Transformation log started {'<' * 20}")
            
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise HousingException(e, sys) from e
    
    def load_data(file_path : str, schema_file_path : str) -> pd.DataFrame:
        try:
            pass
        except Exception as e:
            raise HousingException(e, sys) from e