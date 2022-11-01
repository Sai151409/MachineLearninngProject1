import os, sys
from matplotlib.pyplot import table
from housing.entity.model_factor import GridSearchBestModel, MetricInfoArtifact, \
    ModelFactory, evaluate_regression_model
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import ModelTrainerConfig
from housing.entity.artifact_entity import DataTransformationArtifact, MOdelTrainerArtifact
from housing.util.util import *
from typing import List


class HousingEstimatorModel:
    
    def __init__(self, preprocessing_obj, trained_model_object):
        
        """
        preprocessing_object : preprocessing_object
        trained_model_object : trained_model_object
        """
        
        self.preprocessing_obj = preprocessing_obj
        self.trained_model_object = trained_model_object
        
    def predict(self, X):
        
        """
        This function accepts raw input and then transformed raw input using preprocessing
        object which guarentees that inputs are in the same format as training data 
        At last it perform prediction on transformed features
        """
        try:
            transformed_object = self.preprocessing_obj.transform(X)
            return self.trained_model_object.predict(transformed_object)
  
        except Exception as e:
            raise HousingException(e, sys) from e
        
    def __repr__(self) -> str:
        return f"{type(self.trained_model_object).__name__}()"
    
    def __str__(self) -> str:
        return f"{type(self.trained_model_object).__name__}()"


class ModelTrainer:
    
    def __init__(self, model_trainer_config : ModelTrainerConfig,
                 data_transformation_artifact : DataTransformationArtifact):
        try:
            logging.info(f'{"=" * 20} Model Trainer log started.{"<<" * 20}')
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise HousingException(e, sys) from e
        
    def initiate_model_trainer(self):
        try:
            logging.info('Loading the transformed training dataset')
            transformed_train_file_path = self.data_transformation_artifact.transformed_train_file_path
            train_array = load_numpy_array(transformed_train_file_path)
            
            logging.info('Loading the transformed test dataset')
            transformed_test_file_path = self.data_transformation_artifact.transformed_test_file_path
            test_array = load_numpy_array(transformed_test_file_path)
            
            logging.info('Splitting training and testing input feature and target feature')
            X_train, y_train, X_test, y_test = train_array[:, :-1], train_array[:, -1], test_array[:, :-1], test_array[:, -1]
            
            logging.info('Extracting model config file path')
            model_config_file_path = self.model_trainer_config.model_config_file_path
            
            logging.info("Initializing model factory class by using model config yaml file")
            model_factory = ModelFactory(model_config_path=model_config_file_path)
            
            base_accuracy = self.model_trainer_config.base_accuracy
            logging.info(f"Expected base accuracy : {base_accuracy}")
            
            logging.info("Initiating operation model selection")
            best_model = model_factory.get_best_model(X=X_train, y=y_train, base_accuracy=base_accuracy)
            
            logging.info(f"Best model found on training dataset : {best_model}")
            
            logging.info("Extracting trained model list")
            grid_searched_best_model_list:List[GridSearchBestModel] = model_factory.grid_searched_best_model_list
            print(grid_searched_best_model_list)
            
            model_list = [model.best_model for model in grid_searched_best_model_list]
            print(model_list)
            
            logging.info(f"Evaluation all trained model on training and testing dataset both")
            metric_info : MetricInfoArtifact = evaluate_regression_model(
                model_list=model_list,
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                base_accuracy=base_accuracy
            )
            
            model_object = metric_info.model_object
            
            trained_model_file_path = self.model_trainer_config.trained_model_file_path
            
            preprocessing_obj = load_object(file_path=self.data_transformation_artifact.preprocessed_object_file_path)
            
            housing_model = HousingEstimatorModel(preprocessing_obj=preprocessing_obj,
                                                  trained_model_object=model_object)
            
            save_object(file_path=trained_model_file_path, obj=housing_model)
            
            model_trainer_artifact = MOdelTrainerArtifact(
                trained_model_file_path=trained_model_file_path,
                train_rmse=metric_info.train_rmse,
                test_rmse=metric_info.test_rmse,
                train_accuracy=metric_info.train_accuracy,
                test_accuracy=metric_info.test_accuracy,
                model_accuracy=metric_info.model_accuracy
            )
            
            return model_trainer_artifact
            
        except Exception as e:
            raise HousingException(e, sys) from e
        
        
    def __del__(self):
        return f"{'>>' * 30} Model Trainer log is completed {'<<' * 30}"