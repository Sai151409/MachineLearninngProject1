import os, sys

from matplotlib import test
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact
from housing.logger import logging
from housing.exception import HousingException
import pandas as pd
from housing.util.util import read_yaml_file


class DataValidation:
    
    def __init__(self, data_validation_config : DataValidationConfig,
                 data_ingestion_artifact : DataIngestionArtifact):
        try:
            logging.info(f"{'>' * 20} Data Validation log started {'<' * 20}")
            
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            
        except Exception as e:
            raise HousingException(e, sys) from e
        
    def _is_train_test_file_exists(self) -> bool:
        try :
            logging.info('Checking train and test files are available')
            is_train_file_exist = False
            is_test_file_exist = False
            
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)
            
            is_available =  is_train_file_exist and is_test_file_exist
            
            logging.info(f'Is train and test file exists -> {is_available}')
            
            if not is_available :
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message = f"Training file  : {training_file} or Testing file :  {testing_file} is not present"
                logging.info(message)
                raise Exception(message)
            
            return is_available
        except Exception as e:
            raise HousingException(e, sys) from e
        
    def validate_dataset_schema(self) -> bool:
        try:
            validation_status = False
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            schema_file = read_yaml_file(self.data_validation_config.schema_file_path)
            logging.info('Validating the train dataset, test dataset and schema file')
            if len(list(train_df.columns)) == len(list(test_df.columns)) == len(list(schema_file['columns'])):
                for i in schema_file['domain_value']:
                    if list(train_df[i].unique()).sort() == list(test_df[i].unique()).sort() == schema_file['domain_value'][i].sort():
                        if list(train_df.columns) == list(test_df.columns) == list(schema_file['columns']):
                            validation_status = True
                        else:
                            message = f"""Columns are not same in train dataset : {train_df}, test dataset :{test_df}, 
                            schemafile :{schema_file} that's why we don't take this dataset."""
                            raise Exception(message)
                    else:
                        message = f"""No fo columns are different in train dataset : {train_df}, test dataset :{test_df}, 
                        schemafile :{schema_file} that's why we don't take this dataset."""
                        raise Exception(message)
            else:
                message = f"""Columns are not same in train dataset : {train_df}, test dataset :{test_df}, 
                schemafile :{schema_file} that's why we don't take this dataset."""
                raise Exception(message)
            logging.info("Validation of train_df, test_df and schema file successfully completed.")
            return validation_status
        except Exception as e:
            raise HousingException(e, sys) from e    
    
    def intiate_data_validation(self):
        try:
            self._is_train_test_file_exists()
            self.validate_dataset_schema()
            
            
        except Exception as e:
            raise HousingException(e, sys) from e