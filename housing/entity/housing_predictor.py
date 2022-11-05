import os,sys
from housing.util.util import load_object
from housing.exception import HousingException
import pandas as pd

class HousingData:
    
    def __init__(self,
                 latitude : float,
                 longitude : float,
                 housing_median_age : float,
                 total_rooms : float,
                 total_bedrooms : float,
                 population : float,
                 households : float,
                 median_income : float,
                 ocean_proximity : str,
                 median_house_value : float = None):
        try:
            self.latitude = latitude
            self.longitude=longitude
            self.housing_median_age=housing_median_age
            self.total_rooms=total_rooms
            self.total_bedrooms=total_bedrooms
            self.population=population
            self.households=households
            self.median_income=median_income
            self.ocean_proximity=ocean_proximity
            self.median_house_value=median_house_value
        except Exception as e:
            raise HousingException(e, sys) from e
        
    def housing_input_data_frame(self) : 
        try:
            data = self.get_housing_data_as_dict()
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            raise HousingException(e, sys) from e
        
    def get_housing_data_as_dict(self):
        try:
            input_data = {
                "latitude" : [self.latitude],
                "longitude" : [self.longitude],
                "housing_median_age" : [self.housing_median_age],
                "total_rooms" : [self.total_rooms],
                "total_bedrooms" : [self.total_bedrooms],
                "population" : [self.population],
                "households" : [self.households],
                "median_income" : [self.median_income],
                "median_house_value" : [self.median_house_value],
                "ocean_proximity" : [self.ocean_proximity]
            }
            return input_data
        except Exception as e:
            raise HousingException(e, sys) from e
        
        
class HousingPredictor:
    
    def __init__(self, model_dir : str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise HousingException(e, sys) from e
    
    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            filename = os.listdir(latest_model_dir)[0]
            latest_model_file_path = os.path.join(latest_model_dir, filename)
            return latest_model_file_path
        except Exception as e:
            raise HousingException(e, sys) from e
    
    def predict(self, X):
        try:
            model_file_path =  self.get_latest_model_path()
            
            model = load_object(file_path=model_file_path)
            
            median_housing_value = model.predict(X)
            
            return median_housing_value
        except Exception as e:
            raise HousingException(e, sys) from e