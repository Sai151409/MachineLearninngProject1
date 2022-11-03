from housing.pipeline.pipeline import Pipeline
from housing.logger import logging
from housing.config.configuration import Configuration
from housing.component.data_ingestion import DataIngestion
from housing.component.data_validation import DataValidation
from housing.config.configuration import Configuration
from housing.component.data_transformation import DataTransformation


def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(f"{e}")
        print(e)
    
    
if __name__ == "__main__":
    main()
    
    